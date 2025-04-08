from app import db

class RoleDetails(db.Model):
    __tablename__ = 'roleDetails'

    roleId = db.Column(db.Integer, db.ForeignKey('role.id'), primary_key=True)
    functionId = db.Column(db.Integer, db.ForeignKey('roleFunction.id'), primary_key=True)

    role = db.relationship('Role')
    function = db.relationship('RoleFunction')