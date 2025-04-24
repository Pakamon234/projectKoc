from datetime import datetime
from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from app.models.campaign_category import CampaignCategory
from app.models.employee import Employee
from app.models.order_pro import OrderPro
from app.models.register_campaign import RegisterCampaign
from app.models.review_details import ReviewDetails
from app.models.user import User
from app.routes.auth_routes import login_required
from app import db
employee_bp = Blueprint('employee', __name__, url_prefix='/employee')

@employee_bp.route('/dashboard')
@login_required
def dashboard():
    if session.get('role') != 1:  # role 3 là nhân viên
        flash("Bạn không có quyền truy cập.", "danger")
        return redirect(url_for('home.homepage'))

    employee = Employee.query.filter_by(userId=session.get('username')).first()
    if not employee:
        flash("Không tìm thấy thông tin nhân viên.", "danger")
        return redirect(url_for('home.homepage'))

    return render_template('employee/dashboard_employee.html', employee=employee)

@employee_bp.route('/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if session.get('role') != 1:
        flash("Bạn không có quyền truy cập.", "danger")
        return redirect(url_for('home.homepage'))

    employee = Employee.query.filter_by(userId=session.get('username')).first()
    if not employee:
        flash("Không tìm thấy thông tin nhân viên.", "danger")
        return redirect(url_for('home.homepage'))

    if request.method == 'POST':
        name = request.form['name'].strip()
        phone = request.form['phoneNumber'].strip()
        address = request.form['address'].strip()
        dob = request.form['dob']
        gender = request.form['gender']

        # Kiểm tra tên
        if len(name) > 50:
            flash("Họ tên không được vượt quá 50 ký tự.", "danger")
            return redirect(url_for('employee.edit_profile'))

        # Kiểm tra số điện thoại
        if not phone.isdigit() or len(phone) != 10:
            flash("Số điện thoại phải đúng 10 chữ số.", "danger")
            return redirect(url_for('employee.edit_profile'))

        # Kiểm tra tuổi
        try:
            dob_date = datetime.strptime(dob, "%Y-%m-%d")
            age = (datetime.today() - dob_date).days // 365
            if age < 18:
                flash("Nhân viên phải từ 18 tuổi trở lên.", "danger")
                return redirect(url_for('employee.edit_profile'))
        except Exception:
            flash("Ngày sinh không hợp lệ.", "danger")
            return redirect(url_for('employee.edit_profile'))

        # Lưu
        employee.name = name
        employee.phoneNumber = phone
        employee.address = address
        employee.dob = dob_date
        employee.gender = gender
        employee.updatedAt = datetime.utcnow()

        db.session.commit()
        flash("Cập nhật thông tin thành công.", "success")
        return redirect(url_for('employee.dashboard'))

    return render_template('employee/edit_profile.html', employee=employee)


@employee_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    if session.get('role') != 1:
        flash("Không có quyền.", "danger")
        return redirect(url_for('home.homepage'))

    user = User.query.get(session['username'])
    if request.method == 'POST':
        old_pw = request.form['old_password']
        new_pw = request.form['new_password']

        if user.password.strip() != old_pw.strip():
            flash("Mật khẩu cũ không đúng.", "danger")
            return redirect(url_for('employee.change_password'))

        user.password = new_pw
        user.updatedAt = datetime.utcnow()
        db.session.commit()
        flash("Đổi mật khẩu thành công.", "success")
        return redirect(url_for('employee.dashboard'))

    return render_template('employee/change_password.html')

@employee_bp.route('/manage/employees')
@login_required
def manage_employees():
    if session.get('role') != 1:
        flash("Không có quyền truy cập.", "danger")
        return redirect(url_for('home.homepage'))

    query = Employee.query

    # Lọc theo trường: tên, email, sđt
    field = request.args.get('filter_field')
    keyword = request.args.get('keyword', '').strip()
    if field and keyword:
        if field == 'name':
            query = query.filter(Employee.name.ilike(f"%{keyword}%"))
        elif field == 'email':
            query = query.filter(Employee.email.ilike(f"%{keyword}%"))
        elif field == 'phone':
            query = query.filter(Employee.phoneNumber.ilike(f"%{keyword}%"))

    # Lọc trạng thái
    status = request.args.get('status')
    if status:
        query = query.filter(Employee.status == status)

    employees = query.order_by(Employee.createdAt.desc()).all()
    return render_template('employee/manage_employees.html', employees=employees)

from app.models.business import Business

@employee_bp.route('/manage/businesses')
@login_required
def manage_businesses():
    if session.get('role') != 1:
        flash("Không có quyền truy cập.", "danger")
        return redirect(url_for('home.homepage'))

    query = Business.query

    # Lọc theo trường: tên, email, sđt
    field = request.args.get('filter_field')
    keyword = request.args.get('keyword', '').strip()
    if field and keyword:
        if field == 'name':
            query = query.filter(Business.name.ilike(f"%{keyword}%"))
        elif field == 'email':
            query = query.filter(Business.email.ilike(f"%{keyword}%"))
        elif field == 'phone':
            query = query.filter(Business.phoneNumber.ilike(f"%{keyword}%"))

    # Lọc authenticate
    auth = request.args.get('authenticate')
    if auth in ['0', '1']:
        query = query.filter(Business.authenticate == (auth == '1'))

    # Lọc trạng thái
    status = request.args.get('status')
    if status:
        query = query.filter(Business.status == status)

    businesses = query.order_by(Business.createdAt.desc()).all()
    return render_template('employee/manage_businesses.html', businesses=businesses)
from app.models.koc import KOC

from sqlalchemy import or_

@employee_bp.route('/manage/kocs')
@login_required
def manage_kocs():
    if session.get('role') != 1:
        flash("Không có quyền truy cập.", "danger")
        return redirect(url_for('home.homepage'))

    query = KOC.query

    # Lọc theo trường: tên, email, sdt
    field = request.args.get('filter_field')
    keyword = request.args.get('keyword', '').strip()
    if field and keyword:
        if field == 'name':
            query = query.filter(KOC.name.ilike(f"%{keyword}%"))
        elif field == 'phone':
            query = query.filter(KOC.phoneNumber.ilike(f"%{keyword}%"))
        elif field == 'email':
            query = query.filter(KOC.email.ilike(f"%{keyword}%"))

    # Lọc isKoc
    isKoc = request.args.get('isKoc')
    if isKoc in ['0', '1']:
        query = query.filter(KOC.isKoc == (isKoc == '1'))

    # Lọc đã xác nhận (kocConfirmDate)
    confirmed = request.args.get('confirmed')
    if confirmed == '1':
        query = query.filter(KOC.kocConfirmDate.isnot(None))
    elif confirmed == '0':
        query = query.filter(KOC.kocConfirmDate.is_(None))

    # Lọc theo trạng thái
    status = request.args.get('status')
    if status:
        query = query.filter(KOC.status == status)

    kocs = query.order_by(KOC.createdAt.desc()).all()
    return render_template('employee/manage_kocs.html', kocs=kocs)

@employee_bp.route('/manage/kocs/<int:koc_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_koc(koc_id):
    koc = KOC.query.get_or_404(koc_id)

    if request.method == 'POST':
        name = request.form['name'].strip()
        email = request.form['email'].strip()
        phone = request.form['phoneNumber'].strip()
        gender = request.form['gender']
        address = request.form['address'].strip()
        status = request.form['status'].strip()
        confirm_date = request.form['kocConfirmDate']

        # Kiểm tra
        if len(name) > 64:
            flash("Tên không được quá 64 ký tự.", "danger")
            return redirect(url_for('employee.edit_koc', koc_id=koc_id))
        if phone and (not phone.isdigit() or len(phone) != 10):
            flash("Số điện thoại phải đúng 10 chữ số.", "danger")
            return redirect(url_for('employee.edit_koc', koc_id=koc_id))
        if email and '@' not in email:
            flash("Email không hợp lệ.", "danger")
            return redirect(url_for('employee.edit_koc', koc_id=koc_id))

        # Gán và lưu
        koc.name = name
        koc.email = email
        koc.phoneNumber = phone
        koc.gender = gender
        koc.address = address
        koc.status = status
        try:
            koc.kocConfirmDate = datetime.strptime(confirm_date, "%Y-%m-%d") if confirm_date else None
        except:
            flash("Ngày xác nhận không hợp lệ.", "danger")
            return redirect(url_for('employee.edit_koc', koc_id=koc_id))

        koc.updatedAt = datetime.utcnow()
        db.session.commit()
        flash("Đã cập nhật thông tin người tiêu dùng.", "success")
        return redirect(url_for('employee.manage_kocs'))

    return render_template('employee/edit_koc.html', koc=koc)

@employee_bp.route('/manage/kocs/<int:koc_id>/delete', methods=['POST'])
@login_required
def delete_koc(koc_id):
    koc = KOC.query.get_or_404(koc_id)
    user = User.query.filter_by(userName=koc.userId).first()

    # Kiểm tra role
    if not user or user.roleId not in [2, 3]:
        flash("Không thể xóa: KOC không có vai trò hợp lệ (chỉ role 2 hoặc 3 được phép xóa).", "danger")
        return redirect(url_for('employee.manage_kocs'))

    # Kiểm tra liên kết dữ liệu
    has_orders = OrderPro.query.filter_by(kocId=koc.id).first()
    if has_orders:
        flash("Không thể xóa: KOC đã có đơn hàng trong hệ thống.", "warning")
        return redirect(url_for('employee.manage_kocs'))

    has_reviews = ReviewDetails.query.filter_by(kocId=koc.id).first()
    if has_reviews:
        flash("Không thể xóa: KOC đã có bài review.", "warning")
        return redirect(url_for('employee.manage_kocs'))

    has_registrations = RegisterCampaign.query.filter_by(kocId=koc.id).first()
    if has_registrations:
        flash("Không thể xóa: KOC đã đăng ký chiến dịch.", "warning")
        return redirect(url_for('employee.manage_kocs'))

    # Thực hiện xóa
    db.session.delete(koc)
    if user:
        db.session.delete(user)
    db.session.commit()

    flash("Đã xóa người tiêu dùng thành công.", "success")
    return redirect(url_for('employee.manage_kocs'))
from app.models.koc import KOC

@employee_bp.route('/manage/kocs/create', methods=['GET', 'POST'])
@login_required
def create_koc():
    if session.get('role') != 1:
        flash("Bạn không có quyền truy cập chức năng này.", "danger")
        return redirect(url_for('employee.manage_kocs'))

    if request.method == 'POST':
        name = request.form['name'].strip()
        gender = request.form['gender']
        dob = request.form['dob']
        phone = request.form['phoneNumber'].strip()
        email = request.form['email'].strip()
        address = request.form['address'].strip()
        status = request.form['status'].strip()

        # Kiểm tra dữ liệu
        if len(name) > 64:
            flash("Tên không được quá 64 ký tự.", "danger")
            return redirect(url_for('employee.create_koc'))
        if phone and (not phone.isdigit() or len(phone) != 10):
            flash("Số điện thoại phải đúng 10 chữ số.", "danger")
            return redirect(url_for('employee.create_koc'))
        if email and '@' not in email:
            flash("Email không hợp lệ.", "danger")
            return redirect(url_for('employee.create_koc'))

        try:
            dob_date = datetime.strptime(dob, "%Y-%m-%d")
        except:
            flash("Ngày sinh không hợp lệ.", "danger")
            return redirect(url_for('employee.create_koc'))

        new_koc = KOC(
            name=name,
            gender=gender,
            dob=dob_date,
            phoneNumber=phone,
            email=email,
            address=address,
            isKoc = False,
            status=status,
            createdAt=datetime.utcnow(),
            updatedAt=datetime.utcnow()
        )
        db.session.add(new_koc)
        db.session.commit()
        flash("Thêm KOC thành công.", "success")
        return redirect(url_for('employee.manage_kocs'))

    return render_template('employee/create_koc.html')

@employee_bp.route('/manage/businesses/create', methods=['GET', 'POST'])
@login_required
def create_business():
    if session.get('role') != 1:
        flash("Bạn không có quyền truy cập.", "danger")
        return redirect(url_for('employee.manage_businesses'))

    if request.method == 'POST':
        name = request.form['name'].strip()
        email = request.form['email'].strip()
        phone = request.form['phoneNumber'].strip()
        address = request.form['address'].strip()
        website = request.form['website'].strip()
        status = request.form['status'].strip()

        # Kiểm tra
        if len(name) > 50:
            flash("Tên không được quá 50 ký tự.", "danger")
            return redirect(url_for('employee.create_business'))
        if not phone.isdigit() or len(phone) != 10:
            flash("Số điện thoại phải đúng 10 chữ số.", "danger")
            return redirect(url_for('employee.create_business'))
        if '@' not in email:
            flash("Email không hợp lệ.", "danger")
            return redirect(url_for('employee.create_business'))

        business = Business(
            name=name,
            email=email,
            phoneNumber=phone,
            address=address,
            website=website,
            status=status,
            authenticate = False,
            createdAt=datetime.utcnow(),
            updatedAt=datetime.utcnow()
        )
        db.session.add(business)
        db.session.commit()
        flash("Thêm doanh nghiệp thành công.", "success")
        return redirect(url_for('employee.manage_businesses'))

    return render_template('employee/create_business.html')

@employee_bp.route('/manage/businesses/<int:business_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_business(business_id):
    if session.get('role') != 1:
        flash("Bạn không có quyền truy cập.", "danger")
        return redirect(url_for('employee.manage_businesses'))

    business = Business.query.get_or_404(business_id)

    if request.method == 'POST':
        name = request.form['name'].strip()
        email = request.form['email'].strip()
        phone = request.form['phoneNumber'].strip()
        address = request.form['address'].strip()
        website = request.form['website'].strip()
        status = request.form['status'].strip()
        auth = request.form['authenticate']

        # Kiểm tra dữ liệu
        if len(name) > 50:
            flash("Tên không được quá 50 ký tự.", "danger")
            return redirect(url_for('employee.edit_business', business_id=business_id))
        if not phone.isdigit() or len(phone) != 10:
            flash("Số điện thoại phải đúng 10 chữ số.", "danger")
            return redirect(url_for('employee.edit_business', business_id=business_id))
        if '@' not in email:
            flash("Email không hợp lệ.", "danger")
            return redirect(url_for('employee.edit_business', business_id=business_id))

        # Lưu dữ liệu
        business.name = name
        business.email = email
        business.phoneNumber = phone
        business.address = address
        business.website = website
        business.status = status
        business.updatedAt = datetime.utcnow()
        business.authenticate = (auth == '1')

        db.session.commit()
        flash("Cập nhật doanh nghiệp thành công.", "success")
        return redirect(url_for('employee.manage_businesses'))

    return render_template('employee/edit_business.html', business=business)

from app.models.business import Business
from app.models.campaign import Campaign
from app.models.product_business import ProductBusiness

@employee_bp.route('/manage/businesses/<int:business_id>/delete', methods=['POST'])
@login_required
def delete_business(business_id):
    if session.get('role') != 1:
        flash("Bạn không có quyền thực hiện thao tác này.", "danger")
        return redirect(url_for('employee.manage_businesses'))

    business = Business.query.get_or_404(business_id)

    has_campaigns = Campaign.query.filter_by(businessId=business.id).first()
    if has_campaigns:
        flash("Không thể xóa: Doanh nghiệp đã tạo chiến dịch.", "warning")
        return redirect(url_for('employee.manage_businesses'))

    has_products = ProductBusiness.query.filter_by(businessId=business.id).first()
    if has_products:
        flash("Không thể xóa: Doanh nghiệp đã có sản phẩm.", "warning")
        return redirect(url_for('employee.manage_businesses'))

    # Thực hiện xóa
    db.session.delete(business)
    db.session.commit()

    flash("Đã xóa doanh nghiệp thành công.", "success")
    return redirect(url_for('employee.manage_businesses'))

@employee_bp.route('/manage/employees/create', methods=['GET', 'POST'])
@login_required
def create_employee():
    if session.get('role') != 1:
        flash("Bạn không có quyền truy cập.", "danger")
        return redirect(url_for('employee.manage_employees'))

    if request.method == 'POST':
        name = request.form['name'].strip()
        email = request.form['email'].strip()
        phone = request.form['phoneNumber'].strip()
        gender = request.form['gender']
        dob = request.form['dob']
        address = request.form['address'].strip()
        status = request.form['status'].strip()

        # Kiểm tra dữ liệu
        if len(name) > 50:
            flash("Tên không được quá 50 ký tự.", "danger")
            return redirect(url_for('employee.create_employee'))
        if not phone.isdigit() or len(phone) != 10:
            flash("Số điện thoại phải đúng 10 chữ số.", "danger")
            return redirect(url_for('employee.create_employee'))
        if '@' not in email:
            flash("Email không hợp lệ.", "danger")
            return redirect(url_for('employee.create_employee'))

        try:
            dob_date = datetime.strptime(dob, "%Y-%m-%d")
            age = (datetime.today() - dob_date).days // 365
            if age < 18:
                flash("Nhân viên phải từ 18 tuổi trở lên.", "danger")
                return redirect(url_for('employee.create_employee'))
        except:
            flash("Ngày sinh không hợp lệ.", "danger")
            return redirect(url_for('employee.create_employee'))

        new_emp = Employee(
            name=name,
            email=email,
            phoneNumber=phone,
            gender=gender,
            dob=dob_date,
            address=address,
            status=status,
            createdAt=datetime.utcnow(),
            updatedAt=datetime.utcnow()
        )
        db.session.add(new_emp)
        db.session.commit()
        flash("Thêm nhân viên thành công.", "success")
        return redirect(url_for('employee.manage_employees'))

    return render_template('employee/create_employee.html')

@employee_bp.route('/manage/employees/<int:employee_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_employee(employee_id):
    if session.get('role') != 1:
        flash("Bạn không có quyền truy cập.", "danger")
        return redirect(url_for('employee.manage_employees'))

    emp = Employee.query.get_or_404(employee_id)

    if request.method == 'POST':
        name = request.form['name'].strip()
        email = request.form['email'].strip()
        phone = request.form['phoneNumber'].strip()
        gender = request.form['gender']
        dob = request.form['dob']
        address = request.form['address'].strip()
        status = request.form['status'].strip()

        if len(name) > 50:
            flash("Tên không được quá 50 ký tự.", "danger")
            return redirect(url_for('employee.edit_employee', employee_id=employee_id))
        if not phone.isdigit() or len(phone) != 10:
            flash("Số điện thoại phải đúng 10 chữ số.", "danger")
            return redirect(url_for('employee.edit_employee', employee_id=employee_id))
        if '@' not in email:
            flash("Email không hợp lệ.", "danger")
            return redirect(url_for('employee.edit_employee', employee_id=employee_id))

        try:
            dob_date = datetime.strptime(dob, "%Y-%m-%d")
            age = (datetime.today() - dob_date).days // 365
            if age < 18:
                flash("Nhân viên phải từ 18 tuổi trở lên.", "danger")
                return redirect(url_for('employee.edit_employee', employee_id=employee_id))
        except:
            flash("Ngày sinh không hợp lệ.", "danger")
            return redirect(url_for('employee.edit_employee', employee_id=employee_id))

        emp.name = name
        emp.email = email
        emp.phoneNumber = phone
        emp.gender = gender
        emp.dob = dob_date
        emp.address = address
        emp.status = status
        emp.updatedAt = datetime.utcnow()

        db.session.commit()
        flash("Cập nhật thông tin nhân viên thành công.", "success")
        return redirect(url_for('employee.manage_employees'))

    return render_template('employee/edit_employee.html', emp=emp)

from app.models.campaign import Campaign
from app.models.employee import Employee

@employee_bp.route('/manage/employees/<int:employee_id>/delete', methods=['POST'])
@login_required
def delete_employee(employee_id):
    if session.get('role') != 1:
        flash("Bạn không có quyền thực hiện thao tác này.", "danger")
        return redirect(url_for('employee.manage_employees'))

    emp = Employee.query.get_or_404(employee_id)

    # Kiểm tra xem nhân viên đã duyệt chiến dịch nào chưa
    has_confirmed_campaign = Campaign.query.filter_by(isConfirmed=emp.id).first()
    if has_confirmed_campaign:
        flash("Không thể xóa: Nhân viên đã duyệt chiến dịch.", "warning")
        return redirect(url_for('employee.manage_employees'))

    db.session.delete(emp)
    db.session.commit()
    flash("Đã xóa nhân viên thành công.", "success")
    return redirect(url_for('employee.manage_employees'))


from app.models.campaign import Campaign
from app.models.business import Business

@employee_bp.route('/manage/campaigns')
@login_required
def manage_campaigns():
    if session.get('role') != 1:
        flash("Bạn không có quyền truy cập.", "danger")
        return redirect(url_for('home.homepage'))

    query = Campaign.query.join(Campaign.business).join(Campaign.category)

    # Tìm kiếm theo từ khóa
    field = request.args.get('filter_field')
    keyword = request.args.get('keyword', '').strip()
    if field and keyword:
        if field == 'title':
            query = query.filter(Campaign.title.ilike(f"%{keyword}%"))
        elif field == 'business':
            query = query.filter(Business.name.ilike(f"%{keyword}%"))
        elif field == 'category':
            query = query.filter(CampaignCategory.name.ilike(f"%{keyword}%"))

    # Lọc theo trạng thái
    status = request.args.get('status')
    if status in ['0', '1', '2', '3', '4', '5']:
        query = query.filter(Campaign.status == int(status))

    campaigns = query.order_by(Campaign.createdAt.desc()).all()
    return render_template('employee/manage_campaigns.html', campaigns=campaigns)


from app.models.campaign import Campaign
from app.models.campaign_product import CampaignProduct
from app.models.register_campaign import RegisterCampaign

@employee_bp.route('/manage/campaigns/<int:campaign_id>')
@login_required
def view_campaign(campaign_id):
    if session.get('role') != 1:
        flash("Không có quyền truy cập.", "danger")
        return redirect(url_for('employee.manage_campaigns'))

    campaign = Campaign.query.get_or_404(campaign_id)

    # Lấy sản phẩm của chiến dịch
    campaign_products = CampaignProduct.query.filter_by(campaignId=campaign.id).all()

    # Lấy các người tiêu dùng đã đăng ký thành công
    successful_regs = RegisterCampaign.query \
        .join(CampaignProduct, RegisterCampaign.campaign_product_id == CampaignProduct.id) \
        .filter(CampaignProduct.campaignId == campaign.id, RegisterCampaign.status == 'Thành công') \
        .all()

    return render_template('employee/campaign_detail.html',
                           campaign=campaign,
                           campaign_products=campaign_products,
                           successful_regs=successful_regs)


@employee_bp.route('/manage/campaigns/<int:campaign_id>/approve', methods=['POST'])
@login_required
def approve_campaign(campaign_id):
    if session.get('role') != 1:
        flash("Bạn không có quyền thực hiện.", "danger")
        return redirect(url_for('employee.manage_campaigns'))

    campaign = Campaign.query.get_or_404(campaign_id)

    if campaign.status not in [0,5]:
        flash("Chỉ có thể duyệt chiến dịch ở trạng thái 'Chờ xác nhận'.", "warning")
        return redirect(url_for('employee.view_campaign', campaign_id=campaign_id))

    if campaign.startDate < datetime.today().date():
        flash("Không thể duyệt chiến dịch đã quá hạn duyệt.", "danger")
        return redirect(url_for('employee.view_campaign', campaign_id=campaign_id))

    employee = Employee.query.filter_by(userId=session.get('username')).first()
    if not employee:
        flash("Không tìm thấy thông tin nhân viên.", "danger")
        return redirect(url_for('employee.view_campaign', campaign_id=campaign_id))

    # Duyệt
    campaign.status = 1
    campaign.isConfirmed = employee.id
    campaign.updatedAt = datetime.utcnow()

    db.session.commit()
    flash("Chiến dịch đã được duyệt thành công.", "success")
    return redirect(url_for('employee.view_campaign', campaign_id=campaign_id))

@employee_bp.route('/manage/campaigns/<int:campaign_id>/delete', methods=['POST'])
@login_required
def delete_campaign(campaign_id):
    if session.get('role') != 1:
        flash("Bạn không có quyền truy cập.", "danger")
        return redirect(url_for('employee.manage_campaigns'))

    campaign = Campaign.query.get_or_404(campaign_id)

    if campaign.status != 0:
        flash("Chỉ có thể xóa chiến dịch ở trạng thái 'Chờ xác nhận'.", "warning")
        return redirect(url_for('employee.view_campaign', campaign_id=campaign_id))

    if campaign.startDate <= datetime.today().date():
        flash("Không thể xóa: Chiến dịch đã bắt đầu.", "danger")
        return redirect(url_for('employee.view_campaign', campaign_id=campaign_id))

    db.session.delete(campaign)
    db.session.commit()
    flash("Đã xóa chiến dịch thành công.", "success")
    return redirect(url_for('employee.manage_campaigns'))

@employee_bp.route('/manage/campaigns/<int:campaign_id>/reject', methods=['POST'])
@login_required
def reject_campaign(campaign_id):
    if session.get('role') != 1:
        flash("Bạn không có quyền thực hiện.", "danger")
        return redirect(url_for('employee.manage_campaigns'))

    campaign = Campaign.query.get_or_404(campaign_id)

    if campaign.status not in [0, 1]:
        flash("Chỉ có thể từ chối chiến dịch đang chờ xác nhận hoặc đã xác nhận.", "warning")
        return redirect(url_for('employee.view_campaign', campaign_id=campaign_id))

    if campaign.startDate <= datetime.today().date():
        flash("Không thể từ chối chiến dịch đã bắt đầu.", "danger")
        return redirect(url_for('employee.view_campaign', campaign_id=campaign_id))

    campaign.status = 5  # Từ chối
    campaign.updatedAt = datetime.utcnow()
    db.session.commit()
    flash("Chiến dịch đã bị từ chối.", "success")
    return redirect(url_for('employee.view_campaign'))


from app.models.campaign_category import CampaignCategory

@employee_bp.route('/manage/campaign-categories')
@login_required
def manage_campaign_categories():
    if session.get('role') != 1:
        flash("Bạn không có quyền truy cập.", "danger")
        return redirect(url_for('home.homepage'))

    query = CampaignCategory.query

    keyword = request.args.get('keyword', '').strip()
    if keyword:
        query = query.filter(CampaignCategory.name.ilike(f"%{keyword}%"))

    categories = query.order_by(CampaignCategory.id).all()
    return render_template('employee/manage_campaign_categories.html', categories=categories)



@employee_bp.route('/manage/campaign-categories/create', methods=['GET', 'POST'])
@login_required
def create_campaign_category():
    if session.get('role') != 1:
        flash("Bạn không có quyền truy cập.", "danger")
        return redirect(url_for('home.homepage'))

    if request.method == 'POST':
        name = request.form['name'].strip()
        description = request.form['description'].strip()

        if len(name) > 50:
            flash("Tên loại chiến dịch không được quá 50 ký tự.", "danger")
            return redirect(url_for('employee.create_campaign_category'))

        existing = CampaignCategory.query.filter(db.func.lower(CampaignCategory.name) == name.lower()).first()
        if existing:
            flash("Tên loại chiến dịch đã tồn tại.", "warning")
            return redirect(url_for('employee.create_campaign_category'))

        new_cat = CampaignCategory(name=name, description=description)
        db.session.add(new_cat)
        db.session.commit()

        flash("Đã thêm loại chiến dịch thành công.", "success")
        return redirect(url_for('employee.manage_campaign_categories'))

    return render_template('employee/create_campaign_category.html')

@employee_bp.route('/manage/campaign-categories/<int:category_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_campaign_category(category_id):
    if session.get('role') != 1:
        flash("Bạn không có quyền truy cập.", "danger")
        return redirect(url_for('employee.manage_campaign_categories'))

    category = CampaignCategory.query.get_or_404(category_id)

    if request.method == 'POST':
        name = request.form['name'].strip()
        description = request.form['description'].strip()

        if len(name) > 50:
            flash("Tên loại chiến dịch không được quá 50 ký tự.", "danger")
            return redirect(url_for('employee.edit_campaign_category', category_id=category_id))

        # Kiểm tra trùng tên với loại khác (không phân biệt hoa/thường)
        existing = CampaignCategory.query \
            .filter(db.func.lower(CampaignCategory.name) == name.lower()) \
            .filter(CampaignCategory.id != category.id) \
            .first()
        if existing:
            flash("Tên loại chiến dịch đã tồn tại.", "warning")
            return redirect(url_for('employee.edit_campaign_category', category_id=category_id))

        category.name = name
        category.description = description
        db.session.commit()
        flash("Đã cập nhật loại chiến dịch thành công.", "success")
        return redirect(url_for('employee.manage_campaign_categories'))

    return render_template('employee/edit_campaign_category.html', category=category)

from app.models.campaign import Campaign

@employee_bp.route('/manage/campaign-categories/<int:category_id>/delete', methods=['POST'])
@login_required
def delete_campaign_category(category_id):
    if session.get('role') != 1:
        flash("Bạn không có quyền thực hiện thao tác này.", "danger")
        return redirect(url_for('employee.manage_campaign_categories'))

    category = CampaignCategory.query.get_or_404(category_id)

    # Kiểm tra xem có chiến dịch nào dùng loại này không
    used = Campaign.query.filter_by(campaignCategoryId=category.id).first()
    if used:
        flash("Không thể xóa: Đã có chiến dịch sử dụng loại này.", "warning")
        return redirect(url_for('employee.manage_campaign_categories'))

    db.session.delete(category)
    db.session.commit()
    flash("Đã xóa loại chiến dịch thành công.", "success")
    return redirect(url_for('employee.manage_campaign_categories'))


from app.models.order_detail import OrderDetail
from app.models.koc import KOC
from app.models.business import Business

from app.models.order_pro import OrderPro

@employee_bp.route('/manage/orders')
@login_required
def manage_orders():
    if session.get('role') != 1:
        flash("Không có quyền truy cập.", "danger")
        return redirect(url_for('home.homepage'))

    query = OrderPro.query.join(OrderPro.koc)

    # Lọc theo mã đơn hàng
    order_id = request.args.get('order_id')
    if order_id and order_id.isdigit():
        query = query.filter(OrderPro.id == int(order_id))

    # Lọc theo tên người đặt
    koc_name = request.args.get('koc_name', '').strip()
    if koc_name:
        query = query.filter(KOC.name.ilike(f"%{koc_name}%"))

    # Lọc theo hình thức thanh toán
    ispay = request.args.get('ispay')
    if ispay in ['0', '1']:
        query = query.filter(OrderPro.isPay == int(ispay))

    # Lọc theo trạng thái đơn
    status = request.args.get('status')
    if status:
        query = query.filter(OrderPro.orderStatus == status)

    orders = query.order_by(OrderPro.orderDate.desc()).all()
    return render_template('employee/manage_orders.html', orders=orders)



from app.models.order_pro import OrderPro
from app.models.order_detail import OrderDetail
from app.models.product_business import ProductBusiness
from app.models.product import Product

@employee_bp.route('/manage/orders/<int:order_id>')
@login_required
def view_order(order_id):
    if session.get('role') != 1:
        flash("Bạn không có quyền truy cập.", "danger")
        return redirect(url_for('employee.manage_orders'))

    order = OrderPro.query.get_or_404(order_id)

    # Lấy danh sách chi tiết đơn hàng từ OrderDetail
    order_details = OrderDetail.query.filter_by(orderId=order.id).all()

    return render_template('employee/order_detail.html', order=order, order_details=order_details)


@employee_bp.route('/manage/orders/<int:order_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_order(order_id):
    if session.get('role') != 1:
        flash("Không có quyền truy cập.", "danger")
        return redirect(url_for('employee.manage_orders'))

    order = OrderPro.query.get_or_404(order_id)

    if order.orderStatus not in ["Đang giao","Đặt thành công"]:
        flash("Chỉ có thể chỉnh sửa đơn hàng đang giao, hoặc đặt thành công", "warning")
        return redirect(url_for('employee.view_order', order_id=order.id))

    if request.method == 'POST':
        status = request.form['orderStatus']
        pay_date_str = request.form.get('payDate', '').strip()
        reason = request.form.get('reasonCancel', '').strip()

        if status not in [status,"Đơn thành công", "Đơn thất bại"]:
            flash("Trạng thái đơn hàng không hợp lệ.", "danger")
            return redirect(url_for('employee.edit_order', order_id=order.id))

        if status in ["Đơn thành công","Đặt thành công"]:
            if order.isPay == 0:
                if not pay_date_str:
                    flash("Vui lòng nhập ngày thanh toán (tiền mặt).", "warning")
                    return redirect(url_for('employee.edit_order', order_id=order.id))
            elif order.isPay == 1:
                if not pay_date_str:
                    flash("Phải nhập ngày thanh toán để xác nhận đơn online đã thanh toán.", "warning")
                    return redirect(url_for('employee.edit_order', order_id=order.id))

            try:
                pay_date = datetime.strptime(pay_date_str, "%Y-%m-%dT%H:%M")
                if pay_date < order.orderDate:
                    flash("Ngày thanh toán phải sau ngày đặt hàng.", "danger")
                    return redirect(url_for('employee.edit_order', order_id=order.id))
                order.payDate = pay_date
            except Exception:
                flash("Ngày thanh toán không hợp lệ.", "danger")
                return redirect(url_for('employee.edit_order', order_id=order.id))

            order.reasonCancel = None

        # Nếu đơn thất bại → yêu cầu lý do hủy
        elif status == "Đơn thất bại":
            if not reason:
                flash("Vui lòng nhập lý do hủy đơn.", "warning")
                return redirect(url_for('employee.edit_order', order_id=order.id))
            order.reasonCancel = reason

        # Lưu cập nhật
        order.orderStatus = status
        order.updatedAt = datetime.utcnow()
        db.session.commit()

        flash("Cập nhật đơn hàng thành công.", "success")
        return redirect(url_for('employee.view_order', order_id=order.id))

    return render_template('employee/edit_order.html', order=order)


from app.models.order_detail import OrderDetail

@employee_bp.route('/manage/orders/<int:order_id>/delete', methods=['POST'])
@login_required
def delete_order(order_id):
    if session.get('role') != 1:
        flash("Không có quyền truy cập.", "danger")
        return redirect(url_for('employee.manage_orders'))

    order = OrderPro.query.get_or_404(order_id)

    if order.orderStatus != "Chờ xác nhận":
        flash("Chỉ có thể xóa đơn hàng ở trạng thái 'Chờ xác nhận'.", "warning")
        return redirect(url_for('employee.view_order', order_id=order_id))

    # Xóa các bản ghi OrderDetail liên quan
    OrderDetail.query.filter_by(orderId=order.id).delete()

    # Xóa đơn hàng
    db.session.delete(order)
    db.session.commit()

    flash("Đã xóa đơn hàng và chi tiết đơn hàng thành công.", "success")
    return redirect(url_for('employee.manage_orders'))

from app.models.product_category import ProductCategory

@employee_bp.route('/manage/product-categories')
@login_required
def manage_product_categories():
    if session.get('role') != 1:
        flash("Không có quyền truy cập.", "danger")
        return redirect(url_for('home.homepage'))

    query = ProductCategory.query

    keyword = request.args.get('keyword', '').strip()
    if keyword:
        query = query.filter(ProductCategory.name.ilike(f"%{keyword}%"))

    categories = query.order_by(ProductCategory.id).all()
    return render_template('employee/manage_product_categories.html', categories=categories)



@employee_bp.route('/manage/product-categories/create', methods=['GET', 'POST'])
@login_required
def create_product_category():
    if session.get('role') != 1:
        flash("Không có quyền truy cập.", "danger")
        return redirect(url_for('employee.manage_product_categories'))

    if request.method == 'POST':
        name = request.form['name'].strip()

        if not name:
            flash("Tên loại sản phẩm không được để trống.", "danger")
            return redirect(url_for('employee.create_product_category'))

        # Kiểm tra trùng tên
        exists = ProductCategory.query.filter(db.func.lower(ProductCategory.name) == name.lower()).first()
        if exists:
            flash("Tên loại sản phẩm đã tồn tại.", "warning")
            return redirect(url_for('employee.create_product_category'))

        new_cat = ProductCategory(name=name)
        db.session.add(new_cat)
        db.session.commit()
        flash("Đã thêm loại sản phẩm thành công.", "success")
        return redirect(url_for('employee.manage_product_categories'))

    return render_template('employee/create_product_category.html')

@employee_bp.route('/manage/product-categories/<int:category_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_product_category(category_id):
    if session.get('role') != 1:
        flash("Không có quyền truy cập.", "danger")
        return redirect(url_for('employee.manage_product_categories'))

    category = ProductCategory.query.get_or_404(category_id)

    if request.method == 'POST':
        name = request.form['name'].strip()

        if not name:
            flash("Tên loại sản phẩm không được để trống.", "danger")
            return redirect(url_for('employee.edit_product_category', category_id=category_id))

        # Kiểm tra trùng tên
        exists = ProductCategory.query \
            .filter(db.func.lower(ProductCategory.name) == name.lower()) \
            .filter(ProductCategory.id != category.id).first()
        if exists:
            flash("Tên loại sản phẩm đã tồn tại.", "warning")
            return redirect(url_for('employee.edit_product_category', category_id=category_id))

        category.name = name
        db.session.commit()
        flash("Cập nhật thành công.", "success")
        return redirect(url_for('employee.manage_product_categories'))

    return render_template('employee/edit_product_category.html', category=category)

from app.models.pro_cate import ProCate

@employee_bp.route('/manage/product-categories/<int:category_id>/delete', methods=['POST'])
@login_required
def delete_product_category(category_id):
    if session.get('role') != 1:
        flash("Không có quyền thực hiện thao tác này.", "danger")
        return redirect(url_for('employee.manage_product_categories'))

    category = ProductCategory.query.get_or_404(category_id)

    # Kiểm tra ràng buộc: loại này đã gán cho sản phẩm chưa
    linked = ProCate.query.filter_by(productCategoryId=category.id).first()
    if linked:
        flash("Không thể xóa vì loại sản phẩm này đã được gán cho sản phẩm.", "warning")
        return redirect(url_for('employee.manage_product_categories'))

    db.session.delete(category)
    db.session.commit()
    flash("Đã xóa loại sản phẩm thành công.", "success")
    return redirect(url_for('employee.manage_product_categories'))

from app.models.product import Product
from app.models.pro_cate import ProCate
from app.models.product_category import ProductCategory

@employee_bp.route('/manage/products')
@login_required
def manage_products():
    if session.get('role') != 1:
        flash("Không có quyền truy cập.", "danger")
        return redirect(url_for('home.homepage'))

    keyword = request.args.get('keyword', '').strip()
    category_id = request.args.get('category_id')

    query = Product.query

    if keyword:
        query = query.filter(Product.name.ilike(f"%{keyword}%"))

    if category_id and category_id.isdigit():
        query = query.join(Product.categories).filter(ProductCategory.id == int(category_id))

    products = query.order_by(Product.createdAt.desc()).all()
    all_categories = ProductCategory.query.order_by(ProductCategory.name).all()

    return render_template('employee/manage_products.html',
                           products=products,
                           all_categories=all_categories)


@employee_bp.route('/manage/products/create', methods=['GET', 'POST'])
@login_required
def create_product():
    if session.get('role') != 1:
        flash("Không có quyền truy cập.", "danger")
        return redirect(url_for('employee.manage_products'))

    categories = ProductCategory.query.order_by(ProductCategory.name).all()

    if request.method == 'POST':
        name = request.form['name'].strip()
        selected_ids = list(map(int, request.form.getlist('categories')))

        if not name:
            flash("Tên sản phẩm không được để trống.", "danger")
            return redirect(url_for('employee.create_product'))

        exists = Product.query.filter(db.func.lower(Product.name) == name.lower()).first()
        if exists:
            flash("Tên sản phẩm đã tồn tại.", "warning")
            return redirect(url_for('employee.create_product'))

        selected_categories = ProductCategory.query.filter(ProductCategory.id.in_(selected_ids)).all()
        product = Product(name=name, createdAt=datetime.utcnow(), categories=selected_categories)
        db.session.add(product)
        db.session.commit()

        flash("Thêm sản phẩm thành công.", "success")
        return redirect(url_for('employee.manage_products'))

    return render_template('employee/create_product.html', categories=categories)



@employee_bp.route('/manage/products/<int:product_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_product(product_id):
    if session.get('role') != 1:
        flash("Không có quyền truy cập.", "danger")
        return redirect(url_for('employee.manage_products'))

    product = Product.query.get_or_404(product_id)
    categories = ProductCategory.query.order_by(ProductCategory.name).all()
    selected_ids = [c.id for c in product.categories]

    if request.method == 'POST':
        name = request.form['name'].strip()
        new_selected_ids = list(map(int, request.form.getlist('categories')))

        if not name:
            flash("Tên sản phẩm không được để trống.", "danger")
            return redirect(url_for('employee.edit_product', product_id=product.id))

        exists = Product.query \
            .filter(db.func.lower(Product.name) == name.lower()) \
            .filter(Product.id != product.id).first()
        if exists:
            flash("Tên sản phẩm đã tồn tại.", "warning")
            return redirect(url_for('employee.edit_product', product_id=product.id))

        new_categories = ProductCategory.query.filter(ProductCategory.id.in_(new_selected_ids)).all()
        product.name = name
        product.categories = new_categories
        product.updatedAt = datetime.utcnow()
        db.session.commit()

        flash("Cập nhật sản phẩm thành công.", "success")
        return redirect(url_for('employee.manage_products'))

    return render_template('employee/edit_product.html',
                           product=product,
                           categories=categories,
                           selected_ids=selected_ids)


from app.models.product_business import ProductBusiness
from app.models.pro_cate import ProCate

@employee_bp.route('/manage/products/<int:product_id>/delete', methods=['POST'])
@login_required
def delete_product(product_id):
    if session.get('role') != 1:
        flash("Không có quyền truy cập.", "danger")
        return redirect(url_for('employee.manage_products'))

    product = Product.query.get_or_404(product_id)

    linked = ProductBusiness.query.filter_by(productId=product.id).first()
    if linked:
        flash("Không thể xóa: sản phẩm đã gắn với doanh nghiệp.", "warning")
        return redirect(url_for('employee.manage_products'))

    product.categories.clear()  # xoá liên kết many-to-many
    db.session.delete(product)
    db.session.commit()

    flash("Đã xóa sản phẩm thành công.", "success")
    return redirect(url_for('employee.manage_products'))

from app.models.product_business import ProductBusiness
from app.models.business import Business
from app.models.product import Product

@employee_bp.route('/manage/product-businesses')
@login_required
def manage_product_businesses():
    if session.get('role') != 1:
        flash("Bạn không có quyền truy cập.", "danger")
        return redirect(url_for('home.homepage'))

    keyword = request.args.get('keyword', '').strip()
    field = request.args.get('field', '')
    sort = request.args.get('sort', '')
    query = ProductBusiness.query \
        .join(ProductBusiness.product) \
        .join(Product.categories, isouter=True) \
        .join(ProductBusiness.business)


    if keyword and field:
        like = f"%{keyword}%"
        if field == 'title':
            query = query.filter(ProductBusiness.title.ilike(like))
        elif field == 'product':
            query = query.filter(Product.name.ilike(like))
        elif field == 'category':
            query = query.filter(ProductCategory.name.ilike(like))
        elif field == 'business':
            query = query.filter(Business.name.ilike(like))


    # Sắp xếp
    if sort == 'rating_desc':
        query = query.order_by(ProductBusiness.rating.desc())
    elif sort == 'rating_asc':
        query = query.order_by(ProductBusiness.rating.asc())
    elif sort == 'newest':
        query = query.order_by(ProductBusiness.createdAt.desc())
    else:
        query = query.order_by(ProductBusiness.id.desc())

    products = query.all()

    return render_template('employee/manage_product_businesses.html', products=products)


import os
from werkzeug.utils import secure_filename

@employee_bp.route('/manage/product-businesses/<int:pb_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_product_business(pb_id):
    if session.get('role') != 1:
        flash("Không có quyền truy cập.", "danger")
        return redirect(url_for('employee.manage_product_businesses'))

    pb = ProductBusiness.query.get_or_404(pb_id)

    if request.method == 'POST':
        pb.title = request.form['title'].strip()
        pb.rating = float(request.form['rating']) if request.form['rating'] else None
        pb.unitOfMeasure = request.form['unitOfMeasure'].strip()
        pb.amount = int(request.form['amount'])
        pb.quantityInStock = int(request.form['quantityInStock'])
        pb.description = request.form['description'].strip()

        image_file = request.files['image']
        if image_file and image_file.filename:
            filename = secure_filename(image_file.filename)
            image_path = os.path.join('static/uploads', filename)
            image_file.save(image_path)
            pb.image = filename  # cập nhật ảnh mới

        pb.updatedAt = datetime.utcnow()
        db.session.commit()

        flash("Cập nhật sản phẩm doanh nghiệp thành công.", "success")
        return redirect(url_for('employee.manage_product_businesses'))

    return render_template('employee/edit_product_business.html', pb=pb)

from app.models.order_detail import OrderDetail

@employee_bp.route('/manage/product-businesses/<int:pb_id>/delete', methods=['POST'])
@login_required
def delete_product_business(pb_id):
    if session.get('role') != 1:
        flash("Không có quyền thực hiện thao tác này.", "danger")
        return redirect(url_for('employee.manage_product_businesses'))

    pb = ProductBusiness.query.get_or_404(pb_id)

    # Kiểm tra nếu sản phẩm đã có trong đơn hàng
    used = OrderDetail.query.filter_by(productId=pb.id).first()
    if used:
        flash("Không thể xóa: sản phẩm đã được sử dụng trong đơn hàng.", "warning")
        return redirect(url_for('employee.manage_product_businesses'))

    db.session.delete(pb)
    db.session.commit()
    flash("Đã xóa sản phẩm doanh nghiệp thành công.", "success")
    return redirect(url_for('employee.manage_product_businesses'))


@employee_bp.route('/manage/users')
@login_required
def manage_users():
    if session.get('role') != 1:
        flash("Bạn không có quyền truy cập.", "danger")
        return redirect(url_for('home.homepage'))

    users = User.query.order_by(User.createdAt.desc()).all()
    return render_template('employee/manage_users.html', users=users)

from app.models.user import User
from app.models.koc import KOC
from app.models.business import Business
from app.models.employee import Employee
from app.models.role import Role
from werkzeug.security import generate_password_hash

@employee_bp.route('/manage/users/create', methods=['GET', 'POST'])
@login_required
def create_user():
    if session.get('role') != 1:
        flash("Bạn không có quyền truy cập.", "danger")
        return redirect(url_for('employee.manage_users'))

    roles = Role.query.filter(Role.id.in_([1, 2, 3, 4])).all()

    # Chỉ lấy những người chưa có user
    kocs_koc = KOC.query.filter(
        KOC.userId == None,
        KOC.isKoc == True,
        KOC.kocConfirmDate != None
    ).all()

    kocs_thuong = KOC.query.filter(
        KOC.userId == None,
        db.or_(KOC.isKoc == False, KOC.kocConfirmDate == None)
    ).all()

    businesses = Business.query.filter(Business.userId == None).all()
    employees = Employee.query.filter(Employee.userId == None).all()

    if request.method == 'POST':
        role_id = int(request.form['role'])
        user_name = request.form['userName'].strip()
        password = request.form['password'].strip()
        status = request.form.get('status', 'hoạt động')
        authenticate = bool(int(request.form.get('authenticate', 0)))

        if not user_name or not password:
            flash("Vui lòng nhập đầy đủ tên đăng nhập và mật khẩu.", "danger")
            return redirect(url_for('employee.create_user'))

        exists = User.query.filter_by(userName=user_name).first()
        if exists:
            flash("Tên đăng nhập đã tồn tại.", "warning")
            return redirect(url_for('employee.create_user'))

        # hashed_password = generate_password_hash(password)
        hashed_password = password
        user = User(
            userName=user_name,
            password=hashed_password,
            roleId=role_id,
            status=status,
            authenticate=authenticate,
            createdAt=datetime.utcnow(),
            updatedAt=datetime.utcnow()
        )
        db.session.add(user)
        db.session.commit()

        # Gán userName vào bảng tương ứng
        if role_id == 1:  # Nhân viên
            employee_id = int(request.form['employee_id'])
            emp = Employee.query.get(employee_id)
            emp.userId = user.userName

        elif role_id == 2:  # KOC
            koc_id = int(request.form['koc_id'])
            koc = KOC.query.get(koc_id)
            koc.userId = user.userName

        elif role_id == 3:  # Người dùng thường
            koc_id = int(request.form['koc_id'])
            koc = KOC.query.get(koc_id)
            koc.userId = user.userName

        elif role_id == 4:  # Doanh nghiệp
            bus_id = int(request.form['business_id'])
            bus = Business.query.get(bus_id)
            bus.userId = user.userName

        db.session.commit()
        flash("Tạo tài khoản thành công.", "success")
        return redirect(url_for('employee.manage_users'))

    return render_template(
        'employee/create_user.html',
        roles=roles,
        kocs_koc=kocs_koc,
        kocs_thuong=kocs_thuong,
        businesses=businesses,
        employees=employees
    )


from werkzeug.security import generate_password_hash

@employee_bp.route('/manage/users/<user_name>/edit', methods=['GET', 'POST'])
@login_required
def edit_user(user_name):
    if session.get('role') != 1:
        flash("Bạn không có quyền chỉnh sửa tài khoản.", "danger")
        return redirect(url_for('employee.manage_users'))

    user = User.query.get_or_404(user_name)
    roles = Role.query.filter(Role.id.in_([2, 3, 4])).all()

    if request.method == 'POST':
        user.roleId = int(request.form['role'])
        user.status = request.form['status'].strip()

        user.authenticate = bool(int(request.form['authenticate']))

        password = request.form['password'].strip()
        if password:
            # user.password = generate_password_hash(password)
            user.password = password

        user.updatedAt = datetime.utcnow()
        db.session.commit()
        flash("Cập nhật tài khoản thành công.", "success")
        return redirect(url_for('employee.manage_users'))

    return render_template('employee/edit_user.html', user=user, roles=roles)

@employee_bp.route('/manage/users/<user_name>/delete', methods=['POST'])
@login_required
def delete_user(user_name):
    if session.get('role') != 1:
        flash("Không có quyền thực hiện thao tác này.", "danger")
        return redirect(url_for('employee.manage_users'))

    user = User.query.get_or_404(user_name)

    from app.models.koc import KOC
    from app.models.business import Business
    from app.models.employee import Employee

    linked = any([
        KOC.query.filter_by(userId=user.userName).first(),
        Business.query.filter_by(userId=user.userName).first(),
        Employee.query.filter_by(userId=user.userName).first()
    ])

    if linked:
        flash("Không thể xóa: tài khoản đang liên kết với người dùng trong hệ thống.", "warning")
        return redirect(url_for('employee.manage_users'))

    db.session.delete(user)
    db.session.commit()
    flash("Đã xóa tài khoản thành công.", "success")
    return redirect(url_for('employee.manage_users'))


from datetime import datetime
from flask import flash, redirect, url_for

@employee_bp.route('/manage/orders/statistics', methods=['GET', 'POST'])
@login_required
def statistics_revenue():
    if session.get('role') != 1:
        flash("Bạn không có quyền truy cập.", "danger")
        return redirect(url_for('home.homepage'))

    # Lấy tham số ngày bắt đầu và ngày kết thúc từ form
    start_date_str = request.form.get('start_date', '')
    end_date_str = request.form.get('end_date', '')

    start_date = None
    end_date = None

    # Kiểm tra và chuyển đổi ngày bắt đầu và ngày kết thúc
    if start_date_str:
        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        except ValueError:
            flash("Ngày bắt đầu không hợp lệ.", "danger")
            return redirect(url_for('employee.statistics_revenue'))

    if end_date_str:
        try:
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
        except ValueError:
            flash("Ngày kết thúc không hợp lệ.", "danger")
            return redirect(url_for('employee.statistics_revenue'))

    # Kiểm tra nếu ngày bắt đầu > ngày kết thúc
    if start_date and end_date and start_date > end_date:
        flash("Ngày bắt đầu không được lớn hơn ngày kết thúc.", "danger")
        return redirect(url_for('employee.statistics_revenue'))

    # Lọc các đơn hàng có trạng thái "Đơn thành công" và trong khoảng thời gian (nếu có)
    query = OrderPro.query.filter(OrderPro.orderStatus == "Đơn thành công")

    if start_date:
        query = query.filter(OrderPro.orderDate >= start_date)
    if end_date:
        query = query.filter(OrderPro.orderDate <= end_date)

    orders = query.all()

    # Tính tổng doanh thu
    total_revenue = sum(order.totalPrice for order in orders)

    return render_template('employee/statistics_revenue.html', orders=orders, total_revenue=total_revenue)

import pandas as pd
from flask import Response
from io import BytesIO

@employee_bp.route('/export-excel', methods=['POST'])
@login_required
def export_to_excel():
    if session.get('role') != 1:
        flash("Bạn không có quyền truy cập.", "danger")
        return redirect(url_for('home.homepage'))

    start_date_str = request.form.get('start_date', '')
    end_date_str = request.form.get('end_date', '')

    start_date = datetime.strptime(start_date_str, "%Y-%m-%d") if start_date_str else None
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d") if end_date_str else None

    # Lọc các đơn hàng có trạng thái "Đơn thành công" và trong khoảng thời gian (nếu có)
    query = OrderPro.query.filter(OrderPro.orderStatus == "Đơn thành công")

    if start_date:
        query = query.filter(OrderPro.orderDate >= start_date)
    if end_date:
        query = query.filter(OrderPro.orderDate <= end_date)

    orders = query.all()

    # Tạo DataFrame từ danh sách đơn hàng
    data = []
    for order in orders:
        data.append({
            'Mã đơn hàng': order.id,
            'Ngày đặt': order.orderDate.strftime('%d/%m/%Y'),
            'Tổng tiền': order.totalPrice,
            'Địa chỉ giao hàng': order.address,
            'Trạng thái': order.orderStatus
        })

    df = pd.DataFrame(data)

    # Chuyển đổi DataFrame thành Excel
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Doanh Thu')

    output.seek(0)

    # Trả về file Excel
    return Response(
        output,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment;filename=doanh_thu.xlsx"}
    )

