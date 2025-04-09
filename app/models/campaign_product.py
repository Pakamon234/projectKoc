from app import db

class CampaignProduct(db.Model):
    __tablename__ = 'campaignProduct'

    id = db.Column(db.Integer, primary_key=True)
    campaignId = db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable=False)
    productId = db.Column(db.Integer, db.ForeignKey('productBusinees.id'), nullable=False)  # Correctly referencing productBusinees
    commission = db.Column(db.Float, nullable=False)

    campaign = db.relationship('Campaign')  # Assuming you have a 'Campaign' model
    productBusinees = db.relationship('ProductBusiness')  # Reference to the 'ProductBusiness' model
