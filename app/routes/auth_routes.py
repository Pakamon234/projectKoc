from flask import Blueprint, current_app, render_template, request, redirect, url_for, flash
from datetime import datetime

from itsdangerous import URLSafeTimedSerializer
from app import db
from app.models.user import User
from app.models.koc import KOC
from app.models.business import Business
from app.utils.email import send_confirmation_email
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register')
def register_select():
    return render_template('register.html')

# ====== ĐĂNG KÝ KOC ======
@auth_bp.route('/register/koc', methods=['GET', 'POST'])
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
            socialLink=request.form['socialLink'],
            createdAt=datetime.utcnow(),
            updatedAt=datetime.utcnow(),
            status="Chờ"
        )
        db.session.add(koc)
        db.session.commit()

        # Gửi email xác thực
        if koc.email:
            send_confirmation_email(koc.email)
            flash("Đăng ký thành công! Vui lòng kiểm tra email để xác thực tài khoản.", "info")
        else:
            flash("Đăng ký thành công! Không có email để xác thực.", "warning")

        # return redirect(url_for('auth.login'))

    return render_template('register_koc.html')

# ====== ĐĂNG KÝ DOANH NGHIỆP ======
@auth_bp.route('/register/business', methods=['GET', 'POST'])
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
            roleId=2,  # giả sử 2 là role Business
            createdAt=datetime.utcnow(),
            updatedAt=datetime.utcnow(),
            authenticate=False,
            status="pending"
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

        # return redirect(url_for('auth.login'))

        flash("Đăng ký doanh nghiệp thành công! Vui lòng đăng nhập.", "success")
        return redirect(url_for('auth.login'))

    return render_template('register_business.html')

from app.utils.email import confirm_token

from app.models.koc import KOC
from app.models.user import User

@auth_bp.route('/confirm-email')
def confirm_email():
    token = request.args.get('token')

    email = confirm_token(token)  # hàm này trả ra địa chỉ email từ token

    if not email:
        flash("Liên kết không hợp lệ hoặc đã hết hạn!", "danger")
        return redirect(url_for('auth.login'))

    # Tìm theo email từ bảng KOC
    koc = KOC.query.filter_by(email=email).first()
    if not koc:
        flash("Không tìm thấy KOC với email này.", "danger")
        # Tìm theo email từ bảng KOC
    koc = Business.query.filter_by(email=email).first()
    if not koc:
        flash("Không tìm thấy Business với email này.", "danger")   

    # Lấy user gắn với KOC
    user = koc.user
    if user and not user.authenticate:
        user.authenticate = True
        db.session.commit()
        flash("✅ Tài khoản đã được xác thực thành công!", "success")
    else:
        flash("Tài khoản đã xác thực hoặc không hợp lệ.", "info")

    return redirect(url_for('auth.login'))
