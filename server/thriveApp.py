from flask import Flask, jsonify, render_template, request, redirect
from flask_cas import CAS, login_required
from flask_sslify import SSLify
from flask_cors import CORS
from os import environ
from time import time
from waitress import serve
import updateDB
from goalObject import *
import jsonpickle

app = Flask(__name__, static_folder='./dist/static', template_folder='./dist')
app.config.from_object(__name__)

# Initialize HTTPS redirection.
# sslify = SSLify(app)

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

# Templates with references to objects and JSON representation
allTemplateRefs = {}
allTemplates = {}

# Username
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
	global allTemplateRefs
	global allTemplates

	for index, goal in enumerate(allTemplates[goal_template_id]):
		if int(goal['goalNum']) == int(goal_num):
			if goal['completed']:
				# Goal nums are 1-indexed, so substract 1
				allTemplateRefs[goal_template_id].getSubgoalAtIndex(int(goal_num) - 1).setCompletionStatus(False)
				response_object['message'] = 'Goal not completed.'
			else:
				# Goal nums are 1-indexed, so substract 1
				allTemplateRefs[goal_template_id].getSubgoalAtIndex(int(goal_num) - 1).setCompletionStatus(True)
				response_object['message'] = 'Goal completed!'

	# Update local templates from database
	get_templates()
	
	return jsonify(response_object)

# Mark goal as inProgress
@app.route('/inProgGoal/<goal_num>/<goal_template_id>', methods=['PUT'])
def in_prog_goal(goal_num, goal_template_id):
	response_object = {'status': 'success'}
	global allTemplateRefs
	global allTemplates

	for goal in allTemplates[goal_template_id]:
		if int(goal['goalNum']) == int(goal_num):
			if goal['completed']:
				# Goal nums are 1-indexed, so substract 1
				allTemplateRefs[goal_template_id].getSubgoalAtIndex(int(goal_num) - 1).setCompletionStatus(False)
				response_object['message'] = 'Goal is in progress.'
			if goal['inProgress']:
				# Goal nums are 1-indexed, so substract 1
				allTemplateRefs[goal_template_id].getSubgoalAtIndex(int(goal_num) - 1).setInProgress(False)
				response_object['message'] = 'Goal is not in progress.'
			else:
				# Goal nums are 1-indexed, so substract 1
				allTemplateRefs[goal_template_id].getSubgoalAtIndex(int(goal_num) - 1).setInProgress(True)
				response_object['message'] = 'Goal is in progress.'
	
	# Update local templates from database
	get_templates()

	return jsonify(response_object)

# Retrieving all current goals and adding new goals 
@app.route('/modGoals/<goal_template_id>', methods=['GET', 'POST'])
def all_goals(goal_template_id):
	response_object = {'status': 'success'}
	global allTemplates
	global allTemplateRefs

	print("Printing out contents of allTemplates")
	for each in allTemplates:
		 print(str(each))


	if request.method == 'POST':
		post_data = request.get_json()

		allTemplateRefs[goal_template_id].addSubgoal(
			post_data.get('goalTitle'),
			post_data.get('completed'),
		)
		response_object['message'] = 'Goal added!'
	else:
		response_object['goals'] = allTemplates[goal_template_id]

	# Sort by goal number
	allTemplates[goal_template_id].sort(key=lambda goal: goal['goalNum'])

	# Update local templates from database
	get_templates()

	return jsonify(response_object)

# Retrieve number of completed goals
@app.route('/completedGoals/<goal_template_id>', methods=['GET'])
def completed_goals(goal_template_id):
	response_object = {'status': 'success'}
	response_object['numCompleted'] = count_completed_goals(goal_template_id)
	return jsonify(response_object)

# Updating preexisting goals and deleting goals
@app.route('/modGoals/<goal_num>/<goal_template_id>', methods=['PUT', 'DELETE'])
def update_rem_goal(goal_num, goal_template_id):
	response_object = {'status': 'success'}
	global allTemplateRefs
	global allTemplates

	if request.method == 'PUT':
		put_data = request.get_json()

		# Handles update, overwrites old goal number and overwrites new number
		remove_goal(goal_num, goal_template_id)
		remove_goal(put_data.get('goalNum'), goal_template_id)

		allTemplates[goal_template_id].append({
			'goalNum': put_data.get('goalNum'),
			'goalTitle': put_data.get('goalTitle'),
			'completed': put_data.get('completed'),
			'inProgress': put_data.get('inProgress'),
		})

		response_object['message'] = 'Goal updated!'
	elif request.method == 'DELETE':
		remove_goal(goal_num, goal_template_id)
		response_object['message'] = 'Goal deleted!'
		
	# Sort by goal number
	allTemplates[goal_template_id].sort(key=lambda goal: goal['goalNum'])

	# Update local templates from database
	get_templates()

	return jsonify(response_object)

# Get all existing template IDs
@app.route('/getTemplates', methods=['GET'])
def get_templates():
	response_object = {'status': 'success'}
	global allTemplateRefs
	global allTemplates
	global netID

	# Start template refs from clean slate each time
	allTemplateRefs = {}
	allTemplates = {}
	# Get templates and load into template list
	print("\n\n\n\n\n\n\n")
	print("get_templates has been called:  ")
	print("Here are the contents of the templateList from the database: ")
	print(updateDB.getTemplateList(netID)[2])
	print("")
	for currTemplate in updateDB.getTemplateList(netID)[2]:
		allTemplateRefs[currTemplate[1]] = currTemplate[2]
		allTemplates[currTemplate[1]] = makeGoalDict_fromTemplate(currTemplate[2], 0, True)

	print("\n\n")
	print("Printing out contents of allTemplateRefs")
	for each in allTemplateRefs:
		print("Key: "+str(each) + "| Value: "+ str(allTemplateRefs[each]))
	print("\n\n")
	print("Printing out contents of allTemplates")
	for each in allTemplates:
		print("Key: "+str(each) + "| Value: "+ str(allTemplates[each]))
	print("\n\n\n\n\n\n\n")

	response_object['goalTemplateIDs'] = list(allTemplates.keys())

	return jsonify(response_object)

# Create new, blank template designated with goal_template_id
@app.route('/modTemplates/<goal_template_id>', methods=['DELETE', 'PUT', 'POST'])
def update_template(goal_template_id):
	response_object = {'status': 'success'}
	global allTemplates
	global allTemplateRefs
	global netID

	# print("We are in the modify templates method")

	# Delete current template
	if request.method == 'DELETE':
		updateDB.deleteTemplate(netID, goal_template_id)

	#Update existing template name and remove old entry ID
	elif request.method == 'PUT':
		print("made it into the elif")
		put_data = request.get_json()
		new_template_id = put_data.get('newTemplateID')
		# TODO must fix the line below to use updateTemplateName()
		allTemplates.pop(goal_template_id) 
		allTemplateRefs[goal_template_id].setGoalContent(new_template_id)
		allTemplateRefs[str(new_template_id)] = allTemplateRefs.pop(goal_template_id)
		# allTemplateRefs[str(new_template_id)] = new_ref
		#allTemplates[new_template_id] 
		# print("Printing out contents of allTemplateRefs")
		# for each in allTemplateRefs:
		#  	print(str(each))
		# print(updateDB.getTemplateList(netID)[2])
		# updateDB.deleteTemplate(netID, goal_template_id)

	# Create new template with specified name
	elif request.method == 'POST':
		new_template_id = goal_template_id
		Goal(new_template_id, False, [], None, netID, False)


	# Update local templates from database
	get_templates()
	# print("Printing out contents of allTemplateRefs")
	# for each in allTemplateRefs:
	# 	print(str(each))
	# print("Printing out contents of database for this user: ")
	# print(updateDB.getTemplateList(netID)[2])
	# print("Printing out contents of allTemplates")
	# for each in allTemplates:
	# 	 print(str(each))


	return jsonify(response_object)

# Helper function to count number of completed goals in a template
def count_completed_goals(goal_template_id):
	get_templates()
	global allTemplates

	completedGoalCount = 0

	print("\n\n\n\n\n\n\n")
	print("count_completed_goals has been called:  ")
	print("Here are the contents of the templateList from the database: ")
	print(updateDB.getTemplateList(netID)[2])
	print("")
	print("\n\n")
	print("Printing out contents of allTemplateRefs")
	for each in allTemplateRefs:
		print("Key: "+str(each) + "| Value: "+ str(allTemplateRefs[each]))
	print("\n\n")
	print("Printing out contents of allTemplates")
	for each in allTemplates:
		print(each)
		print("Key: "+str(each) + "| Value: "+ str(allTemplates[each]))
	print("\n\n\n\n\n\n\n")


	# strQuery = jsonpickle.encode("Template")
	# strQuery = jsonpickle.decode(strQuery)
	# print("Testing line 275: "+str(allTemplates[strQuery]))
	for goal in allTemplates[goal_template_id]:
		if goal['completed']:
			completedGoalCount += 1

	return completedGoalCount

# Helper function to remove goal from a template
def remove_goal(goal_num, goal_template_id):
	global allTemplates
	global allTemplateRefs

	for goal in allTemplates[goal_template_id]:
		removed = False
		# Remove using removeSubgoalAtIndex() method
		if goal['goalNum'] == int(goal_num):
			allTemplates[goal_template_id].remove(goal)
			# Goal nums are 1-indexed, so substract 1
			allTemplateRefs[goal_template_id].removeSubgoalAtIndex(int(goal_num) - 1)
			removed = True
		# Decrement all goalNums greater than removed goalNum
		if removed:
			for goal in allTemplates[goal_template_id]:
				if goal['goalNum'] > int(goal_num):
					goal['goalNum'] -= 1
		
def initTestTemplates():
	global netID
	# Make empty templates
	templateOne = Goal('Template 1', False, [], None, netID, False)
	templateTwo = Goal('Template 2', False, [], None, netID, False)

	# Add goals to templates
	templateOne.addSubgoal("Finish basic addition of goals", False)
	templateOne.addSubgoal("Allow goal editing", False)
	templateOne.addSubgoal("Allow goal deletion", False)
	templateTwo.addSubgoal("Alternate template!", False)

	# Delete templates
	# updateDB.deleteTemplate(netID, 'Template 1')
	# updateDB.deleteTemplate(netID, 'Template 2')

# Helper function to create JSON representation from template obj reference
def makeGoalDict_fromTemplate(currTemplate, nestLevel, isFirst):  
	isSubgoal = False
	if currTemplate.getParent() is currTemplate.getTemplate():
		isSubgoal = False
	else:
		isSubgoal = True

	if isFirst:
		curlist = []
	else: 
		curlist = [{
			'goalID': time(),
			'goalNum': 0,
			'goalTitle': currTemplate.getGoalContent(),
			'completed': currTemplate.getCompletionStatus(),
			'inProgress': currTemplate.getInProgress(),
			'isSubgoal': isSubgoal,
			'nestLevel': nestLevel, # should be 0,1,2
			'parentID': currTemplate.getParent().getGoalContent(),
		}]

	retList = []
	if currTemplate.getSubgoalList() is not None:
		for subgoal in currTemplate.getSubgoalList():
			retList.extend(makeGoalDict_fromTemplate(subgoal, (nestLevel + 1), False ))

	curlist.extend(retList)

	numCounter = 1
	for each in curlist:
		each['goalNum'] = numCounter
		numCounter += 1

	return curlist

if __name__ == "__main__":
	initTestTemplates()
	# Bind to PORT if defined, otherwise default to 5000.
	port = int(environ.get('PORT', 5000))
	# Run with Flask dev server or with Waitress WSGI server
	app.run(host='0.0.0.0', port=port)
	# serve(app, host='0.0.0.0', port=port)
