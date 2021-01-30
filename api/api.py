from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask import render_template, request, url_for,redirect,send_from_directory
from sqlalchemy import *
from models import *
from app import *
import json
import os
import jwt, datetime
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date
import sys, flask
from functools import wraps
from flask_cors import CORS, cross_origin


from SimpleHTTPServer import SimpleHTTPRequestHandler, test

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

class DirectorySchema(ma.Schema):
    class Meta:
        fields = ('name', 'contact', 'address')

directory_schema = DirectorySchema()
directories_schema = DirectorySchema(many=True)

class ClassSchema(ma.Schema):
    class Meta:
        fields = ('class_num','class_name')

class_schema = ClassSchema()
classes_schema = ClassSchema(many=True)
class UserSchema(ma.Schema):
    class Meta:
        fields = ('acc_id','username','email','acc_type')

user_schema = UserSchema()
users_schema = UserSchema(many=True)


class DirectorySchema(ma.Schema):
    class Meta:
        fields = ('dir_id','name', 'contact', 'address')

class Directory(db.Model):
    dir_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    contact = db.Column(db.String(20))
    address = db.Column(db.String(50))

    def __init__(self, name,contact,address):
        self.name = name
        self.contact = contact
        self.address = address

    def __repr__(self):
        return '<Directory %r>' % self.name


#retrieve data for parent,child and teacher

@app.route('/api/users', methods=['GET'])
@cross_origin(origin='*')
def users():
    all_data = Account.query.all()
    result = users_schema.dump(all_data)
    return jsonify(result.data)

#retrieve data for parent,child and teacher
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token=None
        if 'x-access-token' in request.headers:
            token= request.headers['x-access-token']
        if not token:
            return jsonify({'message' : 'Token is missing'}),
        try:
            data = jwt.decode(token), app.config['SECRET_KEY']
            current_user = Account.query.filter_by(username=data['username']).first()
        except:
            return jsonify({'message': 'Token is invalid'}), 401
        return f(current_user, *args,**kwargs)
    return decorated


@app.route('/api/user/<acc_id>', methods=['GET'])
# @cross_origin(origin='*')
# @token_required
def getoneuser(acc_id):
    user = Account.query.filter_by(acc_id=acc_id).first()
    if not user:
        return jsonify({'message': "no user found"})
    user_data = {}
    user_data['acc_id'] = user.acc_id
    user_data['username'] = user.username
    user_data['email'] = user.email
    user_data['acc_type'] = user.acc_type
    return jsonify({'user': user_data})


@app.route('/api/teacher/<acc_id>', methods=['GET'])
# @cross_origin(origin='*')
# @token_required
def getinfoteacher(acc_id):
    user = Teacher.query.filter_by(acc_id=acc_id).first()
    if not user:
        return jsonify({'message': "no user found"})
    user_data = {}
    user_data['fname_t'] = user.fname_t
    user_data['lname_t'] = user.lname_t
    user_data['bday_t'] = user.bday_t
    user_data['specialty'] = user.specialty
    user_data['tel_num'] = user.tel_num
    user_data['add_t'] = user.add_t
    return jsonify({'user': user_data})

@app.route('/api/parent/<acc_id>', methods=['GET'])
# @cross_origin(origin='*')
# @token_required
def getinfoparent(acc_id):

    user = Parent.query.filter_by(acc_id=acc_id).first()
    if not user:
        return jsonify({'message': "no user found"})
    user_data = {}
    user_data['fname_p'] = user.fname_p
    user_data['lname_p'] = user.lname_p
    user_data['bday_p'] = user.bday_p
    user_data['add_p'] = user.add_p
    return jsonify({'user': user_data})

@app.route('/api/child/<c_id>', methods=['GET'])
# @cross_origin(origin='*')
# @token_required
def getinfochild(c_id):

    user = Child.query.filter_by(c_id=c_id).first()
    if not user:
        return jsonify({'message': "no user found"})
    user_data = {}
    user_data['fname_c'] = user.fname_c
    user_data['lname_c'] = user.lname_c
    user_data['bday_c'] = user.bday_c
    user_data['diagnosis'] = user.diagnosis
    return jsonify({'user': user_data})



    #edit profile -----------------------------

@app.route('/api/parent/editprofile/<int:acc_id>', methods=['POST']) #this api is for editing parent's profile 
# @cross_origin(origin='*')
# @token_required
def update_parentinfo(acc_id):

    Parent.query.filter_by(acc_id=int(acc_id)).first()
    data = request.get_json()

    output = Parent(fname_p = data['fname_p'], lname_p = data['lname_p'], bday_p = data['bday_p'], add_p = data['add_p'])

    output = db.session.merge(output)
    db.session.add(output)
    db.session.commit()
    return jsonify({'message' : 'success!'})


@app.route('/api/child/editprofile/<int:c_id>', methods=['POST']) #this api is for editing child's profile
# @cross_origin(origin='*')
# @token_required
def update_childinfo(c_id):

    Child.query.filter_by(acc_id=int(c_id)).first()
    data = request.get_json()

    output = Child(fname_c = data['fname_c'], lname_c = data['lname_c'], bday_c = data['bday_c'], diagnosis = data['diagnosis'])

    output = db.session.merge(output)
    db.session.add(output)
    db.session.commit()
    return jsonify({'message' : 'success!'})


@app.route('/api/teacher/editprofile/<int:acc_id>', methods=['POST']) #this api is for editing teacher's profile
# @cross_origin(origin='*')
# @token_required
def update_teacherinfo(c_id):
    Teacher.query.filter_by(acc_id=int(c_id)).first()
    data = request.get_json()
    output = Teacher(fname_t = data['fname_t'], lname_t = data['lname_t'], bday_t = data['bday_c'], specialty = data['specialty'],tel_num = data['tel_num'], add_t = data['add_t'])
    output = db.session.merge(output)
    db.session.add(output)
    db.session.commit()
    return jsonify({'message' : 'success!'})


@app.route('/api/signup', methods=['POST'])
# @cross_origin(origin='*')
def createuser():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_acc = Account(acc_type=int(data['acc_type']), username=data['username'], email=data['email'], password=hashed_password)
    db.session.add(new_acc)
    db.session.commit()

    if data['acc_type']:
        token = jwt.encode({ 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},app.config['SECRET_KEY'])
        acc_1 = Account.query.filter_by(acc_type=int(data['acc_type'])).order_by(desc(Account.acc_id)).first()
        if int(data['acc_type'])==1:
            teacher_or_parent = Teacher(acc_id=acc_1.acc_id)
        else:
            teacher_or_parent = Parent(acc_id=acc_1.acc_id)

        db.session.add(teacher_or_parent)
        db.session.commit()

    return jsonify({'message' : 'New user created.','token': token.decode('UTF-8')})


@app.route('/api/loginn', methods=['POST'])
# @cross_origin(origin='*')
def login_apii():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('un authenticated', 401, {'WWW-Authenticate' : 'Login required'})
    user = Account.query.filter_by(username=auth.username).first()
    if not user:
        return jsonify('User not found', 401, {'WWW-Authenticate' : 'Login required'})
    if check_password_hash(user.password, auth.password):
        token = jwt.encode({ 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},app.config['SECRET_KEY'])
        print 'Token generated!'
        return jsonify({'status': 'ok', 'token': token.decode('UTF-8'),'acc_type': user.acc_type, 'acc_id': user.acc_id, 'message': 'login successful!'})

@app.route('/api/login', methods=['POST'])
# @cross_origin(origin='*')
def login_api():
    #auth = request.authorization
    auth = request.json
    
    #if not auth or not auth.username or not auth.password:
    if not auth or not auth['username'] or not auth['password']:
        return make_response('un authenticated', 401, {'WWW-Authenticate' : 'Login required'})

    #user = Account.query.filter_by(username=auth.username).first()
    user = Account.query.filter_by(username=auth['username']).first()
    if not user:
        return jsonify('User not found', 401, {'WWW-Authenticate' : 'Login required'})

    #if check_password_hash(user.password, auth.password):
    if check_password_hash(user.password, auth['password']):    
        token = jwt.encode({ 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},app.config['SECRET_KEY'])
        print 'Token generated!'
        return jsonify({'status': 'ok', 'token': token.decode('UTF-8'),'acc_type': user.acc_type, 'acc_id': user.acc_id, 'message': 'login successful!'})


@app.route('/api/createeducational', methods=['POST'])
# @cross_origin(origin='*')
def createeduc():
    data = request.get_json()
    new_data = Educational(subject=data['subject'])
    db.session.add(new_data)
    db.session.commit()
    return jsonify({'message':'successfuly added!'})


@app.route('/api/geteducational/list', methods=['GET'])
# @cross_origin(origin='*')
def geteduc():
    data= Educational.query.all()
    if not data:
        return jsonify({'message': "subject not found"})
    user_data = {}
    user_data['subject'] = data.subject
    return jsonify({'user': user_data})


@app.route('/api/educational/progress', methods=['POST'])
# @cross_origin(origin='*')
def progress():
    data = request.get_json()
    new_data = Progress(details=data['details'],title=data['title'],  prog_date=data['prog_date'], prog_time=data['prog_time'],  score=data['score'])
    db.session.add(new_data)
    db.session.commit()
    return jsonify({'status': 'successfuly added!'})

@app.route('/api/add_class', methods=['POST'])
# @cross_origin(origin='*')
def enroll():
    data = request.get_json()
    new_class = Class(class_name=data['classname'])

    db.session.add(new_class)
    db.session.commit()
    return jsonify({'message' : 'New user created.'})

@app.route('/api/class', methods=['GET'])
# @cross_origin(origin='*')
def classs():
    all_data = Class.query.all()
    result = classes_schema.dump(all_data)
    return jsonify(result.data)

@app.route('/api/del_class=<int:cl_id>', methods=['GET'])
# @cross_origin(origin='*')
def del_class(cl_id):
    row = Class.query.filter_by(class_num=cl_id).first()
    db.session.delete(row)
    db.session.commit()
    all_data = Class.query.all()
    result = classes_schema.dump(all_data)
    return jsonify(result.data)

@app.route('/api/add_directory', methods=['POST'])
# @cross_origin(origin='*')
def direc2ry():
    data = request.get_json()
    new_contact = Directory(name=data['name'], contact=data['contact'], address=data['address'],)

    db.session.add(new_contact)
    db.session.commit()
    return jsonify({'message' : 'New contact added'})

@app.route('/api/directory', methods=['GET'])
# @cross_origin(origin='*')
def directory():
    all_data = Directory.query.all()
    result = directories_schema.dump(all_data)
    return jsonify(result.data)

@app.route('/api/directory=<int:d_id>', methods=['GET'])
# @cross_origin(origin='*')
def dir_search(d_id):
    user = Driectory.query.filter_by(dir_id=d_id).first()
    if not user:
        return jsonify({'message': "no user found"})
    dir_data = {}
    user_data['dir_id'] = Directory.dir_id
    user_data['name'] = Directory.name
    user_data['address'] = Directory.address
    user_data['contact'] = Directory.contact
    return jsonify({'contact_info': dir_data})


@app.route('/api/del_directory=<int:req_id>', methods=['GET'])
# @cross_origin(origin='*')
def del_directory(req_id):
    row = Directory.query.filter_by(dir_id=req_id).first()
    db.session.delete(row)
    db.session.commit()
    all_data = Directory.query.all()
    result = directories_schema.dump(all_data)
    return jsonify(result.data)

# @app.route('/api/directory=<int:d_id>', methods=['GET'])
# def dir_search(d_id):
#     directory = Directory.query.filter_by(dir_id=d_id).first()
#     if not directory:
#         return jsonify({'message': "no user found"})
#     dir_data = {}
#     dir_data['dir_id'] = directory.dir_id
#     dir_data['name'] = directory.name
#     dir_data['address'] = directory.address
#     dir_data['contact'] = directory.contact
#     return jsonify({'contact_info': dir_data})

@app.errorhandler(500)
def internal_error(error):
    return "500 error"


@app.errorhandler(404)
def not_found(error):
    return "404 error",404


class CORSHTTPRequestHandler(SimpleHTTPRequestHandler):
   def end_headers(self):
       self.send_header('Access-Control-Allow-Origin', '*')
       super(CORSHTTPRequestHandler, self).end_headers(self)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response