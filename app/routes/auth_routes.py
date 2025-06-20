from functools import wraps
from flask import Blueprint, current_app, render_template, request, redirect, session, url_for, flash
from datetime import datetime

from itsdangerous import URLSafeTimedSerializer
from app import db
from app.models.employee import Employee
from app.models.user import User
from app.models.koc import KOC
from app.models.business import Business
from app.utils.email import send_confirmation_email
auth_bp = Blueprint('auth', __name__)


# === Middleware kiểm tra nếu đã đăng nhập thì chuyển hướng ===
def redirect_if_logged_in(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' in session:
            flash("Bạn đã đăng nhập.", "info")
            return redirect(session.get('profile_url', url_for('home.homepage')))
        return f(*args, **kwargs)
    return decorated_function
# === Middleware: yêu cầu đăng nhập mới truy cập ===
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash("Vui lòng đăng nhập để tiếp tục.", "warning")
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@auth_bp.route('/register', endpoint='register')
@redirect_if_logged_in
def register_select():
    return render_template('register.html')

# ====== ĐĂNG KÝ KOC ======
@auth_bp.route('/register/koc', methods=['GET', 'POST'])
@redirect_if_logged_in
def register_koc():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        existing = User.query.get(username)
        if existing:
            flash("Tên đăng nhập đã tồn tại!", "danger")
            return redirect(url_for('auth.register_koc'))

        user = User(
            userName=username,
            password=password,
            roleId=3,
            createdAt=datetime.utcnow(),
            updatedAt=datetime.utcnow(),
            authenticate=False,
            status="Chờ"
        )
        db.session.add(user)
        db.session.flush()

        koc = KOC(
            userId=user.userName,
            name=request.form['name'],
            dob=request.form['dob'],
            gender=request.form['gender'],
            email=request.form['email'],
            phoneNumber=request.form['phoneNumber'],
            address=request.form['address'],
            # socialLink=request.form['socialLink'],
            createdAt=datetime.utcnow(),
            updatedAt=datetime.utcnow(),
            status="còn"
        )
        db.session.add(koc)
        db.session.commit()

        # Gửi email xác thực
        if koc.email:
            send_confirmation_email(koc.email)
            flash("Đăng ký thành công! Vui lòng kiểm tra email để xác thực tài khoản.", "info")
        else:
            flash("Đăng ký thành công! Không có email để xác thực.", "warning")

        return redirect(url_for('auth.login'))

    return render_template('register_koc.html')

# ====== ĐĂNG KÝ DOANH NGHIỆP ======
@auth_bp.route('/register/business', methods=['GET', 'POST'])
@redirect_if_logged_in
def register_business():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        existing = User.query.get(username)
        if existing:
            flash("Tên đăng nhập đã tồn tại!", "danger")
            return redirect(url_for('auth.register_business'))

        user = User(
            userName=username,
            password=password,
            roleId=4,  # giả sử 2 là role Business
            createdAt=datetime.utcnow(),
            updatedAt=datetime.utcnow(),
            authenticate=False,
            status="chờ"
        )
        db.session.add(user)
        db.session.flush()

        business = Business(
            userId=user.userName,
            name=request.form['name'],
            email=request.form['email'],
            phoneNumber=request.form['phoneNumber'],
            address=request.form['address'],
            website=request.form['website'],
            createdAt=datetime.utcnow(),
            updatedAt=datetime.utcnow(),
            authenticate=False,
            status="pending"
        )
        db.session.add(business)
        db.session.commit()
        # Gửi email xác thực
        if business.email:
            send_confirmation_email(business.email)
            flash("Đăng ký thành công! Vui lòng kiểm tra email để xác thực tài khoản.", "info")
        else:
            flash("Đăng ký thành công! Không có email để xác thực.", "warning")

        return redirect(url_for('auth.login'))

    return render_template('register_business.html')

from app.utils.email import confirm_token

from app.models.koc import KOC
from app.models.user import User

@auth_bp.route('/confirm-email')
def confirm_email():
    token = request.args.get('token')
    email = confirm_token(token)

    if not email:
        flash("Liên kết không hợp lệ hoặc đã hết hạn!", "danger")
        return redirect(url_for('auth.login'))

    koc = KOC.query.filter_by(email=email).first()
    business = Business.query.filter_by(email=email).first()
    
    

    if not koc and not business:
        flash("Không tìm thấy người dùng với email này.", "danger")
        return redirect(url_for('auth.login'))

    user = koc.user if koc else business.user
    print(f"[DEBUG] Tìm thấy user từ email: {user.userName if user else 'None'}")
    if user and not user.authenticate:
        user.authenticate = True
        user.status = 'hoạt động'
        db.session.commit()
        flash("✅ Tài khoản đã được xác thực thành công!", "success")
    else:
        flash("Tài khoản đã xác thực hoặc không hợp lệ.", "info")

    return redirect(url_for('auth.login'))

@auth_bp.route('/login', methods=['GET', 'POST'])
@redirect_if_logged_in
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(userName=username, password=password).first()

        if user:
            if not user.authenticate:
                flash("Tài khoản chưa xác thực email!", "warning")
                return redirect(url_for('auth.login'))
            if user.status == 'ngừng':
                flash("Tài khoản đã ngừng hoạt động!", "warning")
                return redirect(url_for('auth.login'))

            session['username'] = user.userName
            session['role'] = user.roleId

            # Lấy thêm thông tin ID từ bảng tương ứng theo role
            if user.roleId == 2 or user.roleId == 3:  # KOC
                koc = KOC.query.filter_by(userId=user.userName).first()
                session['profile_id'] = koc.id if koc else None
                session['profile_url'] = url_for('dashboard.koc_dashboard')

            elif user.roleId == 4:  # Doanh nghiệp
                business = Business.query.filter_by(userId=user.userName).first()
                session['profile_id'] = business.id if business else None
                session['profile_url'] = url_for('dashboard.business_dashboard')

            elif user.roleId == 1:  # Nhân viên
                employee = Employee.query.filter_by(userId=user.userName).first()
                session['profile_id'] = employee.id if employee else None
                session['profile_url'] = url_for('dashboard.employee_dashboard')

            flash("Đăng nhập thành công!", "success")
            return redirect(url_for('home.homepage'))

        flash("Sai tên đăng nhập hoặc mật khẩu!", "danger")
        return redirect(url_for('auth.login'))

    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    session.clear()
    flash("Bạn đã đăng xuất.", "info")
    return redirect(url_for('auth.login'))