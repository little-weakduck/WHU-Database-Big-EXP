from flask import Flask, render_template, request, redirect, make_response
from flask import session
import json
from flask_sqlalchemy import SQLAlchemy
import os
import pymysql
import re
from sqlalchemy import or_, and_
pymysql.install_as_MySQLdb()

app = Flask(__name__)


class Config(object):
    """配置参数"""
    # 设置连接数据库的URL
    user = 'root'
    password = '1433223'
    database = 'exp-4'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://%s:%s@localhost:3456/%s' % (
        user, password, database)

    # 设置sqlalchemy自动更跟踪数据库
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # 查询时会显示原始SQL语句
    app.config['SQLALCHEMY_ECHO'] = True

    # 禁止自动提交数据处理
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = False


# 读取配置
app.config.from_object(Config)

# 创建数据库sqlalchemy工具对象
db = SQLAlchemy(app)


class user(db.Model):
    # 定义表名
    __tablename__ = 'userinfo'
    # 定义字段
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), unique=True)
    apassword = db.Column(db.String(100), unique=True)
    usertype = db.Column(db.Integer)


class coursesinfo(db.Model):
    # 定义表名
    __tablename__ = 'coursesinfo'
    # 定义字段
    courseid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    coursename = db.Column(db.String(100), unique=True, index=True)


class studentcourse(db.Model):
    # 定义表名
    __tablename__ = 'personcourse'
    # 定义字段
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    coursename = db.Column(db.String(100), unique=True, index=True)
    personname = db.Column(db.String(100))


class course_comment(db.Model):
    # 定义表名
    __tablename__ = 'course_comment'
    # 定义字段
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    personname = db.Column(db.String(100))
    coursename = db.Column(db.String(100))
    course_comment = db.Column(db.String(100))


class teacher(db.Model):
    __tablename__ = 'teacher'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    teachername = db.Column(db.String(100), unique=True)


class teacher_course(db.Model):
    __tablename__ = 'teacher_course'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    teachername = db.Column(db.String(100))
    teachercourse = db.Column(db.String(100))


class courese_teacher(db.Model):
    __tablename__ = 'course_student'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    teachername = db.Column(db.String(100), unique=True)
# 学生：注册，登录，报名上课，退课，课程评论
# 老师：注册，登录，添加课程，退学生，删除评论
 # 一些数据库操作
# 注册


def add_user(name, password, usety):
    a_user = user(username=name, apassword=password, usertype=usety)
    db.session.add(a_user)
    db.session.commit()

# 添加课程


def add_course(name):
    a_course = coursesinfo(coursename=name)
    db.session.add(a_course)
    db.session.commit()
# 老师添加课程


def add_course_teacher(name, couese):
    a_tea = teacher_course(teachername=name, teachercourse=couese)
    db.session.add(a_tea)
    db.session.commit()
# 报名上课


def add_pe_co(name, coursename):
    a_p_c = studentcourse(coursename=coursename, personname=name)
    db.session.add(a_p_c)
    db.session.commit()
# 添加课程评论


def add_comment(com, course, name):
    # personname = db.Column(db.String(100))
    # coursename = db.Column(db.String(100))
    # course_comment = db.Column(db.String(100))
    a_com = course_comment(
        personname=name, coursename=course, course_comment=com)
    db.session.add(a_com)
    db.session.commit()


def del_student_course(name, course):
    #     coursename = db.Column(db.String(100), unique=True, index=True)
    # personname = db.Column(db.String(100))
    studentcourse.query.filter(
        and_(coursename=course, personname=name)).delete()
    db.session.commit()


def del_student_comment(comment_id):
    course_comment.query.filter(id=comment_id).delete()
    db.session.commit()
# 登录


def login_user(name, password):
    if name == "":
        return 0
    if password == "":
        return 0
    User = user.query.filter_by(username=name).first()
    if User == None:
        return 0
    if User.apassword == password:
        return 1
    return 0

# 展示所有course ，返回一个json 包括所有课程名


def showcourse():
    result = coursesinfo.query().all()
    coursename = result["coursename"]
    return json.dumps(coursename)


# 定义会话加密
app.secret_key = str(142857)
# sql注入检查


@app.before_request
def before_request():
    # 假设是post请求，data为传入的请求参数
    data = request.json
    for v in data.values():
        v = str(v).lower()
        pattern = r"\b(and|like|exec|insert|select|drop|grant|alter|delete|update|count|chr|mid|master|truncate|char|delclare|or)\b|(\*|;)"
        r = re.search(pattern, v)
        if r:
            return '请输入规范的参数！'


@app.route('/api/login')
def login_page():
    if "username" in session:
        username = session["username"]
        return render_template("index")
    else:
        return render_template("login")


@app.route('/api/login', methods=['POST'])
# 登录 将用户名和用户类型存入session中
def login():
    if request.method == 'POST':
        name = request.json['username']
        password = request.json['password']

        if login_user(name, password) == 1:
            # 设置cookie
            User = user.query.filter_by(username=name).first()
            session['username'] = User.username
            session['usertype'] = User.usertype
            resp = make_response(render_template("index"))
            resp.set_cookie("username", name, max_age=3600)
            session['username'] = name
            return resp
        else:
            return render_template("wrong_user")


@app.route('/api/signUp', methods=['POST'])
def signup():
    if request.method == 'POST':
        user = request.json['username']
        password = request.json['password']
        types = request.json['usertype']
        # 这里要加检查
        add_user(user, password=password, usety=types)
        return render_template("login")
# 学生加入课程 需要学生姓名，课程姓名


@app.route('/api/add', methods=['GET'])
def add():
    if request.method == 'POST':
        user = request.json['username']
        coursename = request.json['coursename']

        add_pe_co(name=user, coursename=coursename)
        return render_template("index")
# 删除课程 需要学生姓名，课程姓名


@app.route("/api/drop", methods=['GET'])
def drop():
    user = request.json['usename']
    coursename = request.json['coursename']
    del_student_course(user, coursename)

    return render_template("index")
# 评论 需要学生姓名，评论,课程名


@app.route("/api/comment", methods=['GET'])
def comment():
    comment = request.json['comment']
    user = request.json['username']
    course = request.json['coursename']
    add_comment(comment, course, user)
# 删除评论 需要评论id


@app.route("/api/delcom", methods=['GET'])
def delcom():
    comment_id = request.json['commentid']
    del_student_comment(comment_id)
    return render_template("index")

# 显示评论 需要一个coursename


@app.route("/api/showcoment", methods=['GET'])
def show_comment():
    result = course_comment.query.filter(coursename=request.json["coursename"])
    return json.dumps(result)


@app.route("/api/teacheradd")
def teacheradd():
    teachername = request.json["name"]
    course = request.json["course"]
# 登出


@app.route('/api/logout', methods=['POST'])
def logout():
    session.pop("username", None)


@app.route('/api/sign')
def signup_page():
    return render_template("sign")

    return render_template("news-near")


if __name__ == '__main__':
    app.run()

# url_for("static",filename="文件名")
