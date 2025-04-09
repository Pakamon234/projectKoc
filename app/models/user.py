from app import db

class User(db.Model):
    __tablename__ = 'User'

    userName = db.Column(db.Unicode(32), primary_key=True)
    password = db.Column(db.Unicode(64), nullable=False)
    roleId = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    createdAt = db.Column(db.DateTime, nullable=False)
    updatedAt = db.Column(db.DateTime, nullable=False)
    authenticate = db.Column(db.Boolean, default=False)
    status = db.Column(db.Unicode(50))

    role = db.relationship('Role', back_populates='users')