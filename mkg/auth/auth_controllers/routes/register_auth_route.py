from flask                                            import Blueprint, request, jsonify

from mkg.auth.auth_views.service.auth_service         import AuthService


auth_service = AuthService()

register_bp = Blueprint("register_auth", __name__)


@register_bp.route("/register", methods=["POST"])
def register_a_new_user_record():
    body = request.get_json(silent=True)
    if not body:
        return jsonify({"error": "Request body must be JSON"}), 400
 
    member, errors = auth_service.register(body)
 
    if errors:
        return jsonify({"error": "Validation failed", "detail": errors}), 422
 
    return jsonify({"message": "Registration successful", "member": member}), 201
    