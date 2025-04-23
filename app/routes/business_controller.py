from datetime import datetime
from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from app.models.campaign import Campaign
from app.models.campaign_category import CampaignCategory
from app.models.campaign_product import CampaignProduct
from app.models.order_detail import OrderDetail
from app.models.order_pro import OrderPro
from app.models.pro_cate import ProCate
from app.models.product_business import ProductBusiness
from app.models.product_category import ProductCategory
from app.models.user import User
from app.routes.auth_routes import login_required
from app.models.business import Business
from app import db
business_bp = Blueprint('business', __name__, url_prefix='/business')

@business_bp.route('/dashboard')
@login_required
def dashboard():
    if session.get('role') != 4:
        flash("Bạn không có quyền truy cập trang này!", "danger")
        return redirect(url_for('home.homepage'))

    business = Business.query.filter_by(userId=session.get('username')).first()
    if not business:
        flash("Không tìm thấy thông tin doanh nghiệp.", "danger")
        return redirect(url_for('home.homepage'))
    campaigns = Campaign.query.filter_by(businessId=business.id).order_by(Campaign.createdAt.desc()).all()
    # Chuyển sang template chính của dashboard (dashboard_business.html)
    return render_template('dashboard_business.html', business=business, campaigns=campaigns)

@business_bp.route('/profile')
@login_required
def view_profile():
    if session.get('role') != 4:
        flash("Bạn không có quyền truy cập.", "danger")
        return redirect(url_for('home.homepage'))

    business = Business.query.filter_by(userId=session.get('username')).first()
    if not business:
        flash("Không tìm thấy doanh nghiệp.", "danger")
        return redirect(url_for('home.homepage'))

    return render_template('business/profile.html', business=business)
@business_bp.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if session.get('role') != 4:
        flash("Không hợp lệ.", "danger")
        return redirect(url_for('home.homepage'))

    business = Business.query.filter_by(userId=session['username']).first()
    if request.method == 'POST':
        business.name = request.form['name']
        business.address = request.form['address']
        business.email = request.form['email']
        business.phoneNumber = request.form['phoneNumber']
        business.website = request.form['website']
        business.updatedAt = datetime.utcnow()
        db.session.commit()
        flash("Đã cập nhật thông tin doanh nghiệp.", "success")
        return redirect(url_for('business.view_profile'))

    return render_template('business/edit_profile.html', business=business)

@business_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    if session.get('role') != 4:
        flash("Không hợp lệ.", "danger")
        return redirect(url_for('home.homepage'))

    user = User.query.get(session['username'])
    if request.method == 'POST':
        old_password = request.form['old_password']
        new_password = request.form['new_password']

        if user.password.strip() != old_password.strip():
            flash("Mật khẩu cũ không đúng.", "danger")
            return redirect(url_for('business.change_password'))

        user.password = new_password
        user.updatedAt = datetime.utcnow()
        db.session.commit()
        flash("Đổi mật khẩu thành công.", "success")
        return redirect(url_for('business.view_profile'))

    return render_template('business/change_password.html')

@business_bp.route('/campaigns')
@login_required
def view_campaigns():
    business = Business.query.filter_by(userId=session.get('username')).first()
    if not business:
        flash("Không tìm thấy doanh nghiệp.", "danger")
        return redirect(url_for('home.homepage'))

    from app.models.campaign import Campaign
    campaigns = Campaign.query.filter_by(businessId=business.id).order_by(Campaign.createdAt.desc()).all()

    return render_template('business/business_campaigns.html', campaigns=campaigns)


@business_bp.route('/campaign/<int:campaign_id>')
@login_required
def campaign_detail(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)

    if campaign.business.userId != session.get('username'):
        flash("Bạn không có quyền xem chiến dịch này.", "danger")
        return redirect(url_for('business.dashboard'))

    campaign_products = CampaignProduct.query.filter_by(campaignId=campaign.id).all()

    return render_template(
        'business/campaign_detail.html',
        campaign=campaign,
        campaign_products=campaign_products
    )

@business_bp.route('/campaign/<int:campaign_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_campaign(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)

    # Kiểm tra quyền và trạng thái
    if campaign.business.userId != session.get('username'):
        flash("Bạn không có quyền chỉnh sửa chiến dịch này.", "danger")
        return redirect(url_for('business.dashboard'))
    if campaign.status not in [0, 1]:
        flash("Chỉ có thể chỉnh sửa chiến dịch khi đang chờ xác nhận hoặc đã xác nhận.", "warning")
        return redirect(url_for('business.campaign_detail', campaign_id=campaign.id))

    # Lấy danh sách loại chiến dịch và sản phẩm doanh nghiệp
    categories = CampaignCategory.query.all()
    products = ProductBusiness.query.filter_by(businessId=campaign.businessId).all()
    campaign_products = CampaignProduct.query.filter_by(campaignId=campaign.id).all()
    selected_products = {cp.productId: cp.commission for cp in campaign_products}

    if request.method == 'POST':
        # Cập nhật thông tin chiến dịch
        campaign.title = request.form['title']
        campaign.description = request.form['description']
        campaign.startDate = request.form['startDate']
        campaign.endDate = request.form['endDate']
        campaign.registerStartDate = request.form['registerStartDate']
        campaign.registerEndDate = request.form['registerEndDate']
        campaign.numberOfParticipants = request.form['numberOfParticipants']
        campaign.campaignCategoryId = request.form['campaignCategoryId']
        campaign.updatedAt = datetime.utcnow()

        # Nếu đang là "đã xác nhận", chuyển lại "chờ xác nhận"
        if campaign.status == 1:
            campaign.status = 0

        # Cập nhật sản phẩm chiến dịch
    selected_ids = request.form.getlist('product_ids')

    # Lấy tất cả CampaignProduct cũ để kiểm tra
    existing_cps = CampaignProduct.query.filter_by(campaignId=campaign.id).all()
    existing_map = {str(cp.productId): cp for cp in existing_cps}

    for pid in selected_ids:
        commission_val = request.form.get(f'commission_{pid}', '0').strip()
        try:
            commission = float(commission_val) / 100
        except ValueError:
            commission = 0.0

        if pid in existing_map:
            # Nếu đã tồn tại, cập nhật commission
            existing_map[pid].commission = commission
        else:
            # Nếu chưa có, thêm mới
            new_cp = CampaignProduct(
                campaignId=campaign.id,
                productId=int(pid),
                commission=commission
            )
            db.session.add(new_cp)

        db.session.commit()
        flash("Cập nhật chiến dịch thành công!", "success")
        return redirect(url_for('business.campaign_detail', campaign_id=campaign.id))

    return render_template(
        'business/edit_campaign.html',
        campaign=campaign,
        categories=categories,
        products=products,
        selected_products=selected_products
    )


@business_bp.route('/campaign/<int:campaign_id>/delete', methods=['POST'])
@login_required
def delete_campaign(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    if campaign.business.userId != session.get('username'):
        flash("Bạn không có quyền xóa chiến dịch này.", "danger")
        return redirect(url_for('business.dashboard'))
    
    if campaign.status != 0:
        flash("Chỉ có thể xóa chiến dịch ở trạng thái 'Chờ xác nhận'.", "warning")
        return redirect(url_for('business.campaign_detail', campaign_id=campaign.id))

    db.session.delete(campaign)
    db.session.commit()
    flash("Xóa chiến dịch thành công.", "success")
    return redirect(url_for('business.view_campaigns'))

@business_bp.route('/campaign/<int:campaign_id>/cancel', methods=['POST'])
@login_required
def cancel_campaign(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    if campaign.business.userId != session.get('username'):
        flash("Bạn không có quyền thao tác trên chiến dịch này.", "danger")
        return redirect(url_for('business.dashboard'))

    if campaign.status not in [0, 1]:
        flash("Chỉ có thể hủy chiến dịch ở trạng thái Chờ xác nhận hoặc Đã xác nhận.", "warning")
        return redirect(url_for('business.campaign_detail', campaign_id=campaign.id))

    campaign.status = 4  # 4 = Hủy
    campaign.updatedAt = datetime.utcnow()
    db.session.commit()
    flash("Chiến dịch đã được hủy.", "info")
    return redirect(url_for('business.campaign_detail', campaign_id=campaign.id))

@business_bp.route('/orders')
@login_required
def view_orders():
    business = Business.query.filter_by(userId=session.get('username')).first()
    if not business:
        flash("Không tìm thấy doanh nghiệp.", "danger")
        return redirect(url_for('home.homepage'))

    from app.models.order_pro import OrderPro
    from app.models.order_detail import OrderDetail
    from app.models.product_business import ProductBusiness

    # Lấy tất cả orderId có chứa sản phẩm thuộc doanh nghiệp này
    order_details = OrderDetail.query.join(ProductBusiness).filter(
        ProductBusiness.businessId == business.id
    ).all()

    order_map = {}
    for detail in order_details:
        if detail.orderId not in order_map:
            order_map[detail.orderId] = {
                'order': detail.order,
                'details': []
            }
        order_map[detail.orderId]['details'].append(detail)

    # Chuyển thành list để render
    orders = []
    for o in order_map.values():
        o['order'].details = o['details']
        orders.append(o['order'])

    return render_template('business/business_orders.html', orders=orders)

@business_bp.route('/orders/<int:order_id>')
@login_required
def order_detail(order_id):


    business = Business.query.filter_by(userId=session.get('username')).first()
    if not business:
        flash("Không tìm thấy doanh nghiệp.", "danger")
        return redirect(url_for('home.homepage'))

    order = OrderPro.query.get_or_404(order_id)

    # Lấy chi tiết đơn hàng nhưng chỉ sản phẩm thuộc doanh nghiệp này
    details = OrderDetail.query.join(ProductBusiness).filter(
        OrderDetail.orderId == order.id,
        ProductBusiness.businessId == business.id,
        OrderDetail.productId == ProductBusiness.id
    ).all()

    return render_template('business/business_order_detail.html', order=order, details=details)

@business_bp.route('/orders/<int:order_id>/confirm', methods=['POST'])
@login_required
def confirm_order(order_id):
    order = OrderPro.query.get_or_404(order_id)
    if order.orderStatus in [None, 'Chờ xác nhận']:
        order.orderStatus = 'Đặt thành công'
        db.session.commit()
        flash("Đơn hàng đã được duyệt.", "success")
    else:
        flash("Đơn hàng không hợp lệ để duyệt.", "warning")
    return redirect(request.referrer or url_for('business.view_orders'))

@business_bp.route('/orders/<int:order_id>/ship', methods=['POST'])
@login_required
def ship_order(order_id):
    order = OrderPro.query.get_or_404(order_id)
    if order.orderStatus != 'Đặt thành công':
        flash("Chỉ có thể giao hàng khi đơn ở trạng thái 'Đặt thành công'.", "warning")
        return redirect(url_for('business.order_detail', order_id=order.id))

    from app.models.order_detail import OrderDetail
    from app.models.product_business import ProductBusiness
    from app.models.business import Business

    business = Business.query.filter_by(userId=session.get('username')).first()
    if not business:
        flash("Không tìm thấy doanh nghiệp.", "danger")
        return redirect(url_for('home.homepage'))

    # Chỉ cập nhật số lượng tồn của sản phẩm thuộc doanh nghiệp hiện tại
    details = OrderDetail.query.join(ProductBusiness).filter(
        OrderDetail.orderId == order.id,
        ProductBusiness.businessId == business.id,
        OrderDetail.productId == ProductBusiness.id
    ).all()

    for d in details:
        if d.product_business.quantityInStock >= d.quantity:
            d.product_business.quantityInStock -= d.quantity
        else:
            flash(f"Sản phẩm '{d.product_business.title}' không đủ số lượng để giao.", "danger")
            return redirect(url_for('business.order_detail', order_id=order.id))

    order.orderStatus = 'Đã giao'
    db.session.commit()
    flash("Đã cập nhật trạng thái đơn hàng và trừ số lượng tồn.", "success")
    return redirect(url_for('business.order_detail', order_id=order.id))

@business_bp.route('/orders/<int:order_id>/cancel', methods=['POST'])
@login_required
def cancel_order(order_id):
    order = OrderPro.query.get_or_404(order_id)
    if order.orderStatus != 'Đang giao':
        flash("Chỉ có thể hủy đơn đang giao.", "warning")
        return redirect(url_for('business.order_detail', order_id=order.id))

    reason = request.form.get('reasonCancel')
    if not reason:
        flash("Vui lòng nhập lý do hủy.", "danger")
        return redirect(url_for('business.order_detail', order_id=order.id))

    # Hoàn trả số lượng tồn cho doanh nghiệp
    from app.models.product_business import ProductBusiness
    from app.models.order_detail import OrderDetail
    from app.models.business import Business

    business = Business.query.filter_by(userId=session.get('username')).first()

    details = OrderDetail.query.join(ProductBusiness).filter(
        OrderDetail.orderId == order.id,
        ProductBusiness.businessId == business.id,
        OrderDetail.productId == ProductBusiness.id
    ).all()

    for d in details:
        d.product_business.quantityInStock += d.quantity

    order.orderStatus = "Hủy"
    order.reasonCancel = reason
    db.session.commit()

    flash("Đã hủy đơn hàng, cập nhật kho và lưu lý do hủy.", "info")
    return redirect(url_for('business.order_detail', order_id=order.id))

@business_bp.route('/products')
@login_required
def view_products():
    from app.models.product_business import ProductBusiness
    business_id = Business.query.filter_by(userId=session.get('username')).first().id

    products = ProductBusiness.query.filter_by(businessId=business_id).order_by(ProductBusiness.createdAt.desc()).all()
    return render_template('business/business_products.html', products=products)

from app.models.order_detail import OrderDetail

@business_bp.route('/products/<int:product_id>/delete', methods=['POST'])
@login_required
def delete_product(product_id):
    product = ProductBusiness.query.get_or_404(product_id)
    business_id = Business.query.filter_by(userId=session.get('username')).first().id

    # Kiểm tra quyền sở hữu sản phẩm
    if product.businessId != business_id:
        flash("Không thể xóa sản phẩm không thuộc doanh nghiệp của bạn.", "danger")
        return redirect(url_for('business.view_products'))

    # Kiểm tra nếu sản phẩm đã xuất hiện trong bất kỳ đơn hàng nào
    used_in_orders = OrderDetail.query.filter_by(productId=product.id).first()
    if used_in_orders:
        flash("Sản phẩm đã được sử dụng trong đơn hàng, không thể xóa.", "warning")
        return redirect(url_for('business.view_products'))

    # Cho phép xóa nếu chưa từng dùng trong đơn hàng
    db.session.delete(product)
    db.session.commit()
    flash("Đã xóa sản phẩm thành công.", "success")
    return redirect(url_for('business.view_products'))


import os
from werkzeug.utils import secure_filename

@business_bp.route('/products/<int:product_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_product(product_id):
    product = ProductBusiness.query.get_or_404(product_id)
    business_id = Business.query.filter_by(userId=session.get('username')).first().id
    if product.businessId != business_id:
        flash("Không thể chỉnh sửa sản phẩm không thuộc doanh nghiệp của bạn.", "danger")
        return redirect(url_for('business.view_products'))

    if request.method == 'POST':
        product.title = request.form['title']
        product.description = request.form['description']
        product.amount = request.form['amount']
        product.unitOfMeasure = request.form['unitOfMeasure']
        product.quantityInStock = request.form['quantityInStock']
        product.updatedAt = datetime.utcnow()

        # Xử lý ảnh mới nếu có
        file = request.files.get('image')
        if file and file.filename:
            filename = secure_filename(file.filename)
            file_path = os.path.join('static/uploads', filename)
            file.save(file_path)
            product.image = filename

        db.session.commit()
        flash("Cập nhật sản phẩm thành công.", "success")
        return redirect(url_for('business.view_products'))

    return render_template('business/edit_product.html', product=product)

@business_bp.route('/product/<int:product_id>', methods=['GET'])
def view_product_detail(product_id):
    product_bus = ProductBusiness.query.get_or_404(product_id)
    product = product_bus.product
    categories = (
        db.session.query(ProductCategory)
        .join(ProCate, ProCate.productCategoryId == ProductCategory.id)
        .filter(ProCate.productId == product.id)
        .all()
    )
    return render_template('business/product_detail.html', product_bus=product_bus, product=product, categories=categories)
