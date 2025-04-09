from app import db

class OrderDetail(db.Model):
    __tablename__ = 'orderDetail'

    orderId = db.Column(db.Integer, db.ForeignKey('orderPro.id'), primary_key=True)
    productId = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    amountPerOne = db.Column(db.Integer, nullable=False)
    TotalAmount = db.Column(db.Integer, nullable=False)
    kocCode = db.Column(db.Unicode(10))
    rating = db.Column(db.Integer)
    comment = db.Column(db.Text)

    order = db.relationship('OrderPro')
    product = db.relationship('Product')