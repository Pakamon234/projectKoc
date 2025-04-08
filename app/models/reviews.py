from app import db

class Reviews(db.Model):
    __tablename__ = 'Reviews'

    id = db.Column(db.Integer, primary_key=True)
    registerId = db.Column(db.Integer, db.ForeignKey('registerCampaign.id'), nullable=False)
    rating = db.Column(db.Float)
    text = db.Column(db.Text, nullable=False)
    createdAt = db.Column(db.DateTime)
    updatedAt = db.Column(db.DateTime)

    register = db.relationship('RegisterCampaign')