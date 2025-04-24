from datetime import datetime
from app import create_app, db
from sqlalchemy import text

from app.models.campaign import Campaign

app = create_app()
def update_campaign_status():
    current_date = datetime.utcnow().date()

    # Lấy tất cả chiến dịch có trạng thái "Đã xác nhận" (status=1)
    campaigns = Campaign.query.filter(Campaign.status == 1).all()

    # Kiểm tra nếu chiến dịch đã đến ngày bắt đầu và chưa qua ngày kết thúc
    for campaign in campaigns:
        if campaign.registerStartDate <= current_date <= campaign.registerEndDate:
            campaign.status = 2  # Chuyển sang trạng thái "Hoạt động"
            db.session.commit()
            print(f"Chiến dịch {campaign.id} đã được chuyển sang trạng thái 'Hoạt động'.")

with app.app_context():
    try:
        db.session.execute(text('SELECT 1'))
        print("✅ Kết nối thành công tới SQL Server!")
        update_campaign_status()
    except Exception as e:
        print("❌ Kết nối thất bại:", e)

if __name__ == "__main__":
    app.run(debug=True)
