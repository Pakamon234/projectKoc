
from datetime import datetime
from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from app.models import campaign
from app.models.campaign import Campaign
from app.models.campaign_category import CampaignCategory
from app.models.campaign_product import CampaignProduct
from app.models.koc import KOC
from app.models.product import Product
from app.models.register_campaign import RegisterCampaign
from app.routes.auth_routes import login_required
from app import db
home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def homepage():
    return render_template('home.html')

@home_bp.route('/campaigns')
def campaign_list():
    campaigns = Campaign.query.filter(Campaign.status.in_([1, 2, 3])) \
        .order_by(Campaign.createdAt.desc()).all()

    campaign_products_map = {}  # Lưu trữ sản phẩm cho từng chiến dịch
    for campaign in campaigns:
        campaign_products = CampaignProduct.query.filter_by(campaignId=campaign.id).all()
        campaign_products_map[campaign.id] = campaign_products

    return render_template('campaigns/list_campaigns.html', campaigns=campaigns, campaign_products_map=campaign_products_map)

@home_bp.route('/campaigns/register/<int:campaign_id>', methods=['GET', 'POST'])
@login_required
def register_campaign(campaign_id):
    # Kiểm tra role, chỉ cho phép KOC đăng ký
    if session.get('role') != 2:
        flash("Bạn không có quyền đăng ký chiến dịch này.", "danger")
        return redirect(url_for('home.campaign_list'))

    # Lấy thông tin chiến dịch
    campaign = Campaign.query.get_or_404(campaign_id)

    # Kiểm tra xem chiến dịch có nằm trong thời gian đăng ký không
    current_date = datetime.utcnow().date()
    if not (campaign.registerStartDate <= current_date <= campaign.registerEndDate):
        flash("Không thể đăng ký chiến dịch này, thời gian đăng ký đã hết.", "warning")
        return redirect(url_for('home.campaign_list'))

    # Lấy danh sách các sản phẩm của chiến dịch
    campaign_products = CampaignProduct.query.filter_by(campaignId=campaign.id).all()

    if request.method == 'POST':
        product_ids = request.form.getlist('product_ids')

        if not product_ids:
            flash("Vui lòng chọn ít nhất một sản phẩm để đăng ký.", "warning")
            return redirect(url_for('home.register_campaign', campaign_id=campaign.id))

        # Kiểm tra người dùng đã đăng ký chiến dịch này chưa (cho từng sản phẩm)
        for product_id in product_ids:
            existing_registration = RegisterCampaign.query.filter_by(kocId=session.get('profile_id'),
                                                                     campaign_product_id=product_id).first()
            if existing_registration:
                flash("Bạn đã đăng ký sản phẩm này rồi.", "warning")
                return redirect(url_for('home.campaign_list'))

            # Tạo bản ghi đăng ký mới cho mỗi sản phẩm
            new_registration = RegisterCampaign(
                kocId=session.get('profile_id'),
                campaign_product_id=product_id,
                registerDate=datetime.utcnow(),
                status='Chờ duyệt'
            )

            db.session.add(new_registration)

        db.session.commit()

        flash("Đăng ký chiến dịch thành công.", "success")
        return redirect(url_for('home.campaign_list'))

    return render_template('campaigns/register_campaign.html', campaign=campaign, campaign_products=campaign_products)

from app.models.reviews import Reviews
from app.models.product_business import ProductBusiness
from app.models.register_campaign import RegisterCampaign
from app.models.product_category import ProductCategory

@home_bp.route('/product-reviews')
def public_reviews():
    # Lấy dữ liệu lọc từ URL
    filter_by = request.args.get('filter_by')
    filter_value = request.args.get('filter_value', '').strip().lower()
    sort_by = request.args.get('sort_by')

    query = (
        Reviews.query
        .join(Reviews.register)
        .join(RegisterCampaign.campaign_product)
        .join(CampaignProduct.productBusinees)
        .join(CampaignProduct.campaign)
        .join(RegisterCampaign.koc)
    )

    # Áp dụng bộ lọc
    if filter_by and filter_value:
        if filter_by == 'campaign':
            query = query.filter(Campaign.title.ilike(f"%{filter_value}%"))
        elif filter_by == 'product':
            query = query.filter(ProductBusiness.title.ilike(f"%{filter_value}%"))
        elif filter_by == 'campaign_category':
            query = query.join(Campaign.category).filter(CampaignCategory.name.ilike(f"%{filter_value}%"))
        elif filter_by == 'product_category':
            query = query.join(ProductBusiness.product).join(Product.categories).filter(ProductCategory.name.ilike(f"%{filter_value}%"))
        elif filter_by == 'koc':
            query = query.filter(KOC.name.ilike(f"%{filter_value}%"))

    # Sắp xếp
    if sort_by == 'rating_asc':
        query = query.order_by(Reviews.rating.asc())
    elif sort_by == 'rating_desc':
        query = query.order_by(Reviews.rating.desc())
    else:
        query = query.order_by(Reviews.updatedAt.desc())

    reviews = query.all()
    categories = ProductCategory.query.all()

    return render_template('home/product_reviews.html', reviews=reviews, categories=categories)

from app.models.reviews import Reviews
from app.models.review_details import ReviewDetails
from app.models.koc import KOC
from flask import request, session, redirect, render_template, url_for, flash
from datetime import datetime

@home_bp.route('/product-reviews/<int:review_id>', methods=['GET', 'POST'])
def review_description(review_id):
    review = Reviews.query.get_or_404(review_id)
    comments = ReviewDetails.query.filter_by(reviewId=review.id).all()

    # Nếu là POST (gửi bình luận)
    if request.method == 'POST':
        if 'profile_id' not in session or session.get('role') not in[ 2,3]:
            flash("Bạn cần đăng nhập bằng tài khoản người dùng để bình luận.", "warning")
            return redirect(url_for('home.review_description', review_id=review_id))

        text = request.form.get('text')
        rating = int(request.form.get('rating') or 0)
        koc_id = session['profile_id']

        # Kiểm tra nếu đã bình luận thì cập nhật, nếu chưa thì thêm mới
        existing = ReviewDetails.query.filter_by(reviewId=review.id, kocId=koc_id).first()
        if existing:
            existing.text = text
            existing.rating = rating
            flash("Cập nhật bình luận thành công!", "success")
        else:
            new_cmt = ReviewDetails(
                reviewId=review.id,
                kocId=koc_id,
                text=text,
                rating=rating
            )
            db.session.add(new_cmt)
            flash("Bình luận đã được gửi!", "success")

        db.session.commit()
        return redirect(url_for('home.review_description', review_id=review.id))

    return render_template('home/review_des.html', review=review, comments=comments)

