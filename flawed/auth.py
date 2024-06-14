from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash
from models import User

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password_hash, password):
        return username
    return None
