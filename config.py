import os

# Flask-WTF settings
CSRF_ENABLED = True				# cross-site request forgery protections
SECRET_KEY = 'barabbasgavel'	# crypto token


# Database configuration
DATABASE = os.environ.get('DATABASE_URL')
#DATABASE = 'postgresql://localhost/eventsdb'

if os.environ.get('HEROKU') is None:
	SQLALCHEMY_DATABASE_URI = 'postgresql://cicero:123@localhost/rondodb'
else:
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
#DATABASE = os.environ.get('DATABASE_URL')
#print "DATABASE: %s" % DATABASE

OPENID_PROVIDERS = [
    { 'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id' },
    { 'name': 'Yahoo', 'url': 'https://me.yahoo.com' },
    { 'name': 'AOL', 'url': 'http://openid.aol.com/<username>' },
    { 'name': 'Flickr', 'url': 'http://www.flickr.com/<username>' },
    { 'name': 'MyOpenID', 'url': 'https://www.myopenid.com' }]