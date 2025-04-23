from app import db

class Campaign(db.Model):
    __tablename__ = 'campaign'

    id = db.Column(db.Integer, primary_key=True)
    businessId = db.Column(db.Integer, db.ForeignKey('business.id'), nullable=False)
    campaignCategoryId = db.Column(db.Integer, db.ForeignKey('campaignCategory.id'), nullable=False)
    title = db.Column(db.Unicode(50), nullable=False)
    thumbnail = db.Column(db.Unicode(256))
    description = db.Column(db.UnicodeText)
    startDate = db.Column(db.Date, nullable=False)
    endDate = db.Column(db.Date, nullable=False)
    registerStartDate = db.Column(db.Date, nullable=False)
    registerEndDate = db.Column(db.Date, nullable=False)
    numberOfParticipants = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer)
    createdAt = db.Column(db.DateTime)
    updatedAt = db.Column(db.DateTime)
    isConfirmed = db.Column(db.Integer, db.ForeignKey('employee.id'))

    business = db.relationship('Business')
    category = db.relationship('CampaignCategory')
    confirmed_by = db.relationship('Employee')