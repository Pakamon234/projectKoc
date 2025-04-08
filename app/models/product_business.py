from app import db

class ProductBusiness(db.Model):
    __tablename__ = 'productBusinees'

    productId = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key=True)
    businessId = db.Column(db.Integer, db.ForeignKey('business.id'), primary_key=True)
    title = db.Column(db.String(128))
    image = db.Column(db.String(256))
    unitOfMeasure = db.Column(db.String(10))
    description = db.Column(db.Text)
    amount = db.Column(db.Integer)
    quantityInStock = db.Column(db.Integer)
    rating = db.Column(db.Float)
    updatedAt = db.Column(db.DateTime)
    createdAt = db.Column(db.DateTime)

    product = db.relationship('Product')
    business = db.relationship('Business')