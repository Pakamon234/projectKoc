from app import db

class Commission(db.Model):
    __tablename__ = 'commission'

    id = db.Column(db.Integer, primary_key=True)
    registerId = db.Column(db.Integer, db.ForeignKey('registerCampaign.id'), nullable=False)
    quantity = db.Column(db.Integer)
    amount = db.Column(db.Integer)
    totalAmount = db.Column(db.Integer)
    commissionMoney = db.Column(db.Float)
    isDone = db.Column(db.Boolean)

    register = db.relationship('RegisterCampaign')