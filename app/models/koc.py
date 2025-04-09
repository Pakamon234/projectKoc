from app import db

class KOC(db.Model):
    __tablename__ = 'koc'

    id = db.Column(db.Integer, primary_key=True)
    dob = db.Column(db.Date, nullable=False)
    bio = db.Column(db.Unicode(200)) 
    socialLink = db.Column(db.Unicode(256))
    name = db.Column(db.Unicode(64), nullable=False)
    gender = db.Column(db.Unicode(3), nullable=False)
    email = db.Column(db.Unicode(50))
    phoneNumber = db.Column(db.Unicode(10))
    address = db.Column(db.Unicode(50))
    picture = db.Column(db.Unicode(50))
    isKoc = db.Column(db.Boolean)
    kocConfirmDate = db.Column(db.DateTime)
    createdAt = db.Column(db.DateTime)
    updatedAt = db.Column(db.DateTime)
    userId = db.Column(db.Unicode(32), db.ForeignKey('User.userName'))
    status = db.Column(db.Unicode(50))

    user = db.relationship('User')