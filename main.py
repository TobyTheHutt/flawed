from flask import Flask
from config import Config
from models import db, User
import routes
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

app.register_blueprint(routes.bp)

with app.app_context():
    db.create_all()
    # Add a sample user to the database for testing
    if not User.query.filter_by(username='testuser').first():
        sample_user = User(username='testuser', email='testuser@example.com', password_hash=generate_password_hash('testpassword'))
        db.session.add(sample_user)
        db.session.commit()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
