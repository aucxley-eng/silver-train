import os
from flask import Flask
 
from config import config_map
from extensions import db, seriliazer, migrate, limiter
# from app.errors import register_error_handlers


def create_app_for_developemnt(env):

    env = env or os.getenv("FLASK_ENV", "development")
    MKG = Flask(__name__)
    MKG.config.from_object(config_map[env])

    db.init_app(MKG)
    seriliazer.init_app(MKG)
    migrate.init_app(MKG, db)
    limiter.init_app(MKG)

    # register the model(tables) for sql_alchemy to see them
    with MKG.app_context():
        from mkg.auth.auth_models.domain_entity.auth_domain          import Member

        from mkg.authors_app.models.author_domain                    import Author
        from mkg.books_app.models.book_domain                        import Book

    # register the blueprints(endpoints)
    from mkg.authors_app.controllers.authors_routes                  import author_app
    MKG.register_blueprint(author_app)

    from mkg.auth.auth_controllers.routes                            import auth_bp
    MKG.register_blueprint(auth_bp)
    
    return MKG
