# routes/auth.py
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
from extensions import db
from flask_jwt_extended import create_access_token
from datetime import timedelta

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    payload = request.get_json() or {}
    username = payload.get("username")
    password = payload.get("password")
    if not username or not password:
        return jsonify({"msg": "username and password required"}), 400
    if User.query.filter_by(username=username).first():
        return jsonify({"msg": "username taken"}), 400
    hashed = generate_password_hash(password)
    user = User(username=username, password=hashed)
    db.session.add(user)
    db.session.commit()
    return jsonify({"msg": "registered", "user": {"id": user.id, "username": user.username}}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    payload = request.get_json() or {}
    username = payload.get("username")
    password = payload.get("password")
    if not username or not password:
        return jsonify({"msg": "username and password required"}), 400
    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"msg": "bad username or password"}), 401
    access_token = create_access_token(identity=user.id, expires_delta=timedelta(hours=8))
    return jsonify(access_token=access_token), 200
