from rondo import db
from hashlib import md5

ROLE_USER = 0
ROLE_ADMIN = 1

class User(db.Model):

	id = db.Column(db.Integer, primary_key = True)
	nickname = db.Column(db.String(64), unique = True)
	email = db.Column(db.String(120), unique = True)
	role = db.Column(db.SmallInteger, default = ROLE_USER)
	entity_url = db.Column(db.String(120), unique = True)
	events_authored = db.relationship('Event', backref = 'author', lazy = 'dynamic')

	
	def avatar(self, size):
		return 'http://www.gravatar.com/avatar/' + md5(self.email).hexdigest() + '?d=mm&s=' + str(size)

	def is_authenticated(self):
		return True
		
	def is_active(self):
		return True
		
	def is_anonymous(self):
		return False
		
	def get_id(self):
		return unicode(self.id)
		
	def __repr__(self):
		return '<User %r>' % (self.nickname)	
		
		
		
class Event(db.Model):

	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String)
	description = db.Column(db.String)
	start_datetime = db.Column(db.DateTime(timezone=True))
	location = db.Column(db.String)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	
	def __repr__(self):
		return '<Event: %r>' % (self.name)
		