from wtforms import Form, TextField, BooleanField, PasswordField, validators,  widgets

class RegistrationForm(Form):
	"""docstring for RegistrationForm"""
	username = TextField('Username', [validators.Length(min=4, max=10)])
	github_username = TextField('Github Username')#, widget=widgets.TextArea())
	email = TextField('Email')    #email vaidation
	password = PasswordField('Password', [validators.InputRequired(), validators.EqualTo('confirm', message="Passwords must match")])
	confirm = PasswordField('Repeat Password')


class LoginForm(Form):
	"""docstring for RegistrationForm"""
	username = TextField('Username', [validators.Length(min=4, max=20)])
	password = PasswordField('Password', [validators.InputRequired()])


