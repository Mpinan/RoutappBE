import datetime
from app import db, bcrypt
from sqlalchemy.exc import IntegrityError
from sqlalchemy.dialects.postgresql import JSON

class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(255), unique=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    email_verified = db.Column(db.Boolean)
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    routes = db.relationship('Route', backref='author', lazy='dynamic')
    

    def __init__(self, username, email, password, email_verified):
      self.username = username
      self.email = email
      self.password = User.hashed_password(password)
      self.email_verified = email_verified

    
    @staticmethod
    def create_user(self):
      print(self, "i am a payload")

      db.session.add(self)
      try:
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

# Routes Model

class Route(db.Model):

    __tablename__ = 'routes'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255), unique=True)
    method = db.Column(db.String(255), unique=True)
    origin = db.Column(JSON)
    destination = db.Column(JSON)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, name, method, origin, destination, user_id):
      self.name = name
      self.method = method
      self.origin = origin
      self.destination = destination
      self.user_id = user_id

    
    def create_route(self):
      db.session.add(self)
      try:
        db.session.commit()
        return True
      except IntegrityError:
          return False

    def delete_route(route_id):
      print(route_id, "hello in model delete")
      route_to_delete = Route.query.filter_by(id=route_id).first()
      db.session.delete(route_to_delete)
      try:
        db.session.commit()
        return True
      except IntegrityError:
        return False


    def edit_route(route_id, name, method, origin, desetination):
      route_to_update = Route.query.filter_by(id=route_id).first()
      if not route_to_update:
        return
      else:
        route_to_update.name = name
        route_to_update.method = method
        route_to_update.origin = origin
        route_to_update.destination = destination

      try:
      	db.session.commit()
      	return True, self.id
      except IntegrityError:
        print("i am an error")
        return False, None
        db.session.commit()

    @property
    def serialize_route(self):
    	"""Return object data in easily serializeable format"""
    	return {
    	    'id'         	: self.id,
    	    'name'       	: self.name,
    	    'method'     	: self.method,
    	    'origin'     	: self.origin,
    	    'destination'	: self.destination,
    	    'user_id'    	: self.user_id,
    	}