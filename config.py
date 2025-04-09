import urllib

class Config:
    DRIVER = 'ODBC Driver 17 for SQL Server'
    SERVER = r'MSIKatana\SERVERM'
    DATABASE = 'KOC'
    USERNAME = 'sa'
    PASSWORD = 'long091103'

    # CHỈ sửa dòng này:
    CONNECTION_STRING = (
        f'DRIVER={DRIVER};SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD};TrustServerCertificate=yes'
    )

    SQLALCHEMY_DATABASE_URI = 'mssql+pyodbc:///?odbc_connect=' + urllib.parse.quote_plus(CONNECTION_STRING)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'tgddtn05111@gmail.com'
    MAIL_PASSWORD = 'lgqi unxq vozg vgnw'  # dùng App Password nếu Gmail
    MAIL_DEFAULT_SENDER = 'tgddtn05111@gmail.com'
    SECRET_KEY = 'your_secret_key'
    SECURITY_PASSWORD_SALT = 'some_random_salt'
