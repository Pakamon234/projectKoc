from app import db

class Business(db.Model):
    __tablename__ = 'business'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(50), nullable=False)
    address = db.Column(db.Unicode(50), nullable=False)
    email = db.Column(db.Unicode(50), nullable=False)
    phoneNumber = db.Column(db.Unicode(10), nullable=False)
    website = db.Column(db.Unicode(256))
    authenticate = db.Column(db.Boolean)
    createdAt = db.Column(db.DateTime)
    updatedAt = db.Column(db.DateTime)
    userId = db.Column(db.Unicode(32), db.ForeignKey('User.userName'))
    status = db.Column(db.Unicode(50))

    user = db.relationship('User')