from datetime import datetime
from flask import Blueprint, jsonify, render_template, request, session, redirect, url_for, flash
from app.models.campaign import Campaign
from app.models.campaign_product import CampaignProduct
from app.models.commission import Commission
from app.models.koc import KOC
from app.models.order_pro import OrderPro
from app.models.product_business import ProductBusiness
from app.models.register_campaign import RegisterCampaign
from app.models.review_details import ReviewDetails
from app.models.reviews import Reviews
from app.routes.auth_routes import login_required
from app import db
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

    # Lấy trạng thái từ form lọc
    status = request.args.get('status', '')

    # Lọc đơn hàng theo trạng thái
    query = OrderPro.query.filter_by(kocId=koc.id).order_by(OrderPro.orderDate.desc())

    if status:
        query = query.filter(OrderPro.orderStatus == status)

    orders = query.all()

    return render_template('koc/orders.html', orders=orders, koc=koc)

@koc_bp.route('/order/<int:order_id>/rate/<int:product_id>', methods=['POST'])
@login_required
def submit_rating(order_id, product_id):
    koc = KOC.query.filter_by(userId=session.get('username')).first()
    if not koc:
        flash("Không tìm thấy người dùng KOC.", "danger")
        return redirect(url_for('home.homepage'))

    # Lấy thông tin đơn hàng và sản phẩm
    order = OrderPro.query.get_or_404(order_id)
    product = ProductBusiness.query.get_or_404(product_id)

    # Chỉ cho phép đánh giá nếu đơn hàng đã thành công
    if order.orderStatus != 'Đơn thành công':
        flash("Chỉ có thể đánh giá khi đơn hàng đã thành công.", "warning")
        return redirect(url_for('koc.view_orders'))

    # Lấy dữ liệu từ form
    rating = request.form.get('rating')
    comment = request.form.get('comment')

    # Tìm OrderDetail ứng với sản phẩm trong đơn hàng
    order_detail = OrderDetail.query.filter_by(orderId=order.id, productId=product_id).first()

    if order_detail:
        try:
            # Lưu đánh giá
            order_detail.rating = float(rating)
            order_detail.comment = comment
            db.session.commit()

            # Tính lại rating trung bình cho sản phẩm
            rated_details = (
                db.session.query(OrderDetail)
                .join(OrderPro, OrderDetail.orderId == OrderPro.id)
                .filter(
                    OrderDetail.productId == product_id,
                    OrderDetail.rating.isnot(None),
                    OrderPro.orderStatus == 'Đơn thành công'
                )
                .all()
            )

            if rated_details:
                avg_rating = sum([od.rating for od in rated_details]) / len(rated_details)
            else:
                avg_rating = 0

            product.rating = avg_rating
            db.session.commit()

            flash("Đánh giá sản phẩm thành công.", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Lỗi khi lưu đánh giá: {str(e)}", "danger")
    else:
        flash("Không tìm thấy chi tiết đơn hàng này.", "danger")

    return redirect(url_for('koc.order_detail', order_id=order.id))



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

@koc_bp.route('/order/<int:order_id>/cancel', methods=['POST'])
@login_required
def cancel_order(order_id):
    koc = KOC.query.filter_by(userId=session.get('username')).first()
    if not koc:
        flash("Không tìm thấy người dùng KOC.", "danger")
        return redirect(url_for('home.homepage'))

    # Lấy thông tin đơn hàng
    order = OrderPro.query.get_or_404(order_id)

    # Kiểm tra xem KOC có phải là người đăng ký đơn này không
    if order.koc.userId != session.get('profile_id'):
        flash("Bạn không có quyền hủy đơn hàng này.", "danger")
        return redirect(url_for('koc.view_orders'))

    # Kiểm tra trạng thái đơn hàng phải là "Chờ xác nhận" mới cho phép hủy
    if order.orderStatus != 'Chờ xác nhận':
        flash("Chỉ có thể hủy đơn khi đơn hàng đang ở trạng thái 'Chờ xác nhận'.", "warning")
        return redirect(url_for('koc.order_detail', order_id=order.id))

    # Cập nhật trạng thái đơn hàng thành "Đã hủy"
    order.orderStatus = 'Hủy'

    db.session.commit()
    flash("Đơn hàng đã được hủy.", "success")

    return redirect(url_for('koc.view_orders'))

@koc_bp.route('/registered-campaigns')
@login_required
def registered_campaigns():
    # Kiểm tra roleId có phải là 2 (KOC)
    if session.get('role') != 2:
        flash("Bạn không có quyền truy cập chức năng này.", "danger")
        return redirect(url_for('home.homepage'))

    # Lấy KOC theo session profile_id
    koc = KOC.query.filter_by(id=session.get('profile_id')).first()
    if not koc:
        flash("Không tìm thấy thông tin KOC.", "danger")
        return redirect(url_for('home.homepage'))

    # Truy vấn danh sách đăng ký chiến dịch
    registered = (
        RegisterCampaign.query
        .filter_by(kocId=koc.id)
        .join(RegisterCampaign.campaign_product)
        .join(CampaignProduct.campaign)
        .join(Campaign.business)
        .join(Campaign.category)
        .order_by(RegisterCampaign.registerDate.desc())
        .all()
    )

    return render_template('koc/registered_campaigns.html', registrations=registered, koc=koc)
@koc_bp.route('/registered-campaigns/<int:register_id>')
@login_required
def registered_campaign_detail(register_id):
    if session.get('role') != 2:
        flash("Bạn không có quyền truy cập chức năng này.", "danger")
        return redirect(url_for('home.homepage'))

    reg = RegisterCampaign.query.get_or_404(register_id)

    # Kiểm tra quyền sở hữu
    if reg.kocId != session.get('profile_id'):
        flash("Bạn không có quyền xem đăng ký này.", "danger")
        return redirect(url_for('koc.registered_campaigns'))

    review = Reviews.query.filter_by(registerId=reg.id).first()
    return render_template('koc/registered_campaign_detail.html', reg=reg, koc=reg.koc, review=review)


@koc_bp.route('/reviews', methods=['POST'])
@login_required
def submit_review():
    register_id = request.form.get('registerId')
    rating = request.form.get('rating')
    text = request.form.get('text')

    if not all([register_id, rating, text]):
        flash("Vui lòng điền đầy đủ thông tin.", "danger")
        return redirect(request.referrer or url_for('koc.dashboard'))

    try:
        # Tìm review hiện có
        review = Reviews.query.filter_by(registerId=register_id).first()

        if review:
            # Nếu đã có, cập nhật
            review.rating = float(rating)
            review.text = text
            review.updatedAt = datetime.utcnow()
            flash("Cập nhật bài review thành công!", "success")
        else:
            # Nếu chưa có, thêm mới
            review = Reviews(
                registerId=register_id,
                rating=float(rating),
                text=text,
                createdAt=datetime.utcnow(),
                updatedAt=datetime.utcnow()
            )
            db.session.add(review)
            flash("Đã gửi bài review thành công!", "success")

        db.session.commit()

    except Exception as e:
        flash(f"Lỗi khi gửi review: {e}", "danger")

    return redirect(request.referrer or url_for('koc.dashboard'))

@koc_bp.route('/my-reviews')
@login_required
def manage_my_reviews():
    # Kiểm tra vai trò có phải là KOC không
    if session.get('role') != 2:
        flash("Chức năng này chỉ dành cho KOC.", "danger")
        return redirect(url_for('home.homepage'))

    # Lấy thông tin KOC
    koc = KOC.query.filter_by(id=session.get('profile_id')).first()
    if not koc:
        flash("Không tìm thấy thông tin KOC.", "danger")
        return redirect(url_for('home.homepage'))

    # Lấy tất cả bài review thuộc về KOC
    reviews = (
        Reviews.query
        .join(Reviews.register)
        .join(RegisterCampaign.campaign_product)
        .join(CampaignProduct.campaign)
        .join(CampaignProduct.productBusinees)
        .filter(RegisterCampaign.kocId == koc.id)
        .order_by(Reviews.updatedAt.desc())
        .all()
    )

    return render_template('koc/manage_reviews.html', reviews=reviews, koc=koc)

@koc_bp.route('/my-reviews/<int:review_id>')
@login_required
def review_detail(review_id):
    if session.get('role') != 2:
        flash("Bạn không có quyền truy cập chức năng này.", "danger")
        return redirect(url_for('home.homepage'))

    review = Reviews.query.get_or_404(review_id)

    if review.register.kocId != session.get('profile_id'):
        flash("Bạn không có quyền xem bài review này.", "danger")
        return redirect(url_for('koc.manage_my_reviews'))

    comments = ReviewDetails.query.filter_by(reviewId=review.id).all()

    return render_template('koc/review_detail.html', review=review, comments=comments, koc=review.register.koc)


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


@koc_bp.route('/commission')
@login_required
def view_commission():
    koc = KOC.query.filter_by(userId=session.get('username')).first()
    if not koc or not koc.isKoc:
        flash("Chức năng này chỉ dành cho KOC chính thức.", "warning")
        return redirect(url_for('koc.dashboard'))

    # Lấy tất cả các commission của KOC này
    commissions = Commission.query.join(RegisterCampaign).filter(RegisterCampaign.kocId == koc.id).all()
    
    # Tính tổng tiền hoa hồng
    total_commission = sum(c.commissionMoney for c in commissions)

    print(f"Total commission: {total_commission}")  # In tổng hoa hồng

    commission_details = []
    for commission in commissions:
        register_campaign = RegisterCampaign.query.get(commission.registerId)
        print(f"Register Campaign ID: {register_campaign.id}, KOC ID: {register_campaign.kocId}, kocCode: {register_campaign.kocCode}")

        campaign_product = CampaignProduct.query.get(register_campaign.campaign_product_id)
        print(f"Campaign Product ID: {campaign_product.id}, Product ID: {campaign_product.productId}, Commission: {campaign_product.commission}")

        product = ProductBusiness.query.get(campaign_product.productId)
        print(f"Product Title: {product.title}, Amount: {product.amount}")

        # Tìm tất cả các đơn hàng có chi tiết đơn hàng nhập mã kocCode và có trạng thái "Đơn thành công"
        order_details = OrderDetail.query.join(OrderPro).filter(
            OrderDetail.kocCode == register_campaign.kocCode,
            OrderPro.orderStatus == 'Đơn thành công',
            OrderDetail.productId == product.id
        ).all()

        total_quantity = 0
        total_amount = 0
        for order_detail in order_details:
            print(f"Order Detail: Product ID: {order_detail.productId}, Quantity: {order_detail.quantity}, Amount: {order_detail.amountPerOne}")
            total_quantity += order_detail.quantity
            total_amount += order_detail.quantity * order_detail.amountPerOne

        # Tính hoa hồng
        commission_money = total_amount * (campaign_product.commission / 100)
        print(f"Commission Money for Product: {commission_money}")

        commission_details.append({
            'campaign_title': register_campaign.campaign_product.campaign.title,
            'product_title': product.title,
            'quantity_sold': total_quantity,
            'amount': commission.amount,
            'total_amount': total_amount,
            'commission_money': commission_money
        })

    return render_template('koc/commission.html', commission_details=commission_details, total_commission=total_commission, koc=koc)

# === Đăng ký trở thành KOC ===
@koc_bp.route('/register', methods=['POST'])
@login_required
def register_koc():
    koc = KOC.query.filter_by(userId=session.get('username')).first()
    if koc and koc.isKoc:
        flash("Bạn đã là KOC rồi.", "warning")
        return redirect(url_for('koc.dashboard'))

    if koc:
        # Kiểm tra các trường thông tin, nếu đầy đủ thì chuyển isKoc thành 1
        if all([koc.name, koc.dob, koc.gender, koc.phoneNumber, koc.address]):
            koc.isKoc = True
            koc.kocConfirmDate = datetime.utcnow()  # Xác nhận thời gian trở thành KOC
            db.session.commit()
            flash("Đăng ký trở thành KOC thành công!", "success")
        else:
            flash("Thông tin không đầy đủ, vui lòng cập nhật đầy đủ các trường trước khi đăng ký.", "danger")

    return redirect(url_for('koc.dashboard'))