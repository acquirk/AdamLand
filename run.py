from app import app, db
import os

def test_db_connection():
    try:
        with app.app_context():
            db.engine.connect()
        print("Database connection successful!")
    except Exception as e:
        print(f"Database connection failed. Error: {e}")

if __name__ == '__main__':
    test_db_connection()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
