from flask import Flask
from flask import jsonify, request, json

from app.models.models import User, Route
from app import app
# from app import auth

from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

import os

@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username = username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


@app.route('/')
def index():
    return "Hello, World!"

@app.route('/login', methods=["GET"])
@auth.verify_password
def verify_password(username, password):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username = username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


@app.route("/user", methods=["GET"])
def get_user():
    return jsonify(result=g.current_user,
                    routes=Route.get_latest_routes())


@app.route("/create_user", methods=["POST"])
def create_user():
    incoming = request.get_json()
    print(incoming)
    success, id = User.create_user(User(
        incoming["username"],
        incoming["email"],
        incoming["password"],
        incoming["true"]
    ))

    if not success:
        return jsonify(message="User with that email already exists"), 409
        new_user = User.query.filter_by(email=incoming["email"]).first()

    return jsonify(
        id=new_user.id,
        token=generate_token(new_user)
    )


@app.route("/get_token", methods=["POST"])
@auth.login_required
def get_token():
    token = g.user.generate_auth_token()
    return jsonify({ 'token': token.decode('ascii') })


@app.route("/is_token_valid", methods=["POST"])
def is_token_valid():
    incoming = request.get_json()
    is_valid = verify_token(incoming["token"])

    if is_valid:
        return jsonify(token_is_valid=True)
    else:
        return jsonify(token_is_valid=False), 403


@app.route("/create_route", methods=["POST"])
@auth.login_required
def create_route():
    incoming = request.get_json()
    success, id = Route.create_route(
        incoming["name"],
        incoming["method"],
        incoming["origin"],
        incoming["destination"],
        incoming["user_id"]
    )
    
    if not success:
        return jsonify(message="Error submitting task", id=None), 409

    return jsonify(success=True, id=id)



@app.route("/get_routes_for_user", methods=["POST"])
@auth.login_required
def get_routes_for_user():
    incoming = request.get_json()

    return jsonify(
        routes=[i.serialize for i in Route.get_routes_for_user(incoming["user_id"]).all()]
    )

@app.route("/delete_route", methods=["POST"])
@auth.login_required
def delete_route():
    incoming = request.get_json()

    success = Route.delete_route(incoming.get('route_id'))
    if not success:
        return jsonify(message="Error deleting route"), 409

    return jsonify(success=True)


@app.route("/edit_route", methods=["POST"])
@auth.login_required
def edit_route():
    incoming = request.get_json()
   
    success = Route.edit_route(
        incoming["route_id"],
        incoming["name"],
        incoming["method"],
        incoming["origin"],
        incoming["destination"]
    )
    if not success:
        return jsonify(message="Error editing task"), 409

    return jsonify(success=True)
