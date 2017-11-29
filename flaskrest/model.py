# -*- coding: utf-8 -*-
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Newscate(db.Model):
    cate_id = db.Column(db.Integer, primary_key=True)
    cate_name = db.Column(db.String(50), nullable=False)
    cate_title = db.Column(db.String(50), nullable=False)
    newses = db.relationship('News', backref='newscate', lazy=True)

    def __repr__(self):
        return '<Newscate %r>' % self.cate_name


# 一对多关系，一个编辑人下有多条新闻记录
class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(60), nullable=False)
    user_password = db.Column(db.String(30), nullable=False)
    user_nickname = db.Column(db.String(50), nullable=False)
    user_email = db.Column(db.String(100), nullable=False)
    newses = db.relationship('News', backref='user', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.user_nickname


class News(db.Model):
    news_id = db.Column(db.Integer, primary_key=True)
    news_date = db.Column(db.DateTime, nullable=False)
    news_content = db.Column(db.Text, nullable=False)
    news_title = db.Column(db.String(100), nullable=False)
    news_excerpt = db.Column(db.Text, nullable=False)
    news_status = db.Column(db.String(20), nullable=False)
    news_modified = db.Column(db.DateTime, nullable=False)
    news_category = db.Column(db.Integer, db.ForeignKey('newscate.cate_id'), nullable=False)
    news_author = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)

    def __repr__(self):
        return '<News %r>' % self.news_title
