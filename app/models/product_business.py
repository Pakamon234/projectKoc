from app import db

class ProductBusiness(db.Model):
    __tablename__ = 'productBusinees'
    id = db.Column(db.Integer, primary_key=True)
    productId = db.Column(db.Integer, db.ForeignKey('product.id'))
    businessId = db.Column(db.Integer, db.ForeignKey('business.id'))
    title = db.Column(db.Unicode(128))
    image = db.Column(db.Unicode(256))
    unitOfMeasure = db.Column(db.Unicode(10))
    description = db.Column(db.UnicodeText)
    amount = db.Column(db.Integer)
    quantityInStock = db.Column(db.Integer)
    rating = db.Column(db.Float)
    updatedAt = db.Column(db.DateTime)
    createdAt = db.Column(db.DateTime)

    product = db.relationship('Product')
    business = db.relationship('Business')