from app import db

class Employee(db.Model):
    __tablename__ = 'employee'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(3), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(50), nullable=False)
    phoneNumber = db.Column(db.String(10), nullable=False)
    picture = db.Column(db.String(250))
    userId = db.Column(db.String(32), db.ForeignKey('User.userName'))
    status = db.Column(db.String(50))
    updatedAt = db.Column(db.DateTime)
    createdAt = db.Column(db.DateTime)

    user = db.relationship('User')