from app import *
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

<<<<<<< HEAD:api/models.py
class Account(db.Model):
    acc_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), unique=True)
=======
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:regards@localhost/db'
app.config['SECRET_KEY'] = 'hard to guess string'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)


class Account(db.Model):
    acc_id = db.Column(db.Integer, primary_key=True)
    acc_type = db.Column(db.Integer, unique=True)
    username = db.Column(db.String(50), unique=True)
>>>>>>> 3180fb0cd735767f1568d17c8b7773bc76d68e52:app/models.py
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(150))
    acc_type = db.Column(db.Integer)
    acc_p = db.relationship("Parent", uselist=False, backref="account")
    acc_t = db.relation("Teacher", uselist=False, backref="account")

    def __init__(self, acc_type, username, email, password):
        self.acc_type = acc_type
        self.username = username
        self.email = email
        self.password = password
    def __repr__(self):
        return '<Account %r>' % self.acc_type

class Access_Token(db.Model):
    tkn_num = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(20), unique=True)

    def __init__(self, token):
        self.token = token

    def __repr__(self):
        return '<Access_Token %r>' % self.token

class Parent(db.Model):
    p_id = db.Column(db.Integer, primary_key=True)
    fname_p = db.Column(db.String(80))
    lname_p = db.Column(db.String(80))
    bday_p = db.Column(db.Date)
    add_p = db.Column(db.String(120))
    acc_id = db.Column(db.Integer, db.ForeignKey('account.acc_id'))
    child = db.relationship("Child", uselist=False, backref="parent")

    def __init__(self, acc_id):
        self.fname_p = None
        self.lname_p = None
        self.bday_p = None
        self.add_p = None
        self.acc_id = acc_id

    def __repr__(self):
        return '<Parent %r>' % self.fname_p
class Child(db.Model):
    c_id = db.Column(db.Integer, primary_key=True)
    fname_c = db.Column(db.String(80))
    lname_c = db.Column(db.String(80))
    bday_c = db.Column(db.Date)
    diagnosis = db.Column(db.String(50))
    p_id = db.Column(db.Integer, db.ForeignKey('parent.p_id'))
    pers = db.relationship('Personal', backref='child', lazy='dynamic')

    def __init__(self, fname_c, lname_c, bday_c, diagnosis):
        self.fname_c = fname_c
        self.lname_c = lname_c
        self.bday_c = bday_c
        self.diagnosis = diagnosis

    def __repr__(self):
        return '<Child %r>' % self.fname_c

class Teacher(db.Model):
    t_id = db.Column(db.Integer, primary_key=True)
    fname_t = db.Column(db.String(80))
    lname_t = db.Column(db.String(80))
    bday_t = db.Column(db.Date)
    specialty = db.Column(db.String(120))
    tel_num = db.Column(db.BigInteger)
    add_t = db.Column(db.String(120))
    acc_id = db.Column(db.Integer, db.ForeignKey('account.acc_id'))

    def __init__(self, acc_id):
        self.fname_t = None
        self.lname_t = None
        self.bday_t = None
        self.specialty = None
        self.tel_num = None
        self.add_t = None
        self.acc_id = acc_id

    def __repr__(self):
        return '<Teacher %r>' % self.fname_t

class Personal(db.Model):
    per_num = db.Column(db.Integer, primary_key=True)
    per_name = db.Column(db.String(50))
    child_id = db.Column(db.Integer, db.ForeignKey('child.c_id'))
    spec = db.relationship('Specifics', backref='specify', lazy='dynamic')

    def __init__(self, per_name):
        self.per_name = per_name

    def __repr__(self):
        return '<Personal %r>' % self.per_name

<<<<<<< HEAD:api/models.py
=======
class Specifics(db.Model):
    spec_num = db.Column(db.Integer, primary_key=True)
    spec_name = db.Column(db.String(50))
    per_id = db.Column(db.Integer, db.ForeignKey('personal.per_num'))
    log = db.relationship('Logs', backref='logs', lazy='dynamic')

    def __init__(self, spec_name):
        self.spec_name = spec_name
>>>>>>> 3180fb0cd735767f1568d17c8b7773bc76d68e52:app/models.py


class Logs(db.Model):
    log_num = db.Column(db.Integer, primary_key=True)
    clicks = db.Column(db.Integer)
    log_date = db.Column(db.Date)
    log_time = db.Column(db.Time)
    spec_id = db.Column(db.Integer, db.ForeignKey('specifics.spec_num'))

    def __init__(self, clicks, log_date, log_time):
        self.clicks = clicks
        self.log_date = log_date
        self.log_time = log_time

    def __repr__(self):
        return '<Logs %r>' % self.clicks
activity = db.Table('activity',
                    db.Column('spec_num', db.Integer, db.ForeignKey('specifics.spec_num')),
                    db.Column('log_num', db.Integer, db.ForeignKey('logs.log_num'))
                    )

class Specifics(db.Model):
    spec_num = db.Column(db.Integer, primary_key=True)
    spec_name = db.Column(db.String(50))
    act = db.relationship('Logs', secondary=activity, backref=db.backref('act', lazy='dynamic'))
    specify_id = db.Column(db.Integer, db.ForeignKey('personal.per_num'))

    def __init__(self, spec_name):
        self.spec_name = spec_name

    def __repr__(self):
        return '<Specifics %r>' % self.spec_name
class Class(db.Model):
    class_num = db.Column(db.Integer, primary_key=True)
    class_name = db.Column(db.String(50))
    ed = db.relationship('Educational', backref='edu', lazy='dynamic')

    def __init__(self, class_name):
        self.class_name = class_name

    def __repr__(self):
        return '<Class %r>' % self.class_name

class Educational(db.Model):
    ed_num = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(50))
    edu_id = db.Column(db.Integer, db.ForeignKey('class.class_num'))
    prog = db.relationship('Progress', backref='progs', lazy='dynamic')

    def __init__(self, subject):
        self.subject = subject

    def __repr__(self):
<<<<<<< HEAD:api/models.py
        return '<Educational %r>' % self.subject
=======
        return '<Educational %r>' % self.per_subject

class Items(db.Model):
    item_num = db.Column(db.Integer, primary_key=True)
    desc = db.Column(db.String(120))

    def __init__(self, desc):
        self.desc = desc

    def __repr__(self):
        return '<Items %r>' % self.desc

>>>>>>> 3180fb0cd735767f1568d17c8b7773bc76d68e52:app/models.py
class Progress(db.Model):
    prog_num = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    details = db.Column(db.String(500))
    prog_date = db.Column(db.Date)
    prog_time = db.Column(db.Time)
    score = db.Column(db.Integer)
    edu_id = db.Column(db.Integer, db.ForeignKey('educational.ed_num'))

    def __init__(self, title, details, prog_date, prog_time, score):
        self.title = title
        self.details = details
        self.prog_date = prog_date
        self.prog_time = prog_time
        self.score = score
    def __repr__(self):
        return '<Progress %r>' % self.title

report = db.Table('report',
                    db.Column('item_num', db.Integer, db.ForeignKey('items.item_num')),
                    db.Column('prog_num', db.Integer, db.ForeignKey('progress.prog_num'))
                  )

class Items(db.Model):
    item_num = db.Column(db.Integer, primary_key=True)
    desc = db.Column(db.String(120)),
    rep = db.relationship('Progress', secondary=report, backref=db.backref('rep', lazy='dynamic'))

    def __init__(self, desc):
        self.desc = desc

    def __repr__(self):
        return '<Items %r>' % self.desc

class Images(db.Model):
    img_id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.String(50))

    def __init__(self, img):
        self.img = img

    def __repr__(self):
        return '<Images %r>' % self.img

class Audio(db.Model):
    aud_id = db.Column(db.Integer, primary_key=True)
    aud = db.Column(db.String(50))
    def __init__(self, aud):
        self.aud = aud
    def __repr__(self):
        return '<Audio %r>' % self.aud

if __name__ == '__main__':
<<<<<<< HEAD:api/models.py
    app.run()
=======
    app.run()


>>>>>>> 3180fb0cd735767f1568d17c8b7773bc76d68e52:app/models.py
