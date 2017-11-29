# -*- coding: utf-8 -*-
from flask import Flask, jsonify, request
from model import db, User

app = Flask(__name__)
app.config.from_object('config')

db.init_app(app)


@app.route('/')
def index():
    return '<h1>Hello Flask!</h1>'


@app.route('/user', methods=['POST'])
def addUser():
    user_name = request.form.get('user_name')
    user_password = request.form.get('user_password')
    user_nickname = request.form.get('user_nickname')
    user_email = request.form.get('user_email')
    user = User(user_name=user_name, user_password=user_password, user_nickname=user_nickname,
                user_email=user_email)
    try:
        db.session.add(user)
        db.session.commit()
    except:
        db.session.rollback()
        db.session.flush()
    userId = user.user_id
    if (user.user_id is None):
        result = {'msg': '添加失败'}
        return jsonify(data=result)
    data = User.query.filter_by(user_id=userId).first()
    result = {'user_id': data.user_id, 'user_name': data.user_name, 'user_nickname': data.user_nickname,
              'user_email': data.user_email}
    return jsonify(data=result)


@app.route('/user/<int:userId>', methods=['GET'])
def getUser(userId):
    user = User.query.filter_by(user_id=userId).first()
    if (user is None):
        result = {'msg': '找不到数据'}
    else:
        result = {'user_id': user.user_id, 'user_name': user.user_name, 'user_nickname': user.user_nickname,
                  'user_email': user.user_email}
    return jsonify(data=result)


@app.route('/user/<int:userId>', methods=['PATCH'])
def updateUser(userId):
    user_name = request.form.get('user_name')
    user_password = request.form.get('user_password')
    user_nickname = request.form.get('user_nickname')
    user_email = request.form.get('user_email')
    try:
        user = User.query.filter_by(user_id=userId).first()
        if (user is None):
            result = {'msg': '找不到要修改的记录'}
            return jsonify(data=result)
        else:
            user.user_name = user_name
            user.user_password = user_password
            user.user_nickname = user_nickname
            user.user_email = user_email
            db.session.commit()
    except:
        db.session.rollback()
        db.session.flush()
    userId = user.user_id
    data = User.query.filter_by(user_id=userId).first()
    result = {'user_id': data.user_id, 'user_name': data.user_name, 'user_password': data.user_password,
              'user_nickname': data.user_nickname, 'user_email': data.user_email}
    return jsonify(data=result)


@app.route('/user', methods=['GET'])
def getUsers():
    data = User.query.all()
    data_all = []
    for user in data:
        data_all.append({'user_id': user.user_id, 'user_name': user.user_name, 'user_nickname': user.user_nickname,
                         'user_email': user.user_email})
    return jsonify(users=data_all)


@app.route('/user/<int:userId>', methods=['DELETE'])
def deleteUser(userId):
    # 删除数据
    User.query.filter_by(user_id=userId).delete()
    db.session.commit()
    return getUsers()


if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])
