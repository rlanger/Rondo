import psycopg2, re, os
from flask import Flask, request, session, g, redirect, url_for, \
	abort, render_template, flash
from contextlib import closing
from flask.ext.login import LoginManager, login_required, login_user, logout_user, current_user
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.openid import OpenID
from flask.ext.wtf import Form, TextField, BooleanField, Required
from rondo import rondo, db, lm, oid
from models import User, ROLE_USER, ROLE_ADMIN, Event	

@rondo.before_request
def before_request():
	g.user = current_user

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))
	
class LoginForm(Form):
	openid = TextField('openid', validators = [Required()])
	remember_me = BooleanField('remember_me', default = False)

@rondo.route('/')
def homepage():
	return render_template('index.html')
	
@rondo.route('/get_inspired')	
def get_inspired(propmt):
	return render_template('index.html')
	
@login_required
@rondo.route('/dashboard')	
def dashboard():
	return render_template('dashboard.html')


@rondo.route('/events', methods=['POST', 'GET'])
def show_entries():

	#cur = g.db.cursor()
	#cur.execute('select title, description, start_datetime, location from entries order by start_datetime')
	#entries = [dict(title=row[0], text=row[1], start_datetime=row[2], location=row[3]) for row in cur.fetchall()]
	
	entries = db.session.query(Event)
	
	print "Entries:", entries
	
	if request.method =='POST':
		event_title = request.form['title']
		print event_title
		return render_template('show_entries.html', entries=entries, event_title=event_title)
		
	else:
		return render_template('show_entries.html', entries=entries, event_title="")

@rondo.route('/add', methods=['POST'])
@login_required
def add_entry():
	#if not session.get('logged_in'):
	#	abort(401)

	start_date = request.form['start_date']
	start_time = request.form['start_time']
	start_datetime = vali_date(start_date, start_time)
	
	name = request.form['title']
	description = request.form['text']
	location = request.form['location']
	user_id = g.user.id

	event = Event(name = name, description = description, start_datetime = start_datetime, user_id = user_id)
	db.session.add(event)
	db.session.commit()
	
	#g.db.execute('insert into entries (title, start_datetime, location, description) values (?, ?, ?, ?)', 
	#			[request.form['title'], start_datetime, request.form['location'], request.form['text']])
	
	#g.db.commit()
	flash('New entry was successfully posted')
	return redirect(url_for('show_entries'))
	

def vali_date(date, time):

#validation goes here -- REGEX?
	assert re.match(r'\d\d/\d\d/\d\d\d\d', date) is not None
	assert re.match(r'\d{0,}?:\d\d', time) is not None

	splitDate = date.split('/')
	
	dateTime = "%s-%s-%s %s" % (splitDate[2], splitDate[1], splitDate[0], time)
	print dateTime

	return dateTime

	
@rondo.route("/login", methods=["GET", "POST"])
@oid.loginhandler
def login():
	if g.user is not None and g.user.is_authenticated():
		return redirect(url_for('homepage'))
	form = LoginForm()
	if form.validate_on_submit():
		session['remember_me'] = form.remember_me.data
		return oid.try_login(form.openid.data, ask_for = ['nickname', 'email'])
		#login_user(user)
		#flash('You were logged in')
		#return redirect(url_for('show_entries')) 
			
	return render_template('login.html', title = 'Sign In', form = form, providers = app.config['OPENID_PROVIDERS'])


@oid.after_login
def after_login(resp):
    if resp.email is None or resp.email == "":
        flash('Invalid login. Please try again.')
        return redirect(url_for('login'))
    user = User.query.filter_by(email = resp.email).first()
    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname == "":
            nickname = resp.email.split('@')[0]
        nickname = User.make_unique_nickname(nickname)
        user = User(nickname = nickname, email = resp.email, role = ROLE_USER)
        db.session.add(user)
        db.session.commit()
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember = remember_me)
    return redirect(request.args.get('next') or url_for('homepage'))
    

@rondo.route("/logout")
@login_required
def logout():
	logout_user()
	return redirect(url_for('homepage'))
	
	
@rondo.route("/user/<nickname>")
def profile(nickname):
	user = User.query.filter_by(nickname = nickname).first()
	if user == None:
		flash('User ' + nickname + ' not found')
		return redirect(url_for('homepage'))
	#posts = Event.query.filter_by(user_id = username)
	return render_template('profile.html', user = user) #posts = posts)
	