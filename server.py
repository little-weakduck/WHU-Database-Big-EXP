from flask import Flask, jsonify, render_template, request, redirect, make_response
from flask import session
import json
from flask_sqlalchemy import SQLAlchemy
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
    apassword = db.Column(db.String(100))
    usertype = db.Column(db.Integer)


class coursesinfo(db.Model):
    # 定义表名
    __tablename__ = 'coursesinfo'
    # 定义字段
    courseid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True, index=True)
    teacher = db.Column(db.String(100))
    place = db.Column(db.String(100))
    credit = db.Column(db.Integer)
    time = db.Column(db.String(100))
    type = db.Column(db.String(100))
    capacity = db.Column(db.Integer)

    def to_json(self):
        return {
            'id': self.courseid,
            'name': self.name,
            'teacher': self.teacher,
            'place': self.place,
            'credit': self.credit,
            'time': self.time,
            "type": self.type,
            "capacity": self.capacity
        }


class studentcourse(db.Model):
    # 定义表名
    __tablename__ = 'personcourse'
    # 定义字段
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    coursename = db.Column(db.String(100))
    personname = db.Column(db.String(100))

    def to_json(self):
        return {
            'id': self.id,
            'name': self.personname,
            'course': self.coursename
        }


class course_comment(db.Model):
    # 定义表名
    __tablename__ = 'course_comment'
    # 定义字段
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    personname = db.Column(db.String(100))
    coursename = db.Column(db.String(100))
    course_comment = db.Column(db.String(100))
    comment_time = db.Column(db.String(100))

    rank = db.Column(db.Float)

    def to_json(self):
        return {
            'id': self.id,
            'name': self.personname,
            'course': self.coursename,
            'comment': self.course_comment,
            'comment_time': self.comment_time,
            "rank": self.rank
        }


# class teacher(db.Model):
#     __tablename__ = 'teacher'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     teachername = db.Column(db.String(100))


# class courese_student(db.Model):
#     __tablename__ = 'course_student'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     teachername = db.Column(db.String(100))
# 学生：注册，登录，报名上课，退课，课程评论
# 老师：注册，登录，添加课程，退学生，删除评论
 # 一些数据库操作
# 注册


def add_user(name, password, usety):
    a_user = user(username=name, apassword=password, usertype=usety)
    db.session.add(a_user)
    db.session.commit()

# 老师添加课程


def add_course(name, tea, place, cri, time, type, cap):
    # tea = db.Column(db.String(100),  index=True)
    # place = db.Column(db.String(100), index=True)
    # cri = db.Column(db.Integer)
    # time = db.Column(db.String(100), unique=True, index=True)
    # type = db.Column(db.String(100), index=True)
    # cap = db.Column(db.Integer, index=True)
    a_course = coursesinfo(name=name, teacher=tea, credit=cri,
                           time=time, type=type, capacity=cap, place=place)
    db.session.add(a_course)
    db.session.commit()
# #学生添加课程
# def add_course_teacher(name,course):
#     a_dd
#     db.session.add(a_tea)
#     db.session.commit()
# 报名上课


def add_pe_co(name, coursename):
    a_p_c = studentcourse(coursename=coursename, personname=name)
    db.session.add(a_p_c)
    db.session.commit()

# 添加课程评论


def add_comment(com, course, name, time, rank):
    # personname = db.Column(db.String(100))
    # coursename = db.Column(db.String(100))
    # course_comment = db.Column(db.String(100))
    # comment_time = db.Column(db.String(100))
    # rank = db.Column(db.Float)
    a_com = course_comment(personname=name, coursename=course,
                           course_comment=com, rank=rank, comment_time=time)
    db.session.add(a_com)
    db.session.commit()
# 删除学生课程或退课


def del_student_course(name, course):
    #     coursename = db.Column(db.String(100), unique=True, index=True)
    # personname = db.Column(db.String(100))
    studentcourse.query.filter(and_(
        studentcourse.coursename == course, studentcourse.personname == name)).delete()

    db.session.commit()

# 删除学生评论


def del_student_comment(comment_id):
    course_comment.query.filter_by(id=comment_id).delete()
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


@app.route('/api/login.html')
def login_page():
    if "username" in session:
        username = session["username"]
        return render_template("index.html")
    else:
        return render_template("login.html")


@app.route('/api/login', methods=['POST'])
# 登录 将用户名和用户类型存入session中
def login():
    if request.method == 'POST':
        data = request.get_json()
        name = data.get('username')
        password = data.get('password')

        if login_user(name, password) == 1:
            # 设置cookie
            User = user.query.filter_by(username=name).first()
            session['username'] = User.username
            session['usertype'] = User.usertype
            return jsonify({"name": name, "usertype": User.usertype})


@app.route('/api/signUp', methods=['POST'])
def signup():
    if request.method == 'POST':
        data = request.get_json()
        user = data.get('username')
        password = data.get('password')
        types = data.get('usertype')
        # 这里要加检查
        add_user(user, password=password, usety=types)
        return jsonify({"username": user, "usertype": types})

# 修改课程


@app.route("/api/course/change" ,methods=['POST'])
def change():
    data = request.get_json()
    # cap = db.Column(db.Integer, index=True)
    teachername = data.get("teacher")
    name = data.get("name")
    cri = data.get("credit")
    time = data.get("time")
    type = data.get("type")
    pla = data.get("place")
    cap = data.get("capacity")
    result = coursesinfo.query.filter(
        and_(coursesinfo.name == name, coursesinfo.teacher == teachername)).first()
    result.time = time
    result.type = type
    result.place = pla
    db.session.commit()
    return jsonify({})
# 学生加入课程 需要学生姓名，课程姓名


@app.route('/api/add', methods=['POST'])
def add():
    if request.method == 'POST':
        data = request.get_json()
        user = data.get('username')
        coursename = data.get('coursename')

        add_pe_co(name=user, coursename=coursename)
        return jsonify({})

# 获取课程学生


@app.route("/api/allstudent", methods=['POST'])
def show_allpeople():
    data = request.get_json()
    coursename = data.get("coursename")
    result = studentcourse.query.filter_by(coursename=coursename).all()
    temp = []
    for x in result:
        temp.append(x.to_json())
    return jsonify(temp)
# 删除课程 需要学生姓名，课程姓名


@app.route("/api/drop", methods=['POST'])
def drop():
    data = request.get_json()
    user = data.get('username')
    coursename = data.get('coursename')
    del_student_course(user, coursename)
    return jsonify({})
# 评论 需要学生姓名，评论,课程名


@app.route("/api/comment", methods=['POST'])
def comment():
    data = request.get_json()
    comment = data.get('comment')
    user = data.get('name')
    course = data.get('coursename')
    time = data.get('comment_time')
    rank = data.get('rank')
    add_comment(comment, course, user, time, rank)
    return jsonify({})
# 删除评论 需要评论id


@app.route("/api/delcom", methods=['POST'])
def delcom():
    data = request.get_json()
    comment_id = data.get('commentid')
    del_student_comment(comment_id)
    return jsonify({})
# 显示评论 需要一个coursename


@app.route("/api/showcoment", methods=['POST'])
def show_comment():
    data = request.get_json()
    result = course_comment.query.filter_by(coursename=data.get("coursename"))
    temp = []
    for x in result:
        temp.append(x.to_json())
    return jsonify(temp)

# 展示所有course ，返回一个json 包括所有课程名


@app.route("/api/course/all", methods=['POST'])
def showcourse():
    if request.method == 'POST':
        result = coursesinfo.query.filter_by().all()
        temp = []
        for x in result:
            temp.append(x.to_json())
        return jsonify(temp)

# 显示已选课程


@app.route("/api/show_already", methods=['POST'])
def show_already():
    data = request.get_json()
    result = studentcourse.query.filter_by(personname=data.get("username"))
    temp = []
    for x in result:
        temp.append(x.to_json())
    return jsonify(temp)

# 老师添加课程


@app.route("/api/teacheradd", methods=['POST'])
def teacheradd():
    # tea = db.Column(db.String(100),  index=True)
    # place = db.Column(db.String(100), index=True)
    # cri = db.Column(db.Integer)
    # time = db.Column(db.String(100), unique=True, index=True)
    # type = db.Column(db.String(100), index=True)
    data = request.get_json()
    # cap = db.Column(db.Integer, index=True)
    teachername = data.get("teacher")
    course = data.get("name")
    cri = data.get("credit")
    time = data.get("time")
    type = data.get("type")
    pla = data.get("place")
    cap = data.get("capacity")
    add_course(course, teachername, pla, cri,  time, type, cap)
    return jsonify({})
# 登出


@app.route('/api/logout', methods=['POST'])
def logout():
    session.pop("username", None)


@app.route('/api/sign.html')
def signup_page():
    return render_template("sign.html")


if __name__ == '__main__':
    app.run()

# url_for("static",filename="文件名")
