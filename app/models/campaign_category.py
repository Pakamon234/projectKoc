from app import db

class CampaignCategory(db.Model):
    __tablename__ = 'campaignCategory'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(50))