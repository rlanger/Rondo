import os

# Flask-WTF settings
CSRF_ENABLED = True				# cross-site request forgery protections
SECRET_KEY = 'barabbasgavel'	# crypto token


# Database configuration
DATABASE = 'postgresql://localhost/eventsdb'

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'postgresql://cicero:123@localhost/rondodb'
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
#DATABASE = os.environ.get('DATABASE_URL')
#print "DATABASE: %s" % DATABASE

OPENID_PROVIDERS = [
    { 'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id' },
    { 'name': 'Yahoo', 'url': 'https://me.yahoo.com' },
    { 'name': 'AOL', 'url': 'http://openid.aol.com/<username>' },
    { 'name': 'Flickr', 'url': 'http://www.flickr.com/<username>' },
    { 'name': 'MyOpenID', 'url': 'https://www.myopenid.com' }]