from datetime import datetime
from flask import Blueprint, render_template, request, session, redirect, url_for, flash
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

    campaigns = Campaign.query.order_by(Campaign.createdAt.desc()).all()
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
