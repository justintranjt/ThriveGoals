from flask import Flask, jsonify, render_template, request, redirect, session
from flask_cas import CAS, login_required
from flask_sslify import SSLify
from flask_cors import CORS
from os import environ
from time import time
from waitress import serve
import updateDB
from goalObject import *

from flask.sessions import SessionInterface
from beaker.middleware import SessionMiddleware

session_opts = {
	'session.type': 'file',
	'session.cookie_expires': True,
	'session.data_dir': './data',
	'session.auto': True
}

class BeakerSessionInterface(SessionInterface):
	def open_session(self, app, request):
		session = request.environ['beaker.session']
		return session

	def save_session(self, app, session, response):
		session.save()

app = Flask(__name__, static_folder='./dist/static', template_folder='./dist')

#POTENTIALLY IMPORTANT: 
app.config.from_object(__name__)

# Initialize HTTPS redirection.
sslify = SSLify(app)

# Initialize CAS login
cas = CAS()
cas.init_app(app)
app.config['CAS_SERVER'] = 'https://fed.princeton.edu/cas/'
app.config['CAS_AFTER_LOGIN'] = 'login'
app.config['SESSION_TYPE'] = 'filesystem'

# This is a secret key for storing sessions.
secret_key = environ.get('SECRET_KEY', "developmentsecretkey")
app.secret_key = secret_key

# Initialize CORS
CORS(app, supports_credentials=True)

app.wsgi_app = SessionMiddleware(app.wsgi_app, session_opts)
app.session_interface = BeakerSessionInterface()

# Templates with references to objects and JSON representation
allTemplateRefsDict_by_User = {}
allTemplatesDict_by_User = {}

# See here for more info: http://flask.pocoo.org/snippets/57/
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
	return render_template("index.html")

# Set login netID
@app.route('/loginPage', methods=['GET'])
@login_required
def login():
	session['netID'] = cas.username

	# Initialize starter templates
	initTestTemplates(cas.username)

	# Bind to URIROOT if defined, otherwise default to localhost
	uriRoot = environ.get('URIROOT', "http://localhost:8080")
	return redirect(uriRoot + "/goals", code=302)

# Handle CAS login
@app.route('/loginNetID', methods=['GET'])
def loginNetID():
	response_object = {'status': 'success'}
	global allTemplateRefsDict_by_User
	global allTemplatesDict_by_User
	netID = session.get('netID', 'not set')
	
	response_object['netID'] = netID

	allTemplateRefsDict_by_User[netID] = {}
	allTemplatesDict_by_User[netID] = {}

	return jsonify(response_object)

# Mark goal as completed
@app.route('/completeGoal/<goal_ref>/<goal_template_id>', methods=['PUT'])
def cmpl_goal(goal_ref, goal_template_id):
	response_object = {'status': 'success'}
	global allTemplateRefsDict_by_User
	global allTemplatesDict_by_User
	netID = session.get('netID', 'not set')

	# Start template refs from clean slate each time
	allTemplateRefs = allTemplateRefsDict_by_User[netID]

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
	global allTemplateRefsDict_by_User
	global allTemplatesDict_by_User
	netID = session.get('netID', 'not set')

	# Start template refs from clean slate each time
	allTemplateRefs = allTemplateRefsDict_by_User[netID]

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
	global allTemplateRefsDict_by_User
	global allTemplatesDict_by_User
	netID = session.get('netID', 'not set')

	allTemplateRefs = allTemplateRefsDict_by_User[netID]
	allTemplates = allTemplatesDict_by_User[netID]

	if request.method == 'POST':
		post_data = request.get_json()
		parent = post_data.get('parentID')
		root = allTemplateRefs[goal_template_id]

		if parent is not None:
			curGoal = getGoalUsingTime(root, parent)
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
@app.route('/modGoals/<goal_num>/<goal_template_id>/<goal_ref>/<time>', methods=['PUT', 'DELETE'])
def update_rem_goal(goal_num, goal_template_id, goal_ref, time):
	response_object = {'status': 'success'}
	global allTemplateRefsDict_by_User
	netID = session.get('netID', 'not set')

	# Start template refs from clean slate each time
	allTemplateRefs = allTemplateRefsDict_by_User[netID]

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
		put_data.get('inProgress'), put_data.get('goalID'), put_data.get('time'))
		parent.insertSubgoalAtIndex(index, newGoal)
		prevGoal.deleteSelf()

		response_object['message'] = 'Goal updated!'

	elif request.method == 'DELETE':
		remove_goal(goal_num, goal_template_id, goal_ref)
		response_object['message'] = 'Goal deleted!'

	# Update local templates from database
	get_templates()

	return jsonify(response_object)

# Swap two specified goals in priority
@app.route('/swapGoal/<curr_goal_id>/<other_goal_id>/<goal_template_id>', methods=['PUT'])
def swap_goal(curr_goal_id, other_goal_id, goal_template_id):
	global allTemplateRefsDict_by_User
	netID = session.get('netID', 'not set')

	allTemplateRefs = allTemplateRefsDict_by_User[netID]

	# Get references to goals to be swapped
	currGoal = getGoalUsingTime(allTemplateRefs[goal_template_id], curr_goal_id)
	otherGoal = getGoalUsingTime(allTemplateRefs[goal_template_id], other_goal_id)

	# Force goal to swap with its neighbor
	if currGoal.getParent() != otherGoal.getParent():
		currGoalIndex = currGoal.getParent().getSubgoalList().index(currGoal)

		if currGoal == otherGoal.getParent():
			otherGoal = currGoal.getParent().getSubgoalAtIndex(currGoalIndex + 1)
		else:
			otherGoal = currGoal.getParent().getSubgoalAtIndex(currGoalIndex - 1)

		# Prevent strange bug with starting timer and then swapping goals down
		if (currGoal.getParent().getSubgoalList().index(otherGoal) == len(currGoal.getParent().getSubgoalList()) - 1 or
			currGoal.getParent().getSubgoalList().index(currGoal) - 1 == currGoal.getParent().getSubgoalList().index(otherGoal)):
			otherGoal = currGoal.getParent().getSubgoalAtIndex(currGoalIndex + 1)
		
	# Swap the two goals
	currGoal.swapSubgoalsNested(otherGoal)

	# Update local templates from database
	get_templates()

	return jsonify({'status': 'success'})


# Updating preexisting goals and deleting goals
@app.route('/updateTimer/<goal_template_id>/<goal_ref>/<new_time>', methods=['PUT'])
def update_goal_time(goal_template_id, goal_ref, new_time):
	response_object = {'status': 'success'}
	global allTemplateRefsDict_by_User
	netID = session.get('netID', 'not set')

	# Start template refs from clean slate each time
	allTemplateRefs = allTemplateRefsDict_by_User[netID]

	# Update goal time
	if request.method == 'PUT':
		put_data = request.get_json()
		prevGoal = getGoalUsingTime(allTemplateRefs[goal_template_id], goal_ref)

		# TODO Keep this handy piece of code in mind for future methods
		parent = prevGoal.getParent()
		parentList = parent.getSubgoalList()
		index = parentList.index(prevGoal)
		subgoals = prevGoal.getSubgoalList()

		newGoal = Goal(put_data.get('goalTitle'), put_data.get('completed'), subgoals, parent, netID,
		put_data.get('inProgress'), put_data.get('goalID'), new_time)
		parent.insertSubgoalAtIndex(index, newGoal)
		prevGoal.deleteSelf()
		response_object['message'] = 'Goal updated!'

	get_templates()

	return jsonify(response_object)

# Get all existing template IDs
@app.route('/getTemplates', methods=['GET'])
def get_templates():
	response_object = {'status': 'success'}
	global allTemplateRefsDict_by_User
	global allTemplatesDict_by_User
	netID = session.get('netID', 'not set')

	# Start template refs from clean slate each time
	allTemplateRefs = {}
	allTemplates = {}

	# Get templates and load into template list
	for currTemplate in updateDB.getTemplateList(netID)[2]:
		allTemplateRefs[currTemplate[1]] = currTemplate[2]
		allTemplates[currTemplate[1]] = makeGoalDict_fromTemplate(currTemplate[2], 0, True)

	response_object['goalTemplateIDs'] = list(allTemplates.keys())
	
	allTemplateRefsDict_by_User[netID] = allTemplateRefs
	allTemplatesDict_by_User[netID] = allTemplates

	return jsonify(response_object)

# Create new, blank template designated with goal_template_id
@app.route('/modTemplates/<goal_template_id>', methods=['DELETE', 'PUT', 'POST'])
def update_template(goal_template_id):
	response_object = {'status': 'success'}
	global allTemplateRefsDict_by_User
	global allTemplatesDict_by_User
	netID = session.get('netID', 'not set')

	allTemplateRefs = allTemplateRefsDict_by_User[netID]
	allTemplates = allTemplatesDict_by_User[netID]

	# Delete current template
	if request.method == 'DELETE':
		updateDB.deleteTemplate(netID, goal_template_id)

	# Update existing template name and remove old entry ID
	elif request.method == 'PUT':
		put_data = request.get_json()
		new_template_id = put_data.get('newTemplateID')
		#Potential Buggos Hiding Here
		allTemplates.pop(goal_template_id)
		allTemplateRefs[goal_template_id].setGoalContent(new_template_id)
		allTemplateRefs[new_template_id] = allTemplateRefs.pop(goal_template_id)

	# Create new template with specified name
	elif request.method == 'POST':
		new_template_id = goal_template_id
		Goal(new_template_id, False, [], None, netID, False, '', 0)

	# Update local templates from database
	get_templates()

	return jsonify(response_object)

# Helper function to count number of completed goals in a template
def count_completed_goals(goal_template_id):
	global allTemplateRefsDict_by_User
	global allTemplatesDict_by_User
	netID = session.get('netID', 'not set')

	allTemplates = allTemplatesDict_by_User[netID]

	completedGoalCount = 0

	for goal in allTemplates[goal_template_id]:
		if goal['completed']:
			completedGoalCount += 1

	return completedGoalCount

# Helper function to remove goal from a template
def remove_goal(goal_num, goal_template_id, goal_ref):
	global allTemplateRefsDict_by_User
	global allTemplatesDict_by_User
	netID = session.get('netID', 'not set')
	
	allTemplateRefs = allTemplateRefsDict_by_User[netID]
	allTemplates = allTemplatesDict_by_User[netID]

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

# Test templates initialized for first-time users
def initTestTemplates(netID):
	# If user has no templates, insert the 3 default templates
	if not len(updateDB.getTemplateList(netID)[2]):
		# Make empty templates
		templateOne = Goal('Writing Sem Goal Template', False, [], None, netID, False, '', 0)
		templateTwo = Goal('COS 126 Assignment 2 Template', False, [], None, netID, False, '', 0)
		templateThree = Goal('COS 126 Assignment 3 Template', False, [], None, netID, False, '', 0)

		# Add goals to templates
		templateOne.addSubgoal("Read and mark up primary articles", False, False, time())
		nestOne = templateOne.addSubgoal("Gather quotes from articles in Word", False, False, time())
		nestOne.addSubgoal("Highlight most significant quotes", False, False, time())
		nestOne.addSubgoal("Trim down quotes", False, False, time())
		nestTwo = templateOne.addSubgoal("Locate relevant outside articles", False, False, time())
		nestTwo.addSubgoal("Read", False, False, time())
		nestTwo.addSubgoal("Annotate", False, False, time())
		nestThree = templateOne.addSubgoal("Extract quotes which relate to quotes from main articles", False, False, time())
		nestThree.addSubgoal("Trim down quotes", False, False, time())
		templateOne.addSubgoal("Arrange quotes under headings based on relevance and relation to each other", False, False, time())
		templateOne.addSubgoal("Eliminate all quotes which are not significantly connected to most other quotes", False, False, time())
		templateOne.addSubgoal("Write analysis which connects chosen quotes", False, False, time())
		templateOne.addSubgoal("Rearrange and fine-tune analysis", False, False, time())
		templateOne.addSubgoal("Determine main ideas of argument and motivating questions", False, False, time())
		templateOne.addSubgoal("Fill in any research gaps(i.e. find more sources)", False, False, time())
		nestFour = templateOne.addSubgoal("Re-organize paper to reflect argument structure", False, False, time())
		nestFour.addSubgoal("Clearly articulate the motivating questions and your answers in the beginning of the paper", False, False, time())
		nestFour.addSubgoal("Write conclusion which restates and extends your stated hypothesis", False, False, time())
		templateOne.addSubgoal("Extend source based argument to include new original frameworks and ideas", False, False, time())
		templateOne.addSubgoal("Address significance and implications of argument", False, False, time())
		templateOne.addSubgoal("Create works cited", False, False, time())
		templateOne.addSubgoal("Proofread out loud", False, False, time())
		templateOne.addSubgoal("Submit", False, False, time())

		templateTwo.addSubgoal("Find relevant material from the course web page", False, False, time())	
		templateTwo.addSubgoal("Edit, compile, and execute a few short Java programs", False, False, time())
		templateTwo.addSubgoal("Submit pertinent files to Tigerhub", False, False, time())

		templateThree.addSubgoal("Edit appropriate programs", False, False, time())
		templateThree.addSubgoal("Declare and initialize variables", False, False, time())
		templateThree.addSubgoal("Use arithmetric and boolean expressions", False, False, time())
		templateThree.addSubgoal("Use conditionals and loops", False, False, time())
		templateThree.addSubgoal("Nest conditionals and loops", False, False, time())
		templateThree.addSubgoal("Debug code", False, False, time())
		templateThree.addSubgoal("Submit pertinent files to Tigerhub", False, False, time())

		get_templates()

	# If user has existing templates, do not insert default templates
	else:
		get_templates()

	# Delete templates
	# updateDB.deleteTemplate(netID, 'Template 1')

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
			'goalID': str(currTemplate.getUniqueID()),
			'goalNum': 0,
			'goalTitle': currTemplate.getGoalContent(),
			'completed': currTemplate.getCompletionStatus(),
			'inProgress': currTemplate.getInProgress(),
			'isSubgoal': isSubgoal,
			'nestLevel': nestLevel, # should be 0,1,2
			'parentID': str(currTemplate.getParent().getUniqueID()),
			'goalTime': currTemplate.getTime(),
		}]

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

# Function for mapping frontend goal representations to backend object references
def getGoalUsingTime(curNode, var):
	retNode = None

	if (str(curNode.getUniqueID()).strip()) == (str(var).strip()):
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
	for i in range(0, indent):
		string += '     '
	string += str(curGoal)
	print(string)
	if curGoal.getSubgoalList() is not None:
		for subgoal in curGoal.getSubgoalList():
			printTree(subgoal, indent + 1)

if __name__ == "__main__":
	# Bind to PORT if defined, otherwise default to 5000.
	port = int(environ.get('PORT', 5000))
	# Run with Flask dev server or with Waitress WSGI server
	# app.run(host='0.0.0.0', port=port)
	serve(app, host='0.0.0.0', port=port)
