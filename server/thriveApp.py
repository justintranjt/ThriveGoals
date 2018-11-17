from flask import Flask, jsonify, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_cas import CAS, login_required
from flask_sslify import SSLify
from flask_cors import CORS
from os import environ
from waitress import serve

app = Flask(__name__, static_folder='./dist/static', template_folder='./dist')
app.config.from_object(__name__)

# Initialize database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/register' # createdb register (in postgress.app)
db = SQLAlchemy(app)

# Initialize HTTPS redirection.
sslify = SSLify(app)

# Initialize CAS login
cas = CAS()
cas.init_app(app)
app.config['CAS_SERVER'] = 'https://fed.princeton.edu/cas/'
app.config['CAS_AFTER_LOGIN'] = 'login'

# This is a secret key for storing sessions. 
secret_key = environ.get('SECRET_KEY', "developmentsecretkey")
app.secret_key = secret_key

# Initialize CORS
CORS(app)

# Preloaded goals to be displayed
allGoals = {}
goals = [
	{
		'goalNum': 1,
		'goalTitle': 'Finish basic addition of goals',
		'completed': False,
		'inProgress': False,
	},
	{
		'goalNum': 3,
		'goalTitle': 'Allow goal editing',
		'completed': False,
		'inProgress': False,
	},
	{
		'goalNum': 2,
		'goalTitle': 'Allow goal deletion',
		'completed': False,
		'inProgress': False,
	},
]
goals2 = [
	{
		'goalNum': 1,
		'goalTitle': 'Alternate template!',
		'completed': False,
		'inProgress': False,
	},
]
allGoals["Template 1"] = goals
allGoals["Template 2"] = goals2

# Using this as a global variable
netID = None

# See here for more info: http://flask.pocoo.org/snippets/57/
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
	return render_template("index.html")

# TODO Make use of the database and access the netID field instead of using global var!
@app.route('/loginPage', methods=['GET'])
@login_required
def login():
	global netID
	netID = cas.username
	
	# Bind to URIROOT if defined, otherwise default to localhost
	uriRoot = environ.get('URIROOT', "http://localhost:8080")
	return redirect(uriRoot + "/goals", code=302)

@app.route('/loginNetID', methods=['GET'])
def loginNetID():
	# Handle CAS login
	response_object = {'status': 'success'}
	global netID
	response_object['netID'] = netID
	return jsonify(response_object)

# Mark goal as completed
@app.route('/completeGoal/<goal_num>/<goal_template_id>', methods=['PUT'])
def cmpl_goal(goal_num, goal_template_id):
	response_object = {'status': 'success'}

	for goal in allGoals[goal_template_id]:
		if int(goal['goalNum']) == int(goal_num):
			if goal['completed']:
				goal['completed'] = False
				response_object['message'] = 'Goal not completed.'
			else:
				goal['completed'] = True
				response_object['message'] = 'Goal completed!'
	
	return jsonify(response_object)

# Mark goal as inProgress
@app.route('/inProgGoal/<goal_num>/<goal_template_id>', methods=['PUT'])
def in_prog_goal(goal_num, goal_template_id):
	response_object = {'status': 'success'}

	for goal in allGoals[goal_template_id]:
		if int(goal['goalNum']) == int(goal_num):
			if goal['completed']:
				goal['completed'] = False
				response_object['message'] = 'Goal is in progress.'
			if goal['inProgress']:
				goal['inProgress'] = False
				response_object['message'] = 'Goal is not in progress.'
			else:
				goal['inProgress'] = True
				response_object['message'] = 'Goal is in progress.'
	
	return jsonify(response_object)

# Retrieving all current goals and adding new goals 
@app.route('/modGoals/<goal_template_id>', methods=['GET', 'POST'])
def all_goals(goal_template_id):
	response_object = {'status': 'success'}
	if request.method == 'POST':
		post_data = request.get_json()
		# Overwrite existing goal if number is identical
		remove_goal(post_data.get('goalNum'), goal_template_id)
		allGoals[goal_template_id].append({
			'goalNum': post_data.get('goalNum'),
			'goalTitle': post_data.get('goalTitle'),
			'completed': post_data.get('completed'),
			'inProgress': post_data.get('inProgress'),
		})

		response_object['message'] = 'Goal added!'
	else:
		response_object['goals'] = allGoals[goal_template_id]

	# Sort by goal number
	allGoals[goal_template_id].sort(key=lambda goal: goal['goalNum'])
	return jsonify(response_object)

@app.route('/completedGoals/<goal_template_id>', methods=['GET'])
def completed_goals(goal_template_id):
	response_object = {'status': 'success'}
	response_object['numCompleted'] = count_completed_goals(goal_template_id)
	return jsonify(response_object)

# Updating preexisting goals and deleting goals
@app.route('/modGoals/<goal_num>/<goal_template_id>', methods=['PUT', 'DELETE'])
def update_rem_goal(goal_num, goal_template_id):
	response_object = {'status': 'success'}
	if request.method == 'PUT':
		post_data = request.get_json()

		# Handles update, overwrites old goal number and overwrites new number
		remove_goal(goal_num, goal_template_id)
		remove_goal(post_data.get('goalNum'), goal_template_id)

		allGoals[goal_template_id].append({
			'goalNum': post_data.get('goalNum'),
			'goalTitle': post_data.get('goalTitle'),
			'completed': post_data.get('completed'),
		})

		response_object['message'] = 'Goal updated!'
	elif request.method == 'DELETE':
		remove_goal(goal_num, goal_template_id)
		response_object['message'] = 'Goal deleted!'
		
	# Sort by goal number
	allGoals[goal_template_id].sort(key=lambda goal: goal['goalNum'])

	return jsonify(response_object)

# Create new, blank template designated with goal_template_id
def create_template(goal_template_id):
	new_template = []
	allGoals[goal_template_id] = new_template

# Helper function to count number of completed goals in a template
def count_completed_goals(goal_template_id):
	completedGoalCount = 0

	for goal in allGoals[goal_template_id]:
		if goal['completed']:
			completedGoalCount += 1

	return completedGoalCount

# Helper fjunction to remove goal from a template
def remove_goal(goal_num, goal_template_id):
	for goal in allGoals[goal_template_id]:
		if int(goal['goalNum']) == int(goal_num):
			allGoals[goal_template_id].remove(goal)

if __name__ == "__main__":
	# Bind to PORT if defined, otherwise default to 5000.
	port = int(environ.get('PORT', 5000))
	# Run with Flask dev server or with Waitress WSGI server
	app.run(host='0.0.0.0', port=port)
	# serve(app, host='0.0.0.0', port=port)
