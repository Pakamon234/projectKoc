from datetime import datetime
import os
from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from app import db
from app.models.business import Business
from app.models.campaign import Campaign
from app.models.campaign_category import CampaignCategory
from app.models.koc import KOC
from werkzeug.utils import secure_filename

from app.models.pro_cate import ProCate
from app.models.product import Product
from app.models.product_business import ProductBusiness
from app.models.product_category import ProductCategory
from app.models.employee import Employee
from app.routes.auth_routes import login_required

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@dashboard_bp.route('/koc')
@login_required
def koc_dashboard():
    if session.get('role') not in [2, 3]:
        flash("Bạn không có quyền truy cập!", "danger")
        return redirect(url_for('home.homepage'))

    koc = KOC.query.filter_by(userId=session.get('username')).first()

    if not koc:
        flash("Không tìm thấy thông tin KOC.", "danger")
        return redirect(url_for('home.homepage'))

    return render_template('dashboard_koc.html', koc=koc)

@dashboard_bp.route('/koc/edit', methods=['GET', 'POST'])
@login_required
def edit_koc_profile():
    if session.get('role') not in [2, 3]:
        flash("Bạn không có quyền truy cập!", "danger")
        return redirect(url_for('home.homepage'))

    koc = KOC.query.filter_by(userId=session.get('username')).first()

    if request.method == 'POST':
        koc.name = request.form['name']
        koc.dob = request.form['dob']
        koc.gender = request.form['gender']
        koc.phoneNumber = request.form['phoneNumber']
        koc.address = request.form['address']
        koc.bio = request.form['bio']
        koc.socialLink = request.form['socialLink']

        # Cập nhật ảnh nếu có
        if 'picture' in request.files:
            file = request.files['picture']
            if file and file.filename != '':
                filename = secure_filename(file.filename)
                upload_folder = os.path.join('app', 'static', 'uploads')
                os.makedirs(upload_folder, exist_ok=True)
                file_path = os.path.join(upload_folder, filename)
                file.save(file_path)
                koc.picture = filename

        # Cập nhật thời gian chỉnh sửa
        koc.updatedAt = datetime.utcnow()

        db.session.commit()

        flash("Hồ sơ đã được cập nhật!", "success")
        return redirect(url_for('dashboard.koc_dashboard'))

    return render_template('edit_koc_profile.html', koc=koc)

@dashboard_bp.route('/business')
@login_required
def business_dashboard():
    if session.get('role') != 4:
        flash("Bạn không có quyền truy cập!", "danger")
        return redirect(url_for('home.homepage'))

    # Lấy tất cả chiến dịch mà doanh nghiệp đã tạo
    business = Business.query.filter_by(userId=session['username']).first()
    # Lấy tất cả sản phẩm đã tạo
    products = Product.query.all()

    # Lấy tất cả sản phẩm đã đăng ký bán
    product_business = ProductBusiness.query.filter_by(businessId=session['profile_id']).all()
    if not business:
        flash("Không tìm thấy doanh nghiệp của bạn.", "danger")
        return redirect(url_for('home.homepage'))

    campaigns = Campaign.query.filter_by(businessId=business.id).all()

    return render_template('dashboard_business.html', campaigns=campaigns, products=products, product_business=product_business)


@dashboard_bp.route('/business/create-campaign', methods=['GET', 'POST'])
@login_required
def create_campaign():
    if session.get('role') != 4:
        flash("Bạn không có quyền truy cập!", "danger")
        return redirect(url_for('home.homepage'))

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        register_start_date = request.form['register_start_date']
        register_end_date = request.form['register_end_date']
        number_of_participants = request.form['number_of_participants']
        campaign_category_id = request.form['campaign_category_id']
        
        business = Business.query.filter_by(userId=session['username']).first()
        if not business:
            flash("Không tìm thấy doanh nghiệp của bạn.", "danger")
            return redirect(url_for('home.homepage'))

        # Giờ lấy businessId từ bản ghi doanh nghiệp
        campaign = Campaign(
            businessId=business.id,  # Dùng business.id thay vì session['username']
            campaignCategoryId=campaign_category_id,
            title=title,
            description=description,
            startDate=start_date,
            endDate=end_date,
            registerStartDate=register_start_date,
            registerEndDate=register_end_date,
            numberOfParticipants=number_of_participants,
            status=0,  # Mặc định là chưa kích hoạt
            createdAt=datetime.utcnow(),
            updatedAt=datetime.utcnow()
        )

        db.session.add(campaign)
        db.session.commit()
        flash("Chiến dịch đã được tạo!", "success")
        return redirect(url_for('dashboard.business_dashboard'))

    categories = CampaignCategory.query.all()  # Lấy tất cả danh mục chiến dịch
    return render_template('create_campaign.html', categories=categories)

@dashboard_bp.route('/business/create-product', methods=['GET', 'POST'])
@login_required
def create_product():
    if session.get('role') != 4:
        flash("Bạn không có quyền truy cập!", "danger")
        return redirect(url_for('home.homepage'))

    # Lấy tất cả danh mục sản phẩm
    categories = ProductCategory.query.all()

    if request.method == 'POST':
        name = request.form['name']
        categories_selected = request.form.getlist('categories')  # Nhận danh sách các danh mục được chọn

        # Tạo sản phẩm mới
        product = Product(
            name=name,
            createdAt=datetime.utcnow(),
            updatedAt=datetime.utcnow()
        )
        db.session.add(product)
        db.session.commit()  # Lưu sản phẩm vào DB

        # Liên kết sản phẩm với các danh mục
        for category_id in categories_selected:
            pro_cate = ProCate(
                productId=product.id,
                productCategoryId=category_id
            )
            db.session.add(pro_cate)

        db.session.commit()
        flash("Sản phẩm đã được đăng ký!", "success")
        return redirect(url_for('dashboard.business_dashboard'))

    return render_template('create_product.html', categories=categories)

@dashboard_bp.route('/business/create-product-business', methods=['GET', 'POST'])
@login_required
def create_product_business():
    if session.get('role') != 4:
        flash("Bạn không có quyền truy cập!", "danger")
        return redirect(url_for('home.homepage'))

    # Lấy tất cả sản phẩm và danh mục
    products = Product.query.all()
    categories = ProductCategory.query.all()

    if request.method == 'POST':
        product_id = request.form['product_id']
        title = request.form['title']
        description = request.form['description']
        unit_of_measure = request.form['unit_of_measure']
        amount = request.form['amount']
        quantity_in_stock = request.form['quantity_in_stock']
        
        # Xử lý ảnh
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename != '':
                filename = secure_filename(file.filename)
                upload_folder = os.path.join('app', 'static', 'uploads')
                os.makedirs(upload_folder, exist_ok=True)
                file_path = os.path.join(upload_folder, filename)
                file.save(file_path)
            else:
                filename = None
        
        # Lấy businessId từ session
        business_id = session.get('profile_id')

        if not business_id:
            flash("Không tìm thấy doanh nghiệp của bạn.", "danger")
            return redirect(url_for('home.homepage'))
        # Kiểm tra trùng cặp productId – businessId
        existing = ProductBusiness.query.filter_by(
            productId=product_id,
            businessId=business_id
        ).first()

        if existing:
            flash("Sản phẩm này đã được doanh nghiệp bạn đăng ký bán.", "warning")
            return redirect(url_for('dashboard.create_product_business'))
        # Tạo sản phẩm doanh nghiệp bán
        product_business = ProductBusiness(
            productId=product_id,
            businessId=business_id,  # Sử dụng business_id từ session
            title=title,
            image=filename,
            unitOfMeasure=unit_of_measure,
            description=description,
            amount=amount,
            quantityInStock=quantity_in_stock,
            createdAt=datetime.utcnow(),
            updatedAt=datetime.utcnow(),
            rating = 0
        )

        db.session.add(product_business)
        db.session.commit()

        flash("Sản phẩm đã được đăng ký bán!", "success")
        return redirect(url_for('dashboard.business_dashboard'))

    return render_template('business/create_product_business.html', products=products, categories=categories)



@dashboard_bp.route('/employee')
@login_required
def employee_dashboard():
    if session.get('role') != 1:
        flash("Bạn không có quyền truy cập trang này!", "danger")
        return redirect(url_for('home.homepage'))

    employee = Employee.query.filter_by(userId=session.get('username')).first()
    if not employee:
        flash("Không tìm thấy thông tin nhân viên.", "danger")
        return redirect(url_for('home.homepage'))

    return render_template('employee/dashboard_employee.html', employee=employee)