from flask import Flask, jsonify, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_cas import CAS, login_required
from flask_sslify import SSLify
from flask_cors import CORS
import os

app = Flask(__name__, static_folder='./dist/static', template_folder='./dist')
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

# This is a secret key for storing sessions. 
secret_key = os.environ.get('SECRET_KEY', "developmentsecretkey")
app.secret_key = secret_key

# Initialize CORS
CORS(app)

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
	},
]
# Using completed goals as a global variable
completedGoals = 0

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
	uriRoot = os.environ.get('URIROOT', "http://localhost:8080")
	return redirect(uriRoot + "/goals", code=302)

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
			global completedGoals
			completedGoals += 1
	
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
		if post_data.get('completed'):
			global completedGoals
			completedGoals += 1

		response_object['message'] = 'Goal added!'
	else:
		response_object['goals'] = goals

	# Sort by goal number
	goals.sort(key=lambda goal: goal['goalNum'])
	return jsonify(response_object)

@app.route('/completedGoals', methods=['GET'])
def completed_goals():
	response_object = {'status': 'success'}
	response_object['numCompleted'] = completedGoals
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
		if post_data.get('completed'):
			global completedGoals
			completedGoals += 1

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
			if goal['completed']:
				global completedGoals
				completedGoals -= 1

if __name__ == "__main__":
	# Bind to PORT if defined, otherwise default to 5000.
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port)
