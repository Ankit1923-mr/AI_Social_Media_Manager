from flask import Blueprint, request, jsonify
from app.services.news_scraper import fetch_industry_news

news_bp = Blueprint('news', __name__)

@news_bp.route('/industry-news', methods=['POST'])
def industry_news():
    data = request.get_json()
    industry = data.get('industry')

    if not industry:
        return jsonify({'error': 'Industry field is required'}), 400

    try:
        headlines = fetch_industry_news(industry)
        return jsonify({'news': headlines}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
