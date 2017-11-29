from flask import Flask, jsonify
from model import db, User
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort, marshal

app = Flask(__name__)
app.config.from_object('config')

db.init_app(app)

errors = {
    'UserAlreadyExistsError': {
        'message': "A user with that username already exists.",
        'status': 409,
    },
    'ResourceDoesNotExist': {
        'message': "A resource with that ID no longer exists.",
        'status': 410,
        'extra': "Any extra information you want.",
    },
}

api = Api(app, catch_all_404s=True, errors=errors)

parser = reqparse.RequestParser()
parser.add_argument('user_name', required=True)
parser.add_argument('user_password', required=True)
parser.add_argument('user_nickname')
parser.add_argument('user_email', required=True)

resource_full_fields = {
    'user_id': fields.Integer,
    'user_name': fields.String,
    'user_email': fields.String,
    'user_nickname': fields.String
}


class Common:
    def returnTrueJson(self, data, msg="请求成功"):
        return jsonify({
            "status": 1,
            "data": data,
            "msg": msg
        })

    def returnFalseJson(self, data=None, msg="请求失败"):
        return jsonify({
            "status": 0,
            "data": data,
            "msg": msg
        })


class Hello(Resource):
    def get(self):
        return 'Hello Flask!'


class Users(Resource):
    # @marshal_with(resource_full_fields, envelope='data')
    def get(self, userId):
        user = User.query.filter_by(user_id=userId).first()
        if (user is None):
            abort(410, msg="找不到数据", data=None, status=0)
            # return Common.returnFalseJson(Common)
        else:
            return Common.returnTrueJson(Common, marshal(user, resource_full_fields))

    def delete(self, userId):
        deleteRow = User.query.filter_by(user_id=userId).delete()
        db.session.commit()
        if (deleteRow):
            return UserList.get(UserList)
        else:
            return Common.returnFalseJson(Common)

    def put(self, userId):
        args = parser.parse_args()
        user_name = args['user_name']
        user_password = args['user_password']
        user_nickname = args['user_nickname']
        user_email = args['user_email']
        try:
            user = User.query.filter_by(user_id=userId).first()
            user.user_name = user_name
            user.user_password = user_password
            user.user_nickname = user_nickname
            user.user_email = user_email
            db.session.commit()
            userId = user.user_id
            data = User.query.filter_by(user_id=userId).first()
            return Common.returnTrueJson(Common, marshal(data, resource_full_fields))
        except:
            db.session.rollback()
            db.session.flush()
            abort(409, msg="修改失败", data=None, status=0)


class UserList(Resource):
    # @marshal_with(resource_full_fields, envelope='data')
    def get(self):
        # return marshal(User.query.all(), resource_full_fields)
        return Common.returnTrueJson(Common, marshal(User.query.all(), resource_full_fields))

    def post(self):
        args = parser.parse_args()
        user_name = args['user_name']
        user_password = args['user_password']
        user_nickname = args['user_nickname']
        user_email = args['user_email']
        user = User(user_name=user_name, user_password=user_password, user_nickname=user_nickname,
                    user_email=user_email)
        try:
            db.session.add(user)
            db.session.commit()
        except:
            db.session.rollback()
            db.session.flush()
        if (user.user_id is None):
            return Common.returnFalseJson(Common, msg="添加失败")
        else:
            return Users.get(Users, user.user_id)


api.add_resource(Hello, '/', '/hello')
api.add_resource(UserList, '/users')
api.add_resource(Users, '/users/<int:userId>')

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])
