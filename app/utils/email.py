from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message
from flask import url_for, current_app
from app import mail

def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=current_app.config['SECURITY_PASSWORD_SALT'])

def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, salt=current_app.config['SECURITY_PASSWORD_SALT'], max_age=expiration)
    except Exception as e:
        print(f"[DEBUG] Token invalid: {e}")
        return False
    return email

def send_confirmation_email(to_email):
    token = generate_confirmation_token(to_email)
    confirm_url = url_for('auth.confirm_email', token=token, _external=True)

    html = f'''
        <p>Chào bạn,</p>
        <p>Vui lòng xác nhận đăng ký tài khoản bằng cách click vào liên kết bên dưới:</p>
        <a href="{confirm_url}">{confirm_url}</a>
        <p>Liên kết sẽ hết hiệu lực sau 1 giờ.</p>
    '''

    msg = Message('Xác nhận đăng ký KOC', recipients=[to_email], html=html)
    print(f"[DEBUG] Sending confirmation link to {to_email}: {confirm_url}")
    mail.send(msg)
