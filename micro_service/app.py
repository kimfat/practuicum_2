from hashlib import sha256
from flask import Flask
from flask_restful import Api, Resource, abort, reqparse
from uuid import uuid4
from datetime import date
from storage import JSONUsersStorage
pols = JSONUsersStorage('users.json')
app = Flask(__name__)
api = Api(app)
user_args_parser = reqparse.RequestParser().add_argument('password', type=str, help='Password of the user is required',required=True)
def ntext(username):
    if username not in pols:
        abort(404, message='Could not find user with this username')
class User(Resource):
    def get(self, username):
        ntext(username)
        return pols[username]
    def rem(self, username):
        ntext(username)
        del pols[username]
        return '', 204
    def put(self, username):
        ext(username)
        password = user_args_parser.parse_args()['password']
        today = date.today()
        pols[username] = {'password': gt_pss(password)}
        return pols[username], 201
api.add_resource(User, '/user/<string:username>')
def gt_pss(password):
    salt = uuid4().hex
    return salt + sha256((password + salt).encode()).hexdigest()
def ext(username):
    if username in pols:
        abort(409, message='User with this username is already exists')
if __name__ == '__main__':
    app.run()
