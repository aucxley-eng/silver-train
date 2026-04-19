import os


class Config:
    # ── Database ──────────────────────────────────────────────────
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///library.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ── Security ──────────────────────────────────────────────────
    # Generate a strong secret in production:  python -c "import secrets; print(secrets.token_hex(32))"
    SECRET_KEY = os.getenv("SECRET_KEY", "change-me-in-production")
    TOKEN_EXPIRY_SECONDS = int(os.getenv("TOKEN_EXPIRY_SECONDS", 3600))   # 1 hour

    # ── Rate limiting ─────────────────────────────────────────────
    # Stored in memory for dev; swap to "redis://..." in prod.
    RATELIMIT_STORAGE_URI = os.getenv("RATELIMIT_STORAGE_URI", "memory://")
    RATELIMIT_DEFAULT = "200 per day;50 per hour"
    RATELIMIT_HEADERS_ENABLED = True     # X-RateLimit-* headers in every response


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = False              # set True to log every SQL statement


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    RATELIMIT_ENABLED = False


config_map = {
    "development": DevelopmentConfig,
    "production":  ProductionConfig,
    "testing":     TestingConfig,
}
