from flask import Blueprint, request, jsonify

from mkg.auth.auth_views.service.auth_service         import AuthService

auth_service = AuthService()

login_bp = Blueprint("login_auth", __name__)


@login_bp.route("/login", methods=["POST"])
def login():
    body = request.get_json(silent=True)
    if not body:
        return jsonify({"error": "Request body must be JSON"}), 400
 
    email    = (body.get("email")    or "").strip()
    password = (body.get("password") or "").strip()
 
    if not email or not password:
        return jsonify({"error": "email and password are required"}), 400
 
    result, error = auth_service.login(email, password)
 
    if error:
        return jsonify({"error": error}), 401
 
    return jsonify(result), 200
    