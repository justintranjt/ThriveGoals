from flask import Flask, jsonify, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_cas import CAS, login_required
from flask_sslify import SSLify
from flask_cors import CORS
import uuid

app = Flask(__name__)
app.config.from_object(__name__)

# Initialize database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/register' # createdb register (in postgress.app)
db = SQLAlchemy(app)

# Initialize HTTPS redirection. TODO: UNCOMMENT THIS IN DEPLOYED HEROKU VERSION
# sslify = SSLify(app)

# Initialize CAS login
cas = CAS()
cas.init_app(app)
app.config['CAS_SERVER'] = 'https://fed.princeton.edu/cas/'
app.config['CAS_AFTER_LOGIN'] = 'goals'
# This is a secret key for storing sessions. TODO: Store this securely as a Heroku environment variable
app.secret_key = '\xe3\xf9\xae*\xe7,\xf5M\x1fO\xda\xbe'

# Initialize CORD
CORS(app)

# source: http://blog.sahildiwan.com/posts/flask-and-postgresql-app-deployed-on-heroku/
# Create database model. Right now, only saving the netid's. In future, goals, tasks, etc. will be added.
# this may tie into CAS ?
class User(db.Model):
	__tablename__ = "users"
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(120), unique=True)

	def __init__(self, email):
		self.email = email

	def __repr__(self):
		return '<E-mail %r>' % self.email

# Save e-mail to database and send to success page
@app.route('/register', methods=['POST'])
def prereg():
	email = None
	if request.method == 'POST':
		email = request.form['email'] # may not be needed
		# Check that email does not already exist (not a great query, but works)
		if not db.session.query(User).filter(User.email == email).count():
			reg = User(email)
			db.session.add(reg)
			db.session.commit()
			# return render_template('success.html') # don't have html pages set up
	# return render_template('index.html')

GOALS = [
	{
		'id': uuid.uuid4().hex,
		'goalNum': '1',
		'goalTitle': 'Finish basic addition of goals',
	},
	{
		'id': uuid.uuid4().hex,
		'goalNum': '2',
		'goalTitle': 'Allow goal editing',
	},
	{
		'id': uuid.uuid4().hex,
		'goalNum': '3',
		'goalTitle': 'Allow goal deletion',
	}
]

@app.route('/')
def login():
	# I want to display the username once logged in but it doesn't work
	response_object = {'status': 'success'}
	response_object['netid'] = cas.username
	return jsonify(response_object)

@app.route('/goals', methods=['POST', 'GET'])
@login_required
def goals():
	if request.method == 'GET':
		return redirect("http://localhost:8080/goals", code=302)
	# Handle CAS login; I want to display the username once logged in but it doesn't work
	response_object = {'status': 'success'}
	response_object['netid'] = cas.username
	return jsonify(response_object)

@app.route('/getGoals', methods=['GET', 'POST'])
def all_goals():
	response_object = {'status': 'success'}
	if request.method == 'POST':
		post_data = request.get_json()
		GOALS.append({
			'id': uuid.uuid4().hex,
			'goalNum': post_data.get('goalNum'),
			'goalTitle': post_data.get('goalTitle'),
		})
		response_object['message'] = 'Goal added!'
	else:
		response_object['goals'] = GOALS
	return jsonify(response_object)

@app.route('/getGoals/<goal_id>', methods=['PUT'])
def single_goal(goal_id):
	response_object = {'status': 'success'}
	if request.method == 'PUT':
		post_data = request.get_json()
		remove_goal(goal_id)
		GOALS.append({
			'id': uuid.uuid4().hex,
			'goalNum': post_data.get('goalNum'),
			'goalTitle': post_data.get('goalTitle'),
		})
		response_object['message'] = 'Goal updated!'
	return jsonify(response_object)
def remove_goal(goal_id):
	for goal in GOALS:
		if goal['id'] == goal_id:
			GOALS.remove(goal)
			return True
	return False

if __name__ == "__main__":
	app.run()
