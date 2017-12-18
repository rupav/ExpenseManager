from flask import Flask, render_template, flash, request, url_for, redirect, session,  get_flashed_messages
#from flask_compress import Compress
from flask_sqlalchemy import SQLAlchemy
from Forms.forms import RegistrationForm, LoginForm
from Models._user import User, db, connect_to_db  #To make Models seperated folder!
from content_manager import Content
from passlib.hash import sha256_crypt
from functools import wraps
import gc, os

app = Flask(__name__)
app.secret_key = os.urandom(24)
file_path = os.path.abspath(os.getcwd())+"/DataBases/test.db"
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+file_path
_database = 'sqlite:///'+file_path
'''
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config['SESSION_TYPE'] = 'sqlalchemy'
app.config['TESTING'] = False
db = SQLAlchemy(app)
'''
connect_to_db(app,_database)
#Compress(app)

TOPIC_DICT = Content()

def admin_access_required(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if session['username'] == 'admin':
			return f(*args, **kwargs)
		else:
			flash("Access Denied, login as admin")
			return redirect(url_for('login_page'))
	return wrap

def login_required(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return f(*args,*kwargs)
		else:
			flash('You need to login first!')
			return redirect(url_for('login_page'))
	return wrap

@app.route('/logout/')
@login_required
def logout():
	flash("You have been logged out!")
	session.clear()
	flash("You have been logged out!")
	gc.collect()
	return redirect(url_for('main'))

def verify(_username, _password):
	if User.query.filter_by(username=_username).first() is None:
		flash("No such user found with this username")
		return False
	if not sha256_crypt.verify(_password, User.query.filter_by(username=_username).first().password):
		flash("Invalid Credentials, password isn't correct!")
		return False
	return True

@app.route('/', methods=['GET','POST'])
def main():
	#app.logger.debug(get_flashed_messages())
	return render_template('main.html')

@app.route('/dashboard/',methods=['GET','POST'])
@login_required
def dashboard():
	try:
		if request.method == 'POST':
			pass
		else:
			flash("Welcome!")
			return render_template('dashboard.html',TOPIC_DICT = TOPIC_DICT)
	except Exception as e:
		return render_template('error.html',e=e)

@app.route('/login/', methods=['GET','POST'])
def login_page():
	try:
		form = LoginForm(request.form)
		if request.method == 'POST':
			# to create data base first!
			_username = form.username.data
			_password = form.password.data

			# check if username and password are correct
			if verify(_username, _password) is False:
				return render_template('login.html', form=form)
			session['logged_in'] = True
			session['username'] = _username
			gc.collect()
			return redirect(url_for('dashboard'))
			
		return render_template('login.html', form=form)
	except Exception as e:
		return render_template('error.html',e=e)

@app.route('/register/', methods=['GET','POST'])
def register_page():
	try:
		form = RegistrationForm(request.form)
		if request.method == 'POST' and form.validate():
			_username = form.username.data
			_github_username = form.github_username.data
			_email = form.email.data
			_password = sha256_crypt.encrypt(str(form.password.data))
			user = User(username = _username, github_username = _github_username, email = _email, password = _password)
			db.create_all()
			if User.query.filter_by(username=_username).first() is not None:
				flash('User Already registered with github username {}'.format(User.query.filter_by(username=_username).first().github_username))
				return render_template('register.html', form=form)
			if User.query.filter_by(email=_email).first() is not None:
				flash('Email is already registered with us with github username {}'.format(User.query.filter_by(email=_email).first().username))
				return render_template('register.html', form=form)
			if User.query.filter_by(github_username=_github_username).first() is not None:
				flash('Email is already registered with us with github username {}'.format(User.query.filter_by(github_username=_github_username).first().username))
				return render_template('register.html', form=form)		
			flash("Thank you for registering!")

			db.session.add(user)
			db.session.commit()
			db.session.close()
			gc.collect()
			session['logged_in'] = True
			session['username'] = _username
			session.modified = True
			return redirect(url_for('dashboard'))
		return render_template('register.html', form=form)
	except Exception as e:
		return render_template('error.html',e=e)

@app.route('/database/', methods=['GET','POST'])
@login_required
@admin_access_required
def database():
	try:
		return render_template('database.html',data=User.query.all())
	except Exception as e:
		return render_template('error.html',e=e)		


@app.errorhandler(500)
@app.errorhandler(404)
def page_not_found(e):
	return render_template('error.html',e=e)

if __name__ == "__main__":
	db.creat_all()
	app.run(debug=True)