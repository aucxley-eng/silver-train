from flask import Blueprint

from .register_auth_route import register_bp
from .login_auth_route    import login_bp
from .log_out_route       import log_out_bp

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")

auth_bp.register_blueprint(register_bp)
auth_bp.register_blueprint(login_bp)
auth_bp.register_blueprint(log_out_bp)
