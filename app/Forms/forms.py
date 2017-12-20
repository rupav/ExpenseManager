from wtforms import Form, TextField, BooleanField, PasswordField, validators,  widgets, SelectMultipleField

class MultiCheckboxField(SelectMultipleField):
	widget = widgets.ListWidget(prefix_label=False)
	option_widget = widgets.CheckboxInput()


class RegistrationForm(Form):
	"""docstring for RegistrationForm"""
	username = TextField('Username', [validators.Length(min=4, max=20)])
	github_username = TextField('Github Username')
	email = TextField('Email')    #email vaidation
	password = PasswordField('Password', [validators.InputRequired(), validators.EqualTo('confirm', message="Passwords must match")])
	confirm = PasswordField('Repeat Password')

	string_of_files = ['one\r\ntwo\r\nthree\r\n']
	list_of_files = string_of_files[0].split()
	# create a list of value/description tuples
	files = [(x, x) for x in list_of_files]
	example = MultiCheckboxField('Label', choices=files)


class LoginForm(Form):
	"""docstring for RegistrationForm"""
	username = TextField('Username', [validators.Length(min=4, max=20)])
	password = PasswordField('Password', [validators.InputRequired()])


