# app.py
from flask import Flask, jsonify
from config import Config
from extensions import db, migrate, jwt
from routes import api_bp
from routes.auth import auth_bp
from routes.items import items_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # init extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # register blueprints
    app.register_blueprint(api_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(items_bp, url_prefix="/api/items")

    @app.route("/")
    def index():
        return jsonify({"msg": "Flask Backend API Service running"}), 200

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=int(__import__("os").environ.get("PORT", 8000)))
