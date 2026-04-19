from flask import Blueprint, request, jsonify

from mkg.auth.auth_views.service.auth_service         import AuthService

auth_service = AuthService()

log_out_bp = Blueprint("log_out_auth", __name__)

@log_out_bp.route("/logout", methods=["POST"])
# @require_role("guest", "member", "admin")   # any authenticated role
def logout():
    raw_token = request.headers.get("Authorization", "").split(" ", 1)[-1]
    error     = auth_service.logout(raw_token)
 
    if error:
        return jsonify({"error": error}), 400
 
    return jsonify({"message": "Logged out successfully"}), 200
