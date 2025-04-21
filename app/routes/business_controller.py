from datetime import datetime
from flask import Blueprint, render_template, request, session, redirect, url_for, flash
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

    # Chuyển sang template chính của dashboard (dashboard_business.html)
    return render_template('dashboard_business.html', business=business)

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

        if user.password != old_password:
            flash("Mật khẩu cũ không đúng.", "danger")
            return redirect(url_for('business.change_password'))

        user.password = new_password
        user.updatedAt = datetime.utcnow()
        db.session.commit()
        flash("Đổi mật khẩu thành công.", "success")
        return redirect(url_for('business.view_profile'))

    return render_template('business/change_password.html')
