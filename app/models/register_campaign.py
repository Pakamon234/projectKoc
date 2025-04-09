from app import db

class RegisterCampaign(db.Model):
    __tablename__ = 'registerCampaign'

    id = db.Column(db.Integer, primary_key=True)
    kocId = db.Column(db.Integer, db.ForeignKey('koc.id'), nullable=False)
    campaign_product_id = db.Column(db.Integer, db.ForeignKey('campaignProduct.id'), nullable=False)
    registerDate = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Unicode(50), nullable=False)
    kocCode = db.Column(db.Unicode(10))

    koc = db.relationship('KOC')
    campaign_product = db.relationship('CampaignProduct')