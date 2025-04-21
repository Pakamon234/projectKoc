from app import db

class OrderPro(db.Model):
    __tablename__ = 'orderPro'

    id = db.Column(db.Integer, primary_key=True)
    kocId = db.Column(db.Integer, db.ForeignKey('koc.id'), nullable=False)
    orderDate = db.Column(db.DateTime, nullable=False)
    isPay = db.Column(db.Boolean, default=False)
    payDate = db.Column(db.DateTime)
    orderStatus = db.Column(db.Unicode(50))
    address = db.Column(db.Unicode(256))
    reasonCancel = db.Column(db.Unicode(64))
    totalPrice = db.Column(db.Integer, nullable=False)
    koc = db.relationship('KOC')