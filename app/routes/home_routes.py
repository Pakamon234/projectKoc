from flask import Blueprint, render_template
from app.models.campaign import Campaign
home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def homepage():
    return render_template('home.html')

@home_bp.route('/campaigns')
def campaign_list():
    campaigns = Campaign.query.filter(Campaign.status.in_([1, 2, 3])).order_by(Campaign.createdAt.desc()).all()
    return render_template('campaigns/list_campaigns.html', campaigns=campaigns)
