from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from app.models.product_business import ProductBusiness
from datetime import datetime
from app.models.order_pro import OrderPro
from app.models.order_detail import OrderDetail
from app.models.koc import KOC
from app import db
product_bp = Blueprint('product', __name__, url_prefix='/products')

# Route để xem tất cả sản phẩm
@product_bp.route('/')
def view_products():
    products_for_sale = ProductBusiness.query.all()  # Lấy tất cả sản phẩm
    return render_template('products.html', products_for_sale=products_for_sale)

# Thêm các route khác nếu cần (chi tiết sản phẩm, tạo sản phẩm mới, v.v.)
@product_bp.route('/product/<int:product_id>')
def view_product_details(product_id):
    # Lấy thông tin sản phẩm dựa trên product_id
    product = ProductBusiness.query.get_or_404(product_id)
    
    return render_template('product_details.html', product=product)

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

    # Thêm chi tiết đơn
    for item in cart:
        detail = OrderDetail(
            orderId=order.id,
            productId=item['product_id'],
            quantity=item['quantity'],
            amountPerOne=item['amount'],
            totalAmount=item['total']
        )
        db.session.add(detail)

    db.session.commit()
    session.pop('cart', None)
    session.pop('total_cart', None)
    flash("Đặt hàng thành công!", "success")
    return redirect(url_for('product.view_products'))

