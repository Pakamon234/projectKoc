from flask import Blueprint, render_template, session, redirect, url_for, flash
from app.models.koc import KOC
from app.models.order_pro import OrderPro
from app.models.product_business import ProductBusiness
from app.routes.auth_routes import login_required

koc_bp = Blueprint('koc', __name__, url_prefix='/koc')

# === Dashboard KOC chính ===
@koc_bp.route('/dashboard')
@login_required
def dashboard():
    if session.get('role') not in [2, 3]:
        flash("Bạn không có quyền truy cập trang này!", "danger")
        return redirect(url_for('home.homepage'))

    koc = KOC.query.filter_by(userId=session.get('username')).first()
    if not koc:
        flash("Không tìm thấy thông tin KOC.", "danger")
        return redirect(url_for('home.homepage'))

    return render_template('dashboard_koc.html', koc=koc)

# === Các route khác cho các chức năng trong dashboard ===
@koc_bp.route('/orders')
@login_required
def view_orders():
    koc = KOC.query.filter_by(userId=session.get('username')).first()
    if not koc:
        flash("Không tìm thấy người dùng.", "danger")
        return redirect(url_for('home.homepage'))

    orders = OrderPro.query.filter_by(kocId=koc.id).order_by(OrderPro.orderDate.desc()).all()
    return render_template('koc/orders.html', orders=orders, koc=koc)

from app.models.order_detail import OrderDetail
from app.models.product_business import ProductBusiness

@koc_bp.route('/order/<int:order_id>')
@login_required
def order_detail(order_id):
    koc = KOC.query.filter_by(userId=session.get('username')).first()
    order = OrderPro.query.get_or_404(order_id)

    if order.koc.userId != session.get('username'):
        flash("Bạn không có quyền xem đơn hàng này.", "danger")
        return redirect(url_for('koc.view_orders'))

    details = OrderDetail.query.filter_by(orderId=order_id).all()

    for d in details:
        pb = ProductBusiness.query.filter_by(id=d.productId).first()
        d.product_title = pb.title if pb else "Không rõ"
        d.image_url = f"/static/uploads/{pb.image}" if pb and pb.image else None

    return render_template('koc/order_detail.html', order=order, details=details, koc=koc)

@koc_bp.route('/comments')
@login_required
def view_comments():
    return render_template('koc/comments.html')

@koc_bp.route('/reviews')
@login_required
def view_reviews():
    return render_template('koc/reviews.html')

@koc_bp.route('/campaigns')
@login_required
def manage_campaigns():
    koc = KOC.query.filter_by(userId=session.get('username')).first()
    if not koc or not koc.isKoc:
        flash("Chức năng này chỉ dành cho KOC chính thức.", "warning")
        return redirect(url_for('koc.dashboard'))

    return render_template('koc/manage_campaigns.html')

@koc_bp.route('/my-reviews')
@login_required
def manage_my_reviews():
    koc = KOC.query.filter_by(userId=session.get('username')).first()
    if not koc or not koc.isKoc:
        flash("Chức năng này chỉ dành cho KOC chính thức.", "warning")
        return redirect(url_for('koc.dashboard'))

    return render_template('koc/manage_reviews.html')

@koc_bp.route('/commission')
@login_required
def view_commission():
    koc = KOC.query.filter_by(userId=session.get('username')).first()
    if not koc or not koc.isKoc:
        flash("Chức năng này chỉ dành cho KOC chính thức.", "warning")
        return redirect(url_for('koc.dashboard'))

    return render_template('koc/commission.html')
