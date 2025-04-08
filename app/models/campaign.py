from app import db

class Campaign(db.Model):
    __tablename__ = 'campaign'

    id = db.Column(db.Integer, primary_key=True)
    businessId = db.Column(db.Integer, db.ForeignKey('business.id'), nullable=False)
    campaignCategoryId = db.Column(db.Integer, db.ForeignKey('campaignCategory.id'), nullable=False)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(50))
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