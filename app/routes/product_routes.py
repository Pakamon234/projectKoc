from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from app.models.business import Business
from app.models.product import Product
from app.models.product_business import ProductBusiness
from datetime import datetime
from app.models.order_pro import OrderPro
from app.models.order_detail import OrderDetail
from app.models.koc import KOC
from app import db
from app.models.product_category import ProductCategory
from app.models.register_campaign import RegisterCampaign
from app.models.review_details import ReviewDetails
from app.models.reviews import Reviews
product_bp = Blueprint('product', __name__, url_prefix='/products')

# Route để xem tất cả sản phẩm
@product_bp.route('/')
def view_products():
    # Lấy tất cả danh mục sản phẩm và doanh nghiệp
    product_categories = ProductCategory.query.all()
    businesses = Business.query.all()

    # Lọc theo tên sản phẩm, loại sản phẩm và tên doanh nghiệp
    product_name = request.args.get('product_name', '').strip()
    product_category_id = request.args.get('product_category', '').strip()
    business_name = request.args.get('business_name', '').strip()

    query = ProductBusiness.query

    # Lọc theo tên sản phẩm
    if product_name:
        query = query.filter(ProductBusiness.title.ilike(f"%{product_name}%"))
    
    # Lọc theo loại sản phẩm (sử dụng join với Product và ProductCategory)
    if product_category_id:
        query = query.join(ProductBusiness.product).join(Product.categories).filter(ProductCategory.id == int(product_category_id))
    
    # Lọc theo tên doanh nghiệp
    if business_name:
        query = query.join(ProductBusiness.business).filter(Business.name.ilike(f"%{business_name}%"))

    # Thực hiện truy vấn
    products_for_sale = query.all()

    return render_template('products.html', 
                           products_for_sale=products_for_sale, 
                           product_categories=product_categories,
                           businesses=businesses)


@product_bp.route('/product/<int:product_id>')
def view_product_details(product_id):
    # Lấy thông tin sản phẩm dựa trên product_id
    product = ProductBusiness.query.get_or_404(product_id)

    # Lấy tất cả các bình luận và đánh giá từ OrderDetail
    order_details = OrderDetail.query.filter_by(productId=product.id).all()

    # Truyền danh sách các bình luận và đánh giá vào template, thêm tên KOC
    reviews = []
    for order_detail in order_details:
        if order_detail.rating is not None:
            koc = KOC.query.get(order_detail.order.kocId)  # Lấy tên KOC từ OrderPro
            reviews.append({
                "rating": order_detail.rating,
                "comment": order_detail.comment,
                "kocName": koc.name if koc else "Không rõ",
                "kocCode": order_detail.kocCode
            })

    return render_template('product_details.html', product=product, reviews=reviews)




@product_bp.route('/add-to-cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    # Lấy sản phẩm từ database
    product = ProductBusiness.query.get_or_404(product_id)
    quantity = int(request.form['quantity'])  # Lấy số lượng từ form

    # Kiểm tra nếu giỏ hàng đã tồn tại trong session, nếu chưa thì khởi tạo
    if 'cart' not in session:
        session['cart'] = []

    # Kiểm tra xem sản phẩm đã có trong giỏ hàng chưa
    for item in session['cart']:
        if item['product_id'] == product_id:
            item['quantity'] += quantity  # Cập nhật số lượng nếu đã có trong giỏ hàng
            item['total'] = item['quantity'] * item['amount']  # Cập nhật tổng tiền
            session.modified = True  # Đánh dấu session đã thay đổi
            flash(f"Cập nhật số lượng sản phẩm {product.title} trong giỏ hàng!", "success")
            break
    else:
        # Thêm sản phẩm vào giỏ hàng (dưới dạng dictionary)
        session['cart'].append({
            'product_id': product.id,
            'title': product.title,
            'amount': product.amount,
            'quantity': quantity,
            'total': product.amount * quantity  # Tính tổng tiền ngay khi thêm sản phẩm
        })

    # Tính tổng tiền giỏ hàng và lưu vào session
    cart_total = sum(item['total'] for item in session['cart'])
    session['total_cart'] = cart_total  # Lưu tổng tiền vào session

    session.modified = True  # Đánh dấu session đã thay đổi

    flash(f"Sản phẩm {product.title} đã được thêm vào giỏ hàng!", "success")
    return redirect(url_for('product.view_product_details', product_id=product_id))



@product_bp.route('/cart')
def view_cart():
    # Lấy giỏ hàng từ session
    cart = session.get('cart', [])
    return render_template('cart.html', cart=cart)

@product_bp.route('/remove-from-cart/<int:product_id>')
def remove_from_cart(product_id):
    # Xóa sản phẩm khỏi giỏ hàng
    cart = session.get('cart', [])
    session['cart'] = [item for item in cart if item['product_id'] != product_id]
    session.modified = True

    # Cập nhật lại tổng tiền giỏ hàng (total_cart)
    total_cart = sum(item['total'] for item in session['cart'])
    session['total_cart'] = total_cart  # Lưu vào session

    flash("Sản phẩm đã được xóa khỏi giỏ hàng.", "info")
    return redirect(url_for('product.view_cart'))


@product_bp.route('/update-cart/<int:product_id>', methods=['POST'])
def update_cart(product_id):
    # Lấy giỏ hàng từ session
    cart = session.get('cart', [])

    # Kiểm tra xem sản phẩm có trong giỏ hàng không
    for item in cart:
        if item['product_id'] == product_id:
            # Cập nhật số lượng
            item['quantity'] = int(request.form['quantity'])
            item['total'] = item['quantity'] * item['amount']  # Cập nhật tổng tiền
            session.modified = True
            flash("Số lượng sản phẩm đã được cập nhật!", "success")
            break

    # Cập nhật lại tổng tiền giỏ hàng (total_cart)
    total_cart = sum(item['total'] for item in cart)
    session['total_cart'] = total_cart  # Lưu vào session

    session.modified = True
    return redirect(url_for('product.view_cart'))

@product_bp.route('/place-order', methods=['POST'])
def place_order():
    if 'username' not in session:
        flash("Bạn cần đăng nhập để đặt hàng.", "warning")
        return redirect(url_for('auth.login'))

    if session.get('role') not in [2, 3]:
        flash("Chỉ người tiêu dùng mới được đặt hàng.", "danger")
        return redirect(url_for('product.view_cart'))

    cart = session.get('cart', [])
    if not cart:
        flash("Giỏ hàng trống, không thể đặt hàng.", "warning")
        return redirect(url_for('product.view_cart'))
# Kiểm tra người dùng có số điện thoại chưa
    from app.models.koc import KOC
    koc = KOC.query.filter_by(userId=session['username']).first()
    if not koc or not koc.phoneNumber or koc.phoneNumber.strip() == "":
        flash("Bạn cần có số điện thoại trước khi đặt hàng.", "warning")
        return redirect(url_for('product.view_cart'))
    return redirect(url_for('product.checkout'))

@product_bp.route('/checkout', methods=['GET'])
def checkout():
    if 'username' not in session or session.get('role') not in [2, 3]:
        flash("Bạn không có quyền truy cập.", "danger")
        return redirect(url_for('auth.login'))

    cart = session.get('cart', [])
    total = session.get('total_cart', 0)
    return render_template('checkout.html', cart=cart, total=total)

@product_bp.route('/confirm-order', methods=['POST'])
def confirm_order():
    if 'username' not in session or session.get('role') not in [2, 3]:
        flash("Không hợp lệ.", "danger")
        return redirect(url_for('auth.login'))

    cart = session.get('cart', [])
    if not cart:
        flash("Giỏ hàng trống!", "warning")
        return redirect(url_for('product.view_cart'))

    koc = KOC.query.filter_by(userId=session['username']).first()
    if not koc:
        flash("Không tìm thấy người dùng.", "danger")
        return redirect(url_for('product.view_cart'))

    address = request.form['address']
    is_pay = bool(int(request.form['isPay']))
    total = session.get('total_cart', 0)

    # Tạo đơn
    order = OrderPro(
        kocId=koc.id,
        orderDate=datetime.utcnow(),
        isPay=is_pay,
        orderStatus="Chờ xác nhận",
        address=address,
        totalPrice=total
    )
    db.session.add(order)
    db.session.flush()  # Lấy order.id

    # Thêm chi tiết đơn hàng và lưu kocCode
    for item in cart:
        detail = OrderDetail(
            orderId=order.id,
            productId=item['product_id'],
            quantity=item['quantity'],
            amountPerOne=item['amount'],
            totalAmount=item['total'],
            kocCode=item.get('kocCode')  # Lưu kocCode vào đơn hàng

        )
        db.session.add(detail)

    db.session.commit()
    session.pop('cart', None)
    session.pop('total_cart', None)
    flash("Đặt hàng thành công!", "success")
    return redirect(url_for('product.view_products'))


from flask import request, flash, redirect, url_for, session
from app.models.register_campaign import RegisterCampaign
from app.models.product_business import ProductBusiness
from datetime import datetime

from flask import request, flash, redirect, url_for, session
from app.models.register_campaign import RegisterCampaign
from app.models.campaign_product import CampaignProduct
from datetime import datetime

@product_bp.route('/apply-koc-code/<int:product_id>', methods=['POST'])
def apply_koc_code(product_id):
    koc_code = request.form.get('kocCode')

    # Lấy sản phẩm và chiến dịch sản phẩm
    product = ProductBusiness.query.get_or_404(product_id)
    campaign_products = CampaignProduct.query.filter_by(productId=product.id).all()

    if not campaign_products:
        flash("Sản phẩm không thuộc chiến dịch nào.", "danger")
        return redirect(url_for('product.view_cart'))

    valid_campaign_found = False  # Biến kiểm tra xem có chiến dịch hợp lệ không

    # Kiểm tra tất cả các chiến dịch của sản phẩm
    for campaign_product in campaign_products:
        # Kiểm tra mã giới thiệu cho từng chiến dịch
        register_campaign = RegisterCampaign.query.filter_by(campaign_product_id=campaign_product.id, kocCode=koc_code).first()

        if register_campaign:
            # Kiểm tra nếu chiến dịch đang trong thời gian hoạt động
            current_date = datetime.utcnow().date()
            if not (register_campaign.campaign_product.campaign.registerStartDate <= current_date <= register_campaign.campaign_product.campaign.registerEndDate):
                flash(f"Mã giới thiệu {koc_code} đã hết hạn cho chiến dịch {campaign_product.campaign.title}.", "danger")
            else:
                # Nếu chiến dịch hợp lệ, áp dụng kocCode cho sản phẩm trong giỏ hàng
                for item in session['cart']:
                    if item['product_id'] == product_id:
                        item['kocCode'] = koc_code  # Lưu kocCode vào giỏ hàng
                        item['kocCodeValue'] = register_campaign.kocCodeValue  # Lưu giá trị mã giới thiệu
                        item['total'] = item['quantity'] * item['amount'] * (1 - item['kocCodeValue'])  # Áp dụng giảm giá
                        session.modified = True
                        flash(f"Mã giới thiệu {koc_code} đã được áp dụng cho sản phẩm {product.title}.", "success")
                        valid_campaign_found = True
                        break
                break

    # Tính lại tổng giỏ hàng (total_cart) sau khi áp dụng mã giới thiệu
    total_cart = sum(item['total'] for item in session['cart'])
    session['total_cart'] = total_cart  # Lưu lại tổng tiền vào session

    if not valid_campaign_found:
        flash(f"Mã giới thiệu {koc_code} không hợp lệ hoặc hết hạn cho tất cả các chiến dịch của sản phẩm.", "danger")

    return redirect(url_for('product.view_cart'))

