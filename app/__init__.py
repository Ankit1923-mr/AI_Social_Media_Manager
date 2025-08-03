from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Register blueprints
    from app.routes.business import business_bp
    from app.routes.news import news_bp
    from app.routes.content import content_bp
    # from app.routes.planner import planner_bp
    # from app.routes.post_manager import post_bp
    # from app.routes.facebook import fb_bp

    app.register_blueprint(business_bp, url_prefix="/api/business")
    app.register_blueprint(news_bp, url_prefix="/api/news")
    app.register_blueprint(content_bp, url_prefix="/api/content")
    # app.register_blueprint(planner_bp, url_prefix="/api/plan")
    # app.register_blueprint(post_bp, url_prefix="/api/posts")
    # app.register_blueprint(fb_bp, url_prefix="/api/facebook")

    return app
