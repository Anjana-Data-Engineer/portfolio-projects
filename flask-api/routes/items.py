# routes/items.py
from flask import Blueprint, request, jsonify
from models import Item
from extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity

items_bp = Blueprint("items", __name__)

@items_bp.route("", methods=["GET"])
@jwt_required()
def list_items():
    items = Item.query.order_by(Item.created_at.desc()).all()
    return jsonify([i.to_dict() for i in items]), 200

@items_bp.route("/<int:item_id>", methods=["GET"])
@jwt_required()
def get_item(item_id):
    it = Item.query.get_or_404(item_id)
    return jsonify(it.to_dict()), 200

@items_bp.route("", methods=["POST"])
@jwt_required()
def create_item():
    payload = request.get_json() or {}
    name = payload.get("name")
    if not name:
        return jsonify({"msg": "name required"}), 400
    it = Item(name=name, description=payload.get("description"), value=payload.get("value"))
    db.session.add(it)
    db.session.commit()
    return jsonify(it.to_dict()), 201

@items_bp.route("/<int:item_id>", methods=["PUT"])
@jwt_required()
def update_item(item_id):
    payload = request.get_json() or {}
    it = Item.query.get_or_404(item_id)
    it.name = payload.get("name", it.name)
    it.description = payload.get("description", it.description)
    it.value = payload.get("value", it.value)
    db.session.commit()
    return jsonify(it.to_dict()), 200

@items_bp.route("/<int:item_id>", methods=["DELETE"])
@jwt_required()
def delete_item(item_id):
    it = Item.query.get_or_404(item_id)
    db.session.delete(it)
    db.session.commit()
    return jsonify({"msg": "deleted"}), 200
