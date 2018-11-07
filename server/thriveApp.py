from flask import Flask, jsonify, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_cas import CAS, login_required
from flask_sslify import SSLify
from flask_cors import CORS

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
app.config['CAS_AFTER_LOGIN'] = 'login'
# This is a secret key for storing sessions. TODO: Store this securely as a Heroku environment variable
app.secret_key = '\xe3\xf9\xae*\xe7,\xf5M\x1fO\xda\xbe'

# Initialize CORS
CORS(app)

# source: http://blog.sahildiwan.com/posts/flask-and-postgresql-app-deployed-on-heroku/
# Create database model. Right now, only saving the netID's. In future, goals, tasks, etc. will be added.
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

# Preloaded goals to be displayed
goals = [
	{
		'goalNum': 1,
		'goalTitle': 'Finish basic addition of goals',
		'completed': False,
	},
	{
		'goalNum': 3,
		'goalTitle': 'Allow goal editing',
		'completed': False,
	},
	{
		'goalNum': 2,
		'goalTitle': 'Allow goal deletion',
		'completed': False,
	}
]

# Using this as a global variable
netID = None

# TODO Make use of the database and access the netID field instead of using global var!
@app.route('/loginPage', methods=['GET'])
@login_required
def login():
	global netID
	netID = cas.username
	return redirect("http://localhost:8080/goals", code=302)

@app.route('/loginNetID', methods=['GET'])
def loginNetID():
	# Handle CAS login
	response_object = {'status': 'success'}
	global netID
	response_object['netID'] = netID
	return jsonify(response_object)

# Mark goal as completed
@app.route('/completeGoal/<goal_num>', methods=['PUT'])
def cmpl_goal(goal_num):
	response_object = {'status': 'success', 'message': 'Goal completed!'}

	for goal in goals:
		if int(goal['goalNum']) == int(goal_num):
			goal['completed'] = True
	
	return jsonify(response_object)

# Retrieving all current goals and adding new goals 
@app.route('/modGoals', methods=['GET', 'POST'])
def all_goals():
	response_object = {'status': 'success'}
	if request.method == 'POST':
		post_data = request.get_json()
		# Overwrite existing goal if number is identical
		remove_goal(post_data.get('goalNum'))
		goals.append({
			'goalNum': post_data.get('goalNum'),
			'goalTitle': post_data.get('goalTitle'),
			'completed': post_data.get('completed'),
		})
		response_object['message'] = 'Goal added!'
	else:
		response_object['goals'] = goals

	# Sort by goal number
	goals.sort(key=lambda goal: goal['goalNum'])

	return jsonify(response_object)

# Updating preexisting goals and deleting goals
@app.route('/modGoals/<goal_num>', methods=['PUT', 'DELETE'])
def update_rem_goal(goal_num):
	response_object = {'status': 'success'}
	if request.method == 'PUT':
		post_data = request.get_json()
		# Handles update, overwrites old goal number and overwrites new number
		remove_goal(goal_num)
		remove_goal(post_data.get('goalNum'))

		goals.append({
			'goalNum': post_data.get('goalNum'),
			'goalTitle': post_data.get('goalTitle'),
			'completed': post_data.get('completed'),
		})
		response_object['message'] = 'Goal updated!'
	elif request.method == 'DELETE':
		remove_goal(goal_num)
		response_object['message'] = 'Goal deleted!'
		
	# Sort by goal number
	goals.sort(key=lambda goal: goal['goalNum'])

	return jsonify(response_object)

def remove_goal(goal_num):
	for goal in goals:
		if int(goal['goalNum']) == int(goal_num):
			goals.remove(goal)

if __name__ == "__main__":
	app.run()
