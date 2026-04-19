from mkg import create_app_for_developemnt
from extensions import db

app = create_app_for_developemnt("development")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run()
    