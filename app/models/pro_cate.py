from app import db

class ProCate(db.Model):
    __tablename__ = 'proCate'

    productId = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key=True)
    productCategoryId = db.Column(db.Integer, db.ForeignKey('productCategory.id'), primary_key=True)

    product = db.relationship('Product')
    category = db.relationship('ProductCategory')