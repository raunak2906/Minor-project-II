import pymysql
pymysql.install_as_MySQLdb()
from main import app, db, Review, User

if __name__ == "__main__":
    with app.app_context():
        # This will create tables for models that don't exist in the DB yet
        db.create_all()
        print("Database tables updated (Review table created if missing).")
