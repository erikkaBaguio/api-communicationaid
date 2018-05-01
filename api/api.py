
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
#post progress report
@app.route('/api/educational/progress', methods=['POST'])
def progress():
    data = request.get_json()
    new_data = Progress(details=data['details'],title=data['title'],  prog_date=data['prog_date'], prog_time=data['prog_time'],  score=data['score'])
    db.session.add(new_data)
    db.session.commit()
    return jsonify({'status': 'successfuly added!'})
#view progress report
@app.route('/api/educational/progress/<prog_num>', methods=['GET'])
def getinfochild(prog_num):
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
