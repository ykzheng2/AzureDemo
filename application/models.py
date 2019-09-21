from . import db

class User(db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer,primary_key=True)
	username = db.Column(db.String(80),index=False,unique=True,nullable=False)
	email = db.Column(db.String(120),index=True,unique=True,nullable=False)
	created = db.Column(db.DateTime,index=False,unique=False,nullable=False)
	picture = db.Column(db.String(250),index=False,unique=True,nullable=False)
	sensors = db.relationship('Sensor', backref='user', lazy=True)

	def __init__(self, username, email, created, picture):
		self.username = username
		self.email = email
		self.created = created
		self.picture = picture
	
	def __repr__(self):
		return '<User {}>'.format(self.username)

class Sensor(db.Model):
	__tablename__ = 'Sensors'
	sid = db.Column(db.Integer, primary_key=True)
	sname = db.Column(db.String(80), index=False, unique=False, nullable=False)
	stype = db.Column(db.Boolean, index=False, unique=False, nullable=False)
	uid = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

	def __init__(self, sname, stype, uid):
		self.sname = sname
		self.stype = stype
		self.uid = uid

	def __repr__(self):
		return '<User: {}, Type: {}, UserId: {}>'.format(self.sname, self.stype, self.uid)