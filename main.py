from flask import Flask
from config import Config
from models import db
import routes
# import psycopg2

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

app.register_blueprint(routes.bp)

if __name__ == '__main__':
    app.run(debug=True)