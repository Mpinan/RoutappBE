from app import db, bcrypt
from sqlalchemy.exc import IntegrityError

class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    confirm_email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    

    def __init__(self, username, email, confirm_email, password):
        self.username = username
        self.email = email
        self.confirm_email = confirm_email
        self.password = User.hashed_password(password)
    
    @staticmethod
    def create_user(payload):
        user = User(
            username=payload["username"],
            email=payload["email"],
            confirm_email=payload["confirm_email"],
            password=payload["password"],
        )

        try:
            db.session.add(user)
            db.session.commit()
            return True
        except IntegrityError:
            return False

    @staticmethod
    def hashed_password(password):
        return bcrypt.generate_password_hash(password).decode("utf-8")

    @staticmethod
    def get_user_by_id(user_id):
        user = User.query.filter_by(id=user_id).first()
        return user

    @staticmethod
    def get_user_with_email_and_password(email, password):
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return None