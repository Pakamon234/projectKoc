from app import db

class ReviewDetails(db.Model):
    __tablename__ = 'reviewDetails'

    reviewId = db.Column(db.Integer, db.ForeignKey('Reviews.id'), primary_key=True)
    kocId = db.Column(db.Integer, db.ForeignKey('koc.id'), primary_key=True)
    text = db.Column(db.UnicodeText)
    rating = db.Column(db.Integer)

    koc = db.relationship('KOC')
    review = db.relationship('Reviews')