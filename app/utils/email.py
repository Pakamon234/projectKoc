from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message
from flask import url_for
from app import mail

# ⚠️ Khai báo trực tiếp thay vì dùng current_app.config
SECRET_KEY = "your_secret_key_here"
SECURITY_PASSWORD_SALT = "random_salt_here"

def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(SECRET_KEY)
    return serializer.dumps(email, salt=SECURITY_PASSWORD_SALT)

def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(SECRET_KEY)
    try:
        email = serializer.loads(token, salt=SECURITY_PASSWORD_SALT, max_age=expiration)
    except:
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
    mail.send(msg)
