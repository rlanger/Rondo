# all the imports
import sqlite3, re
from flask import Flask, request, session, g, redirect, url_for, \
	abort, render_template, flash
from contextlib import closing
from flask.ext.login import LoginManager
	
# configuration
DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

# create our application
app = Flask(__name__)
app.config.from_object(__name__)

app.debug = DEBUG

login_manager = LoginManager()
	
# creates the database tables
def init_db():
	with closing(connect_db()) as db:
		with app.open_resource('schema.sql') as f:
			db.cursor().executescript(f.read())
		db.commit()
		
def connect_db():
	return sqlite3.connect(app.config['DATABASE'])

@app.before_request
def before_request():
	g.db = connect_db()
	
@app.teardown_request
def teardown_request(exception):
	g.db.close()
	
@app.route('/')
def homepage():
	return render_template('index.html')
	
@app.route('/get_inspired')	
def get_inspired(propmt):
	return render_template('index.html')
	
@app.route('/dashboard')	
def dashboard():
	return render_template('dashboard.html')


@app.route('/events', methods=['POST', 'GET'])
def show_entries():

	cur = g.db.execute('select title, description, start_datetime, location from entries order by start_datetime')
	entries = [dict(title=row[0], text=row[1], start_datetime=row[2], location=row[3]) for row in cur.fetchall()]
	
	if request.method =='POST':
		event_title = request.form['title'];
		print event_title
		return render_template('show_entries.html', entries=entries, event_title=event_title)
		
	else:
		return render_template('show_entries.html', entries=entries, event_title="")


@app.route('/add', methods=['POST'])
def add_entry():
	if not session.get('logged_in'):
		abort(401)

	start_date = request.form['start_date'];
	start_time = request.form['start_time'];
	start_datetime = vali_date(start_date, start_time);
	
	g.db.execute('insert into entries (title, start_datetime, location, description) values (?, ?, ?, ?)', 
				[request.form['title'], start_datetime, request.form['location'], request.form['text']])
	g.db.commit()
	flash('New entry was successfully posted')
	return redirect(url_for('show_entries'))
	

def vali_date(date, time):

#validation goes here -- REGEX?
	assert re.match(r'\d\d/\d\d/\d\d\d\d', date) != None
	assert re.match(r'\d{0,}?:\d\d', time) != None

	splitDate = date.split('/')
	
	dateTime = "%s-%s-%s %s" % (splitDate[2], splitDate[1], splitDate[0], time)
	print dateTime

	return dateTime



@app.route('/login', methods = ['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['username'] != app.config['USERNAME']:
			error = 'Invalid username'
		elif request.form['password'] != app.config['PASSWORD']:
			error = 'Invalid password'
		else:
			session['logged_in'] = True
			flash('You were logged in')
			return redirect(url_for('show_entries'))
	return render_template('login.html', error = error)
	
@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	flash('You were logged out')
	return redirect(url_for('show_entries'))
	
if __name__ == '__main__':
	init_db()
	login_manager.init_app(app)
	app.run()