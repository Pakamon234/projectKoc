from app import db

class ProductCategory(db.Model):
    __tablename__ = 'productCategory'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(50))