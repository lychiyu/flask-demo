# -*- coding: utf-8 -*-
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import ConfigParser

app = Flask(__name__)

app_config = ConfigParser.ConfigParser()
app_config.read('db.conf')

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://' + app_config.get('DB', 'DB_USER') + ':' + app_config.get(
    'DB', 'DB_PASSWORD') + '@' + app_config.get('DB', 'DB_HOST') + '/' + app_config.get('DB', 'DB_DB')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

mydb = SQLAlchemy()
mydb.init_app(app)


# 一对多关系，一个分类下有多条新闻记录
class Newscate(mydb.Model):
    cate_id = mydb.Column(mydb.Integer, primary_key=True)
    cate_name = mydb.Column(mydb.String(50), nullable=False)
    cate_title = mydb.Column(mydb.String(50), nullable=False)
    newses = mydb.relationship('News', backref='newscate', lazy=True)

    def __repr__(self):
        return '<Newscate %r>' % self.cate_name


# 一对多关系，一个编辑人下有多条新闻记录
class User(mydb.Model):
    user_id = mydb.Column(mydb.Integer, primary_key=True)
    user_name = mydb.Column(mydb.String(60), nullable=False)
    user_password = mydb.Column(mydb.String(30), nullable=False)
    user_nickname = mydb.Column(mydb.String(50), nullable=False)
    user_email = mydb.Column(mydb.String(100), nullable=False)
    newses = mydb.relationship('News', backref='user', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.user_nickname


class News(mydb.Model):
    news_id = mydb.Column(mydb.Integer, primary_key=True)
    news_date = mydb.Column(mydb.DateTime, nullable=False)
    news_content = mydb.Column(mydb.Text, nullable=False)
    news_title = mydb.Column(mydb.String(100), nullable=False)
    news_excerpt = mydb.Column(mydb.Text, nullable=False)
    news_status = mydb.Column(mydb.String(20), nullable=False)
    news_modified = mydb.Column(mydb.DateTime, nullable=False)
    news_category = mydb.Column(mydb.Integer, mydb.ForeignKey('newscate.cate_id'), nullable=False)
    news_author = mydb.Column(mydb.Integer, mydb.ForeignKey('user.user_id'), nullable=False)

    def __repr__(self):
        return '<News %r>' % self.news_title


# 获取所有用户信息
@app.route('/users', methods=['GET'])
def getUsers():
    data = User.query.all()
    datas = []
    for user in data:
        datas.append({'user_id': user.user_id, 'user_name': user.user_name, 'user_nickname': user.user_nickname,
                      'user_email': user.user_email})
    return jsonify(data=datas)


# 获取一个用户信息
@app.route('/user/<int:userId>', methods=['GET'])
def getUser(userId):
    user = User.query.filter_by(user_id=userId).first()
    if not user:
        result = {'msg': '该用户不存在'}
    else:
        result = {'user_id': user.user_id, 'user_name': user.user_name, 'user_nickname': user.user_nickname,
                  'user_email': user.user_email}
    return jsonify(data=result)


# 添加用户信息
@app.route('/user', methods=['POST'])
def addUser():
    user_name = request.form.get('user_name')
    user_password = request.form.get('user_password')
    user_nickname = request.form.get('user_nickname')
    user_email = request.form.get('user_email')
    user = User(user_name=user_name, user_password=user_password, user_nickname=user_nickname, user_email=user_email)
    try:
        mydb.session.add(user)
        mydb.session.commit()
    except:
        mydb.session.rollback()
        mydb.session.flush()
    userId = user.user_id
    if (user.user_id is None):
        result = {'msg': '添加用户失败'}
        return jsonify(data=result)

    data = User.query.filter_by(user_id=userId).first()
    result = {'user_id': user.user_id, 'user_name': user.user_name, 'user_nickname': user.user_nickname,
              'user_email': user.user_email}
    return jsonify(data=result)


# 修改用户信息
@app.route('/user/<int:userId>', methods=['PATCH'])
def updateUser(userId):
    user_name = request.form.get('user_name')
    user_password = request.form.get('user_password')
    user_nickname = request.form.get('user_nickname')
    user_email = request.form.get('user_email')
    try:
        user = User.query.filter_by(user_id=userId).first()
        if (user is None):
            result = {'msg': '该用户不存在'}
            return jsonify(data=result)
        else:
            user.user_name = user_name
            user.user_password = user_password
            user.user_nickname = user_nickname
            user.user_email = user_email
            mydb.session.commit()
    except:
        mydb.session.rollback()
        mydb.session.flush()
    userId = user.user_id
    data = User.query.filter_by(user_id=userId).first()
    result = {'user_id': user.user_id, 'user_name': user.user_name, 'user_password': user.user_password,
              'user_nickname': user.user_nickname, 'user_email': user.user_email}
    return jsonify(data=result)


# 删除用户
@app.route('/user/<int:userId>', methods=['DELETE'])
def deleteUser(userId):
    User.query.filter_by(user_id=userId).delete()
    mydb.session.commit()
    return getUsers()


# 首页展示新闻
@app.route('/')
def index():
    html = '<h1>Flask RESTful API</h1>'
    html += '<p>获取所有新闻数据[GET]：<br />http://127.0.0.1:5000/newslist</p>'
    html += '<p>添加一条新闻数据[POST]：<br />http://127.0.0.1:5000/news</p>'
    html += '<p>删除一条新闻数据[DELETE]：<br />http://127.0.0.1:5000/news/1</p>'
    html += '<p>修改一条新闻数据[PATCH]：<br />http://127.0.0.1:5000/news/1</p>'
    html += '<p>查询一条新闻数据[GET]：<br />http://127.0.0.1:5000/news/1</p>'
    return html


# 添加新闻
@app.route('/news', methods=['POST'])
def addNews():
    news_author = request.form.get('news_author')
    news_date = request.form.get('news_date')
    news_content = request.form.get('news_content')
    news_title = request.form.get('news_title')
    news_excerpt = request.form.get('news_excerpt')
    news_category = request.form.get('news_category')
    news_status = request.form.get('news_status')
    news_modified = request.form.get('news_modified')
    news = News(news_author=news_author, news_date=news_date, news_content=news_content, news_title=news_title,
                news_excerpt=news_excerpt, news_category=news_category, news_status=news_status,
                news_modified=news_modified)
    try:
        mydb.session.add(news)
        mydb.session.commit()
    except:
        mydb.session.rollback()
        mydb.session.flush()
    newsId = news.news_id
    if (newsId is None):
        result = {'msg': '添加失败'}
        return jsonify(data=result)

    # 查询最新插入的数据
    data = mydb.session.query(News.news_id, News.news_author, News.news_date, News.news_title, News.news_content,
                              News.news_excerpt, News.news_status, News.news_modified, Newscate.cate_name,
                              Newscate.cate_title, User.user_name, User.user_nickname).filter_by(news_id=newsId).join(
        Newscate, News.news_category == Newscate.cate_id).join(User, News.news_author == User.user_id).first()
    result = {'news_id': data.news_id, 'news_author': data.news_author, 'news_author_name': data.user_name,
              'news_author_nickname': data.user_nickname, 'news_date': data.news_date, 'news_title': data.news_title,
              'news_content': data.news_content, 'news_excerpt': data.news_excerpt, 'news_status': data.news_status,
              'news_modified': data.news_modified, 'news_cate_name': data.cate_name, 'news_cate_title': data.cate_title}
    return jsonify(data=result)


# 删除新闻
@app.route('/news/<int:newsId>', methods=['DELETE'])
def deleteNews(newsId):
    News.query.filter_by(news_id=newsId).delete()
    mydb.session.commit()
    return getNewslist()


# 修改新闻
@app.route('/news/<int:newsId>', methods=['PATCH'])
def updateNews(newsId):
    # 获取请求的数据
    news_author = request.form.get('news_author')
    news_date = request.form.get('news_date')
    news_content = request.form.get('news_content')
    news_title = request.form.get('news_title')
    news_excerpt = request.form.get('news_excerpt')
    news_category = request.form.get('news_category')
    news_status = request.form.get('news_status')
    news_modified = request.form.get('news_modified')
    try:
        news = News.query.filter_by(news_id=newsId).first()
        if (news is None):
            result = {'msg': '找不到要修改的记录'}
            return jsonify(data=result)
        else:
            news.news_author = news_author
            news.news_date = news_date
            news.news_content = news_content
            news.news_title = news_title
            news.news_excerpt = news_excerpt
            news.news_category = news_category
            news.news_status = news_status
            news.news_modified = news_modified
            mydb.session.commit()
    except:
        mydb.session.rollback()
        mydb.session.flush()
    # 获取修改的数据ID
    newsId = news.news_id
    # 查询修改的数据
    data = mydb.session.query(News.news_id, News.news_author, News.news_date, News.news_title, News.news_content,
                              News.news_excerpt, News.news_status, News.news_modified, Newscate.cate_name,
                              Newscate.cate_title, User.user_name, User.user_nickname).filter_by(news_id=newsId).join(
        Newscate, News.news_category == Newscate.cate_id).join(User, News.news_author == User.user_id).first()
    result = {'news_id': data.news_id, 'news_author': data.news_author, 'news_author_name': data.user_name,
              'news_author_nickname': data.user_nickname, 'news_date': data.news_date, 'news_title': data.news_title,
              'news_content': data.news_content, 'news_excerpt': data.news_excerpt, 'news_status': data.news_status,
              'news_modified': data.news_modified, 'news_cate_name': data.cate_name, 'news_cate_title': data.cate_title}
    return jsonify(data=result)


# 查询单个新闻
@app.route('/news/<int:newsId>', methods=['GET'])
def getNews(newsId):
    news = mydb.session.query(News.news_id, News.news_author, News.news_date, News.news_title, News.news_content,
                              News.news_excerpt, News.news_status, News.news_modified, Newscate.cate_name,
                              Newscate.cate_title, User.user_name, User.user_nickname).filter_by(news_id=newsId).join(
        Newscate, News.news_category == Newscate.cate_id).join(User, News.news_author == User.user_id).first()
    if (news is None):
        result = {'msg': '找不到数据'}
    else:
        result = {'news_id': news.news_id, 'news_author': news.news_author, 'news_author_name': news.user_name,
                  'news_author_nickname': news.user_nickname, 'news_date': news.news_date,
                  'news_title': news.news_title, 'news_content': news.news_content, 'news_excerpt': news.news_excerpt,
                  'news_status': news.news_status, 'news_modified': news.news_modified,
                  'news_cate_name': news.cate_name, 'news_cate_title': news.cate_title}
    return jsonify(data=result)


# 查询所有新闻
@app.route('/newslist', methods=['GET'])
def getNewslist():
    data = mydb.session.query(News.news_id, News.news_author, News.news_date, News.news_title, News.news_content,
                              News.news_excerpt, News.news_status, News.news_modified, Newscate.cate_name,
                              Newscate.cate_title, User.user_name, User.user_nickname).join(Newscate,
                                                                                            News.news_category == Newscate.cate_id).join(
        User, News.news_author == User.user_id)
    data_all = []
    for news in data:
        data_all.append({'news_id': news.news_id, 'news_author': news.news_author, 'news_author_name': news.user_name,
                         'news_author_nickname': news.user_nickname, 'news_date': news.news_date,
                         'news_title': news.news_title, 'news_content': news.news_content,
                         'news_excerpt': news.news_excerpt, 'news_status': news.news_status,
                         'news_modified': news.news_modified, 'news_cate_name': news.cate_name,
                         'news_cate_title': news.cate_title})
    return jsonify(data=data_all)



if __name__ == '__main__':
    app.run(debug=True)
