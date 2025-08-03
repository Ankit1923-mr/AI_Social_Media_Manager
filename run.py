from flask import Flask
from flask_cors import CORS

from app.routes.business import business_bp
from app.routes.news import news_bp
from app.routes.content import content_bp
from app.routes.planner import planner_bp
from app.routes.facebook import facebook_bp


def create_app():
    app = Flask(__name__)
    # Enable CORS - adjust origins for production if needed
    CORS(app)

    # Register Blueprints
    app.register_blueprint(business_bp, url_prefix="/api/business")
    app.register_blueprint(news_bp, url_prefix="/api/news")
    app.register_blueprint(content_bp, url_prefix="/api/content")
    app.register_blueprint(planner_bp, url_prefix="/api/weekly-planner")
    app.register_blueprint(facebook_bp, url_prefix="/api/facebook")

    return app


if __name__ == "__main__":
    app = create_app()
    # Run on all IPs for local network testing, default port 5000
    app.run(host="0.0.0.0", port=5000, debug=True)
