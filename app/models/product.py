from app import db

class Product(db.Model):
    __tablename__ = 'product'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(50), nullable=False)
    createdAt = db.Column(db.DateTime)
    updatedAt = db.Column(db.DateTime)
    # ✅ SỬA file product.py:
    categories = db.relationship('ProductCategory',
                                secondary='proCate',
                                backref='products')  # giữ ở đây
