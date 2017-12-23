from flask import Flask, render_template, flash, request, url_for, redirect, session,  get_flashed_messages
from calendar import Calendar, HTMLCalendar
from flask_sqlalchemy import SQLAlchemy 
from Forms.forms import RegistrationForm, LoginForm
from Models._user import User, Budget, Category, Expenditure, db, connect_to_db  #To make Models seperated folder!
from content_manager import Content, CategoriesText
from passlib.hash import sha256_crypt
from functools import wraps
from datetime import datetime
import gc, os
import pygal


app = Flask(__name__)
app.secret_key = os.urandom(24)
file_path = os.path.abspath(os.getcwd())+"/DataBases/test.db"
_database = 'sqlite:///'+file_path
#_database =  'postgresql://localhost/[YOUR_DATABASE_NAME]'
_database =  'postgresql:///' + 'test.db'
#_database = "postgresql:///postgresql-crystalline-52597"
_database = "postgres://obdxkvayrltxks:70113e774ea85210837de8ea04dd009f4a104f19a864cd09771e1b85335981e6@ec2-54-83-3-101.compute-1.amazonaws.com:5432/df1jmn45io8vio"
connect_to_db(app,_database)


TOPIC_DICT = Content()
CATS = CategoriesText()

def admin_access_required(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if session['username'] == 'admin':
			return f(*args, **kwargs)
		else:
			flash("Access Denied, login as admin", "danger")
			return redirect(url_for('login_page'))
	return wrap

def login_required(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return f(*args,*kwargs)
		else:
			flash('You need to login first!', "warning")
			return redirect(url_for('login_page'))
	return wrap

def already_logged_in(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			flash("You are already logged in!", "success")
			return redirect(url_for('dashboard'))
		else:
			return f(*args, **kwargs)
	return wrap

def initialize_categories():
	#check if its not created yet!
	if Category.query.first() == None:

		categories_daily = ['Food', 'Travel', 'Clothing', 'Entertainment', 'Online Shopping']
		categories_monthly = ['Electricity Bill', 'Water Bill', 'Gas', 'Groceries']
		for cat in categories_daily:
			category_obj = Category(category=cat, category_daily=True, category_primary=True)
			db.session.add(category_obj)
			
		for cat in categories_monthly:
			category_obj = Category(category=cat, category_daily=False, category_primary=True)
			db.session.add(category_obj)
		
		db.session.commit()
		db.session.close()
		gc.collect()
		flash("Categories Initialized!", "success")
		return True
	return False

def pie_chart(_categories, _values, _title='Expenditure'):
	pie_chart = pygal.Pie(width=800, height=400)
	pie_chart.title = _title
	for cat, val in zip(_categories, _values):
		pie_chart.add(cat, val)
	return pie_chart.render_data_uri()

def gauge_chart(title_list, val_list, max_valList):
	
	gauge = pygal.SolidGauge(
    half_pie=True, inner_radius=0.70,
    style=pygal.style.styles['default'](value_font_size=10))

	percent_formatter = lambda x: '{:.10g}%'.format(x)
	rupees_formatter = lambda x: '{:.10g} Rs'.format(x)
	gauge.value_formatter = rupees_formatter

	for title, val, max_val in zip(title_list, val_list, max_valList):
		if max_val == 0:
			max_val = 1
		gauge.add(title, [{'value': int(val), 'max_value': int(max_val)}])

	return gauge.render_data_uri()

def convert_toPercent(_list):
	''' accepts a list and returns the list '''
	a = sum(_list)
	_new_list = []
	if a != 0:
		for i in _list:
			_new_list.append((i/a)*100)
		return _new_list
	return _list

@app.route('/logout/')
@login_required
def logout():
	flash("You have been logged out!", "success")
	session.clear()
	gc.collect()
	return redirect(url_for('main'))

def verify(_username, _password):
	if User.query.filter_by(username=_username).first() is None:
		flash("No such user found with this username", "warning")
		return False
	if not sha256_crypt.verify(_password, User.query.filter_by(username=_username).first().password):
		flash("Invalid Credentials, password isn't correct!", "danger")
		return False
	return True

def calculate_expenditure(category_id, userid, today= True):
	sum = 0
	if today:
		for obj in Expenditure.query.filter_by(expenditure_userid= userid).all():
			if obj.category_id == category_id and obj.date_of_expenditure.day == datetime.today().day:
				sum += obj.spent
		return sum
	else:
		for obj in Expenditure.query.filter_by(expenditure_userid= userid).all():
			if obj.date_of_expenditure.month == datetime.today().month and obj.category_id == category_id:
				sum += obj.spent
		return sum

def calculate_expenditureBudget_month(userid, month):
	#month should be in range (1,12]
	sum_expense = 0
	sum_budget = 0
	for obj in Expenditure.query.filter_by(expenditure_userid= userid).all():
		if obj.date_of_expenditure.month == month:
			sum_expense += obj.spent
	for obj in Budget.query.filter_by(budget_userid= userid).all():
		if obj.budget_year == datetime.today().year and obj.budget_month == month:
			sum_budget += obj.budget_amount
	return sum_expense, sum_budget


@app.route('/', methods=['GET','POST'])
def main():
	#app.logger.debug(get_flashed_messages())
	return render_template('main.html')

@app.route('/dashboard/',methods=['GET','POST'])
@login_required
def dashboard():
	html_cal = HTMLCalendar()
	html_code =  html_cal.formatmonth(datetime.today().year, datetime.today().month, True)
	username = session['username']
	pie_data = [pie_chart([cat for cat in CATS['Daily'] + CATS['Monthly']], convert_toPercent([calculate_expenditure(category_object.id, userid=User.query.filter_by(username=username).first().id, today= False) for category_object in Category.query.all()]), "My Expenditure Distribution this Month."), 
	            pie_chart([cat for cat in CATS['Daily']], convert_toPercent([calculate_expenditure(category_object.id, userid=User.query.filter_by(username=username).first().id, today= True) for category_object in Category.query.all()]) , "My Expenditure Distribution today!")]
	months = ['Jan', 'Feb', 'March', 'April', 'May', 'June', 'July', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']
	l = [calculate_expenditureBudget_month(userid=User.query.filter_by(username=username).first().id, month = month) for month in range(1,13)]
	exp, budg =  zip(*l)
	gauge_data = gauge_chart(['{}{}'.format(a,b) for a, b in zip(months,[' Expenses']*12)], exp, budg)

	try:
		if request.method == 'POST':
			initialize_categories()
			if request.form['submit'] == "Set Budget":
				username = session['username']
				_budget_userid = User.query.filter_by(username = username).first().id 
				_budget_amount = request.form['amount']
				_budget_month = datetime.today().month
				_budget_year = datetime.today().year
				budget_object = Budget(budget_userid = _budget_userid, budget_year = _budget_year, budget_month = _budget_month,  budget_amount = _budget_amount)
				db.session.add(budget_object)
				db.session.commit()
				session['current_budget_id'] = budget_object.id
				flash(session['current_budget_id'])
				flash(_budget_userid)
				db.session.close()
				gc.collect()
				flash("Budget Set!", "success")
			
			for key in CATS.keys():
				for cat in CATS[key]:
					if request.form['submit'] == "Set {} amount".format(cat):						
						username = session['username']
						_expenditure_userid = User.query.filter_by(username = username).first().id
						_spent = request.form['amount']
						_where_spent = request.form['location']
						_category_id = Category.query.filter_by(category = cat).first().id
						_date_of_expenditure = datetime.today()
						_description = request.form['comment']
						expenditure_object = Expenditure(expenditure_userid = _expenditure_userid, spent = _spent, where_spent= _where_spent, category_id = _category_id, date_of_expenditure = _date_of_expenditure, description = _description)
						db.session.add(expenditure_object)
						db.session.commit()
						db.session.close()
						gc.collect()
						flash("Expenditure recorded of {}!".format(cat))

						pie_data = [pie_chart([cat for cat in CATS['Daily'] + CATS['Monthly']], convert_toPercent([calculate_expenditure(category_object.id, userid=User.query.filter_by(username=username).first().id, today= False) for category_object in Category.query.all()]), "My Expenditure Distribution this Month."), 
						            pie_chart([cat for cat in CATS['Daily']], convert_toPercent([calculate_expenditure(category_object.id, userid=User.query.filter_by(username=username).first().id, today= True) for category_object in Category.query.all()]) , "My Expenditure Distribution today!")]

						l = [calculate_expenditureBudget_month(userid=User.query.filter_by(username=username).first().id, month = month) for month in range(1,13)]
						exp, budg =  zip(*l)
						gauge_data = gauge_chart(['{}{}'.format(a,b) for a, b in zip(months,[' Expenses']*12)], exp, budg)

						if Category.query.filter_by(category = cat).first().category_daily == True:
							flash(calculate_expenditure(_category_id, _expenditure_userid, True), "default")
							return render_template('dashboard.html',CATS = CATS, html_code = html_code, active_tab = 'expense', isDaily=True, pie_data = pie_data, gauge_data = gauge_data)
						else:
							flash(calculate_expenditure(_category_id, _expenditure_userid, False), "default")
							return render_template('dashboard.html',CATS = CATS, html_code = html_code, active_tab = 'expense', isDaily=False, pie_data = pie_data, gauge_data = gauge_data)
					
			
			return render_template('dashboard.html',CATS = CATS, html_code = html_code, active_tab = 'Home')
		else:
			flash("Welcome!","default")
			return render_template('dashboard.html',CATS = CATS, html_code = html_code, active_tab = 'Home', pie_data = pie_data, gauge_data = gauge_data)
	except Exception as e:
		return render_template('error.html',e=e)

@app.route('/login/', methods=['GET','POST'])
@already_logged_in
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
			flash(form.example.data)
			user = User(username = _username, github_username = _github_username, email = _email, password = _password)
			db.create_all()
			if User.query.filter_by(username=_username).first() is not None:
				flash('User Already registered with github username {}'.format(User.query.filter_by(username=_username).first().github_username), "warning")
				return render_template('register.html', form=form)
			if User.query.filter_by(email=_email).first() is not None:
				flash('Email is already registered with us with github username {}'.format(User.query.filter_by(email=_email).first().username), "warning")
				return render_template('register.html', form=form)
			if User.query.filter_by(github_username=_github_username).first() is not None:
				flash('User is already registered with us with username {}'.format(User.query.filter_by(github_username=_github_username).first().username), "warning")
				return render_template('register.html', form=form)		
			flash("Thank you for registering!", "success")

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
		return render_template('database.html',data= User.query.all())
	except Exception as e:
		return render_template('error.html',e=e)		


@app.errorhandler(500)
@app.errorhandler(404)
def page_not_found(e):
	return render_template('error.html',e=e)

if __name__ == "__main__":
	db.create_all()
	app.run(debug=True)