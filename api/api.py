
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask import render_template, request, url_for,redirect,send_from_directory
from sqlalchemy import *
from models import *
import json
import os
from werkzeug.security import generate_password_hash, check_password_hash


@app.route('/api/user/<acc_id>', methods=['GET'])
def getoneuser(acc_id):
    user = Account.query.filter_by(acc_id=acc_id).first()
    if not user:
        return jsonify({'message: "no user found"'})
    user_data = {}                          #container
    user_data['acc_id'] = user.acc_id
    user_data['username'] = user.username  #dictionary
    user_data['email'] = user.email
    user_data['acc_type'] = user.acc_type
    return jsonify({'user': user_data})

# educational logs
#api for posting progress report
@app.route('/api/educational/progress/<edu_id>', methods=['POST'])
def progress(edu_id):
    Progress.query.filter_by(edu_id=int(edu_id)).first()
    data = request.get_json()

    myProgress = Progress(title=data['title'], details=data['details'], prog_date=datetime.datetime.now(), prog_time=datetime.datetime.now(), score=data['score'])

    db.session.add(myProgress)
    db.session.commit()
    return jsonify({'data': myProgress, 'status': 'ok'})

#view progress report
@app.route('/api/educational/progress/<prog_num>', methods=['GET'])
def getprogress(prog_num):
    prog = Progress.query.filter_by(prog_num=prog_num).first()
    if not prog:
        return jsonify({'message': "no progress found"})
    user_data = {}
    user_data['title'] = prog.title
    user_data['details'] = prog.details
    user_data['prog_date'] = prog.prog_date
    user_data['prog_time'] = prog.prog_time
    user_data['score'] = prog.score
    return jsonify({'prog': user_data})
