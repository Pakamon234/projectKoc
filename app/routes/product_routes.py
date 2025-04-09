from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from app.models.product_business import ProductBusiness

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
    session['cart_total'] = cart_total  # Lưu tổng tiền vào session

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
