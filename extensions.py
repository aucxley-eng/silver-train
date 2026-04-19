from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

db         = SQLAlchemy()
seriliazer = Marshmallow()
migrate    = Migrate()

# Rate limiter — key on the real client IP.
# Swap get_remote_address for a custom function behind a reverse proxy.
limiter = Limiter(key_func=get_remote_address)
