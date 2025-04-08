from app import db

class Role(db.Model):
    __tablename__ = 'role'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(50))

    users = db.relationship('User', back_populates='role', cascade='all, delete')