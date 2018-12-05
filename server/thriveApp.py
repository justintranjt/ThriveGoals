from flask import Flask, jsonify, render_template, request, redirect
from flask_cas import CAS, login_required
from flask_sslify import SSLify
from flask_cors import CORS
from os import environ
from time import time
from waitress import serve
import updateDB
from goalObject import *
import difflib

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
@app.route('/completeGoal/<goal_ref>/<goal_template_id>', methods=['PUT'])
def cmpl_goal(goal_ref, goal_template_id):
	response_object = {'status': 'success'}
	global allTemplateRefs
	global allTemplates

	curGoal = getGoalUsingTime(allTemplateRefs[goal_template_id], goal_ref)
	if(curGoal.getCompletionStatus()):
		curGoal.setCompletionStatus(False)
		response_object['message'] = 'Goal not completed.'
	else:
		curGoal.setCompletionStatus(True)
		response_object['message'] = 'Goal completed!'

	# Update local templates from database
	get_templates()

	return jsonify(response_object)

# Mark goal as inProgress
@app.route('/inProgGoal/<goal_ref>/<goal_template_id>', methods=['PUT'])
def in_prog_goal(goal_ref, goal_template_id):
	response_object = {'status': 'success'}
	global allTemplateRefs
	global allTemplates

	curGoal = getGoalUsingTime(allTemplateRefs[goal_template_id], goal_ref)
	if(curGoal.getInProgress()):
		curGoal.setInProgress(False)
		response_object['message'] = 'Goal not in progress.'
	else:
		curGoal.setInProgress(True)
		response_object['message'] = 'Goal in progress!'


	# Update local templates from database
	get_templates()

	return jsonify(response_object)



# Retrieving all current goals and adding new goals
@app.route('/modGoals/<goal_template_id>', methods=['GET', 'POST'])
def all_goals(goal_template_id):
	response_object = {'status': 'success'}
	global allTemplates
	global allTemplateRefs

	if request.method == 'POST':
		post_data = request.get_json()


		parent = post_data.get('parentID')

		# print("\n\n\n\nIn add Subgoal, parent id is: "+str(parent))
		root = allTemplateRefs[goal_template_id]
		# print()
		# print("rootnode is: "+str(root))
		# print()

		if parent is not None:

			curGoal = getGoalUsingTime(root, parent)

			# print(str(curGoal))
			curGoal.addSubgoal(
				post_data.get('goalTitle'),
				post_data.get('completed'),
				False,
				time(),
			)
			response_object['message'] = 'Goal added!'
		else:
			root.addSubgoal(
				post_data.get('goalTitle'),
				post_data.get('completed'),
				False,
				time(),
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
@app.route('/modGoals/<goal_num>/<goal_template_id>/<goal_ref>', methods=['PUT', 'DELETE'])
def update_rem_goal(goal_num, goal_template_id, goal_ref):
	response_object = {'status': 'success'}
	global allTemplateRefs
	global allTemplates

	# Update goal title
	if request.method == 'PUT':
		put_data = request.get_json()
		prevGoal = getGoalUsingTime(allTemplateRefs[goal_template_id], goal_ref)

		# TODO Keep this handy piece of code in mind for future methods
		parent = prevGoal.getParent()
		parentList = parent.getSubgoalList()
		index = parentList.index(prevGoal)
		subgoals = prevGoal.getSubgoalList()


		newGoal = Goal(put_data.get('goalTitle'), put_data.get('completed'), subgoals, parent, netID,
			put_data.get('inProgress'), put_data.get('goalID'))
		parent.insertSubgoalAtIndex(index, newGoal)
		prevGoal.deleteSelf()
		# prevRef.deleteSelf()

		response_object['message'] = 'Goal updated!'

	elif request.method == 'DELETE':
		remove_goal(goal_num, goal_template_id, goal_ref)
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
	for currTemplate in updateDB.getTemplateList(netID)[2]:
		allTemplateRefs[currTemplate[1]] = currTemplate[2]
		allTemplates[currTemplate[1]] = makeGoalDict_fromTemplate(currTemplate[2], 0, True)

	response_object['goalTemplateIDs'] = list(allTemplates.keys())

	return jsonify(response_object)

# Create new, blank template designated with goal_template_id
@app.route('/modTemplates/<goal_template_id>', methods=['DELETE', 'PUT', 'POST'])
def update_template(goal_template_id):
	response_object = {'status': 'success'}
	global allTemplates
	global allTemplateRefs
	global netID

	# Delete current template
	if request.method == 'DELETE':
		updateDB.deleteTemplate(netID, goal_template_id)

	# Update existing template name and remove old entry ID
	elif request.method == 'PUT':
		put_data = request.get_json()
		new_template_id = put_data.get('newTemplateID')

		allTemplates.pop(goal_template_id)
		allTemplateRefs[goal_template_id].setGoalContent(new_template_id)
		allTemplateRefs[new_template_id] = allTemplateRefs.pop(goal_template_id)

	# Create new template with specified name
	elif request.method == 'POST':
		new_template_id = goal_template_id
		Goal(new_template_id, False, [], None, netID, False, '')


	# Update local templates from database
	get_templates()

	return jsonify(response_object)

# Helper function to count number of completed goals in a template
def count_completed_goals(goal_template_id):
	get_templates()
	global allTemplates

	completedGoalCount = 0

	for goal in allTemplates[goal_template_id]:
		if goal['completed']:
			completedGoalCount += 1

	return completedGoalCount

# Helper function to remove goal from a template
def remove_goal(goal_num, goal_template_id, goal_ref):
	global allTemplates
	global allTemplateRefs

	curGoal = getGoalUsingTime(allTemplateRefs[goal_template_id], goal_ref)

	for goal in allTemplates[goal_template_id]:
		removed = False
		# Remove using removeSubgoalAtIndex() method

		if goal['goalNum'] == int(goal_num):
			curGoal.deleteSelf()
			removed = True
		# Decrement all goalNums greater than removed goalNum
		if removed:
			for goal in allTemplates[goal_template_id]:
				if goal['goalNum'] > int(goal_num):
					goal['goalNum'] -= 1
			return None

def initTestTemplates():
	global netID
	# Make empty templates
	templateOne = Goal('Template 1', False, [], None, netID, False, '')
	templateTwo = Goal('Template 2', False, [], None, netID, False, '')

	# Add goals to templates
	templateOne.addSubgoal("Finish basic addition of goals", False, False, time())
	templateOne.addSubgoal("Allow goal editing", False, False, time())
	templateOne.addSubgoal("Allow goal deletion", False, False, time())
	templateTwo.addSubgoal("Alternate template!", False, False, time())

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
			'goalID':  str(currTemplate.getUniqueID()),
			'goalNum': 0,
			'goalTitle': currTemplate.getGoalContent(),
			'completed': currTemplate.getCompletionStatus(),
			'inProgress': currTemplate.getInProgress(),
			'isSubgoal': isSubgoal,
			'nestLevel': nestLevel, # should be 0,1,2
			'parentID': str(currTemplate.getParent().getUniqueID()),
		}]
		# print()
		# print("Inside loop in makeGoalDict_fromTemplate ")
		# print("Goal Content: "+str(currTemplate.getGoalContent()))
		# print("nestLevel: "+ str(nestLevel))
		# print("Goal Id: "+str(currTemplate.getUniqueID()))
		# print("parentID: "+str(currTemplate.getParent().getUniqueID()))
		# print()

	retList = []
	if currTemplate.getSubgoalList() is not None:
		for subgoal in currTemplate.getSubgoalList():
			retList.extend(makeGoalDict_fromTemplate(subgoal, (nestLevel + 1), False))

	curlist.extend(retList)

	numCounter = 1
	for each in curlist:
		each['goalNum'] = numCounter
		numCounter += 1

	return curlist

#function for mapping frontend goal representations to backend object references
def getGoalUsingTime(curNode, var):
	#note that the rootnode is just refferring to the template
	retNode = None
	# print("\n\ncurNode's ID number in getGoalUsingTime: ")
	# print(str(curNode.getGoalContent()))
	# print(str(curNode.getUniqueID()).strip())
	# print(str(var).strip())
	# print("Strings are equal:"+str(curNode.getUniqueID()).strip() == (str(var).strip()))

	if (str(curNode.getUniqueID()).strip()) == (str(var).strip()):
			# print("We found a matching node in getGoalUsingTime!!!")
			retNode = curNode
			return retNode
	for eachNode in curNode.getSubgoalList():
		potentialVal = getGoalUsingTime(eachNode, var)
		if potentialVal is not None:
			retNode = potentialVal
	return retNode


# special debugging method
def printTree(curGoal, indent):
    string = ''
    for i in range(0,indent):
        string += '     '
    string += str(curGoal)
    print (string)
    if curGoal.getSubgoalList() is not None:
	    for subgoal in curGoal.getSubgoalList():
	        printTree(subgoal, indent + 1)

# special debugging method
def printTree(curGoal, indent):
    string = ''
    for i in range(0,indent):
        string += '     '
    string += str(curGoal)
    print (string)
    if curGoal.getSubgoalList() is not None:
	    for subgoal in curGoal.getSubgoalList():
	        printTree(subgoal, indent + 1)

if __name__ == "__main__":
	initTestTemplates()
	# Bind to PORT if defined, otherwise default to 5000.
	port = int(environ.get('PORT', 5000))
	# Run with Flask dev server or with Waitress WSGI server
	app.run(host='0.0.0.0', port=port)
	# serve(app, host='0.0.0.0', port=port)
