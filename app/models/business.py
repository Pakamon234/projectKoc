from app import db

class Business(db.Model):
    __tablename__ = 'business'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    phoneNumber = db.Column(db.String(10), nullable=False)
    website = db.Column(db.String(256))
    authenticate = db.Column(db.Boolean)
    createdAt = db.Column(db.DateTime)
    updatedAt = db.Column(db.DateTime)
    userId = db.Column(db.String(32), db.ForeignKey('User.userName'))
    status = db.Column(db.String(50))

    user = db.relationship('User')