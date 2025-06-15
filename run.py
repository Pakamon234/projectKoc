from datetime import datetime
from app import create_app, db
from sqlalchemy import text

from app.models.campaign import Campaign

app = create_app()

with app.app_context():
    try:
        db.session.execute(text('SELECT 1'))
        print("✅ Kết nối thành công tới SQL Server!")
    except Exception as e:
        print("❌ Kết nối thất bại:", e)

if __name__ == "__main__":
    app.run(debug=True)
