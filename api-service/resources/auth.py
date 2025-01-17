from flask import request
from flask_restful import Resource
from database.db import db
from database.models import User
from function.function import process_user


class SignupApi(Resource):
    def post(self):
        username = request.form['username']
        password = request.form['password']
        user = User(
            username=username,
            password=password,
            email=None,
            fullname=None,
            address=None,
            phone=None,
            privilege_id=2,
            avatar='https://i.imgur.com/6PIeBYs.png',
            verified=False,
        )
        if user.sign_up():
            return {'message': 'Sign up successfully'}, 200
        return {'error': 'Username has been used'}, 401


class LoginApi(Resource):
    def post(self):
        username = request.form['username']
        password = request.form['password']
        user = db.session.query(User).filter(User.username == username).first()
        if user is None or not user.check_password(password):
            return {'error': 'Username or Password invalid'}, 401

        token = user.sign_in()
        user = process_user(user)
        del user['email'], user['fullname'], user['address'], user['phone'], user['verified'], user['privilege']

        return {'token': token,
                'user': user}, 200
