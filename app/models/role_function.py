from app import db

class RoleFunction(db.Model):
    __tablename__ = 'roleFunction'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(50))