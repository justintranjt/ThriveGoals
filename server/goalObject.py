#!/usr/bin/env python

#-----------------------------------------------------------------------
# goalObject.py
# Author: Josh Gardner, Hamza Mahmood
#-----------------------------------------------------------------------


import jsonpickle
import psycopg2
from updateDB import updateTemplate, updateTemplateName

class Goal (object):

	#initializes a new goal
	#adding additional fields to allow for easier evolution
	def __init__(self, goalContent, completionStatus, initialSubgoals, parent, user, inProgress):
		#string containing the actual content of a goal
		self._goalContent = goalContent
		#boolean: true if goal complete, else false
		self._completionStatus = completionStatus
		#list of goal objects
		self._subgoals = initialSubgoals
		# parent Node, returns goal object
		self._parent = parent

		#username that the template belongs to
		self._user = user

		#in progress status 
		self._inProgress = inProgress

		
		#Not sure why we have these, but Dr. Dondero recommended we have them for some reason
		#just in case we add fields later. Apparently, it would be a major logistical challenge
		# self._extraField1 = None

		# self._extraField2 = None

		# self._extraField3 = None


		self.updateDatabase()



	# returns goal as string representation containing goal content and completion status
	def __str__(self):
		retStr = 'Goal Name: '+ str(self._goalContent)+ ' | Completion Status:'+ str(self._completionStatus)
		return retStr

	# returns the parent, which should be another goal Object
	def getParent(self):
		return self._parent

	
	

	# removes goal from its current position and moves it to the subgoals list of the 
	#new parent 
	def setParent(self, newParent):
		if self._parent != None and self._parent != newParent: # there is already a current parent (so overwrite)
			self._parent.removeSubgoal(self)					# and if its the same parent being set, just set it as below.
			self._parent = newParent
		# not enough -- need to add the goal to the parent's subgoals
			self._parent.addSubgoal(self)
		else:
			self._parent = newParent
		self.updateDatabase()



	#returns the template(a goal object) the goal belongs to if it is a goal
	#if it is the root Node,i.e. the template, this method returns the calling object
	def getTemplate(self):
		current = self._parent
		previous = None
		while current is not None:
			previous = current
			current = current.getParent()
		if previous == None:
			return self
		else:
			return previous

	def getUser(self):
		return self._user

	def setInProgress(self, bool):
		self._inProgress = bool
		self.updateDatabase()

	def getInProgress(self):
		return self._inProgress 

	def updateDatabase(self):
		template = self.getTemplate()
		name = template.getGoalContent()
		user = template.getUser()
		jsonStr = template.toJSON()
		updateTemplate(user, name, jsonStr)



	# returns the goal content, which should be a string
	def getGoalContent(self):
		return self._goalContent

	#updates the string containing goal content for the current goal
	def setGoalContent(self, newContent):
		self._goalContent = newContent
		if self.getParent is None:
			json = self.toJSON()
			userName = self.getUser()
			deleteTemplate()
		self.updateDatabase()
		


	#returns the completions status of the current goal object
	def getCompletionStatus(self):
		return self._completionStatus


	# updates the boolean completion status of this goal object
	def setCompletionStatus(self, newStatus):
		self._completionStatus = newStatus
		self.updateDatabase()


	#returs a list of goal objects
	def getSubgoalList(self):
		return self._subgoals

	# overwrites the existing list of subgoals(a list of goal objects)
	# with newSubgoals(another list of goal objects)
	def setSubgoalList(self, newSubgoals):
		self._subgoals = newSubgoals
		for subgoal in self._subgoals: # also need to make sure parent property is set.
			subgoal.setParent(self)
		self.updateDatabase()


	#appends a new subgoal to the end of the subgoals list for this goal
	def _addSubgoal(self, newSubgoal):
		current = self._subgoals
		if (current == None):
			current = []
		current.append(newSubgoal)
		self._subgoals = current
		self.updateDatabase()

	#appends a new subgoal to the end of the subgoals list for this goal
	def addSubgoal(self, goalString):
		newGoal = Goal(goalString, False, [], self, self._user, False)
		self._addSubgoal(newGoal)
		return newGoal 



	def removeSubgoal(self, subgoal):
		current = self._subgoals
		i = 0
		while i < len(current): # find the subgoal to remove
			if subgoal == current[i]:
				current.remove(subgoal)
				break
			i = i + 1
		self.updateDatabase()


	#takes an integer named index and a string named newSubgoal
	#inserts the newSubgoal into the subgoals list at the index specified
	def insertSubgoalAtIndex(self, index, newSubgoal):
		#newSubgoal = Goal(newSubgoal, False, [], self)
		current = self._subgoals
		current.insert(index, newSubgoal)
		self._subgoals = current
		self.updateDatabase()


	#takes an integer named index, removes the subgoal at that index
	def removeSubgoalAtIndex(self, index):   # what exactly is the index ...
		current = self._subgoals
		current.pop(index)
		self._subgoals = current
		self.updateDatabase()

	#takes an integer named index, returns the subgoal at that index
	def getSubgoalAtIndex(self, index):
		return self._subgoals[index]


	#only works within one level
	def swapSubGoals(self, index1, index2):
		temp1 = self._subgoals[index1]
		temp2 = self._subgoals[index2]
		self._subgoals[index1] = temp2
		self._subgoals[index2] = temp1
		self.updateDatabase()

	# literally just chages the parent reference 
	def set_Parent_For_Swap_Nested(self, newParent):
		self._parent = newParent
		self.updateDatabase()

	# swaps subgoals between arbitrary nesting levels 
	def swapSubgoalsNested(self, other):
		
		selfParent = self.getParent()
		otherParent = other.getParent()

		if selfParent != None:
			selfList = selfParent.getSubgoalList()
			selfIndex = selfList.index(self)


		else: # if it is the root node (only case when parent is null)
			selfList = selfParent
			selfIndex = 0


		if otherParent != None:
			otherList = otherParent.getSubgoalList()
			otherIndex = otherList.index(other)
		else:
			otherList = otherParent
			otherIndex = 0


		other.set_Parent_For_Swap_Nested(selfParent)
		selfList[selfIndex] = other   # overwrites self with the other at self's index in the subgoal list.

		self.set_Parent_For_Swap_Nested(otherParent)
		otherList[otherIndex] = self

		self.updateDatabase()



	#if all the goals in the subgoals list are marked complete, then the goal is also complete
	#else the goal is still incomplete. Note this implementation technically misses complex cases
	# that occur with arbitrary nesting, where a goal should technically be complete, but one of its
	# subgoals hasn't been marked compolete yet
	def update_Completion_Using_Subgoals(self):
		goalsList = self._subgoals
		for eachGoal in goalsList:
			if (eachGoal.getCompletionStatus() == False):
				self._completionStatus = False
				self.updateDatabase()
				return False
		self._completionStatus = True
		self.updateDatabase()
		return True

		#removes the calling goal from the tree
	def deleteSelf(self):
		if (self._parent == None):
	  		raise Exception("Invalid Argument Error: programmer called deleteSelf on rootnode. See deleteSelf in goalObject.py ~Josh")
		parent = self._parent
		goalsList = parent.getSubgoalList()
		indexOfGoal = goalsList.index(self)
		parent.removeSubgoalAtIndex(indexOfGoal)
		parent.updateDatabase()



	# return this object as a JSON object (a python dictionary)
	# def listify(self, input):
	# 	newList = []
	# 	#string containing the actual content of a goal
	# 	goalContent = input.getGoalContent() 
	# 	#boolean: true if goal complete, else false
	# 	completionStatus = input.getCompletionStatus()
	# 	#list of goal objects
	# 	subgoals = input.getSubgoalList() 
	# 	# parent Node, returns goal object
	# 	parent = input.getParent() 
	# 	#username that the template belongs to
	# 	user = input.getUser() 

	# 	nestedList = []
	# 	for goal in subgoals: 
	# 		nestedList.append(goal.listify(goal))


	# 	newList.append(goalContent)
	# 	newList.append(completionStatus)
	# 	newList.append(nestedList)
	# 	newList.append(parent)
	# 	newList.append(user)
		
	# 	return newList


	def toJSON(self):
		return jsonpickle.encode(self)
 





   
  #  # private helper function for deleting subtrees recursively
  #  	def delRecursive(self):
  #  	 goalsList = self.getSubgoalList()
  #  	 if goalsList is not None: 
	 #   	 for subgoal in goalsList:
	 #   	 	subgoal.delRecursive()
	 # del self 

	# # Method for deleting a subtree and updating the database to reflect the deletion 
	# #This works as long as you do not call it on the root node(the template, in which case everything crashes)
	# def deleteSubtree(self):
	#   template = self.getTemplate()
	#   if (self == template):
	#   	raise Exception("Invalid Argument Error: programmer called deleteSubTree on rootnode. See deleteSubtree in goalObject.py ~Josh")
	#   parent = self._parent
	#   goalsList = parent.getSubgoalList()
	#   #what about the case in which there are multiple identical goal objects in a given list?? This doesn't work then!!!!
	#   indexOfGoal = goalsList.index(self)
	#   parent.removeSubgoalAtIndex(indexOfGoal)
	#   self.delRecursive()
	#   del self
	#   template.updateDatabase()
