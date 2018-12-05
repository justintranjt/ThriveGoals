from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import Integer, String
import os
from sys import argv, stderr, exit
from sys import exit, argv, path
import psycopg2
from sqlalchemy import and_
from sqlalchemy import asc
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import exists
import json
import jsonpickle

db_uri = "postgres://wrlppbbvqcauzp:764db7ff9a698abcadb0ecf37e5d3f6405fb5acf6a1f1802f2febad6f6e52dfe@ec2-50-16-196-138.compute-1.amazonaws.com:5432/d7p8464rd276rt"
#conn = psycopg2.connect(db_uri, sslmode='require')
#os.environ['DATABASE_URL']
engine = create_engine(db_uri)
conn = engine.connect()
metadata = MetaData(engine, reflect=True)
#print(metadata.tables)

# Get Table
template_table = metadata.tables['templates']


# QUERY DATABSE
# NOTE: EDIT TO INCORPORATE CORRECT USERNAME!!!!
# updates blob of goals (templateBlob), necessary for changes in any one goal
def updateTemplate(username, templateName, newTemplateJSON):
	try:
	   

		select_st = select([template_table]).where((template_table.c.username == username) & (template_table.c.templateName == templateName))
		res = conn.execute(select_st)
		#.fetchone()
		# print(res)

		count = 0 
		for each in res:
			count +=1
		# if template doesn't already exist, insert it in new row 
		if count is 0:
			ins = template_table.insert().values(username = username, templateName = templateName, templateJSON = newTemplateJSON)
			conn.execute(ins)
			print("new row created")
		else: # if template exists, update template 

			update = template_table.update().where(
				(template_table.c.username == username) & (template_table.c.templateName == templateName)).values(templateJSON = newTemplateJSON)
			conn.execute(update)

	except Exception as e:
		# print "Oh fuck........."
		print (str(e))
		return (True, str(e))

	# print "End of update Call no exceptions thrown "
	return (False, "The template has been successfully updated.")

# updateTemplateBlob("soniajoseph", "mytemplate", "newTemplateBlob")



# function takes a string userName and returns a list of lists where each sublist is of length 3 
# and contains username, template name, and the blob object for each template for a given user
# The larger list is ordered alphabetically by template name 
def getTemplateList(userName):
	try:
		select_st = select([template_table]).where(
				template_table.c.username == userName).order_by(
				template_table.c.templateName.asc())
		res = conn.execute(select_st)
		listOfLists =[]
		for row in res: 
			username = row[0]
			tempName = row[1]
			jsonStr = fromJSONtoTemplate(row[2])
			oneList = [username, tempName, jsonStr]
			listOfLists.append(oneList)


	except Exception as e:
			#conn.rollback()
			return ("True", str(e), listOfLists)
	return (False, "If this message prints, the goal has been successfully inserted.", listOfLists)


####################################################################################################
#################Functions for JSON conversion and storage##########################################
####################################################################################################

# takes an already loaded json object
# def _buildTemplateRecursively(input):
#         goalContent = input['_goalContent']
#         #boolean: true if goal complete, else false
#         completionStatus = intput['_completionStatus'] 
#         # parent Node, returns goal object
#         parent = input['_parent'] 
#         #username that the template belongs to
#         user = input['_user'] 
#         newGoal = Goal(goalContent, completionStatus, [], parent, user)
#         for goal in input['_subgoals']: 
#             newGoal.addSubgoal(_processObjRecursively(goal))
#         return newGoal

# This function must take the json version of goal object
# any other input will cause an exception to be thrown. 
def fromJSONtoTemplate(json_input): 
		try:
			decoded = jsonpickle.decode(json_input)
		   # newTemplate = _buildTemplateRecursively(decoded)
			return decoded 
		 
		except (ValueError, KeyError, TypeError):
			print ("JSON format error")

#given a template name and username, this function returns the corresponding template
#this function considers having any more than one template meeting these criteria 
#to be a programmer error. Having only one template per user with the same name
#is an invariant that should be enforced across the application. 
def getTemplate(templateName, userName): 
	try:
		select_st = select([template_table]).where(
			 (template_table.c.templateName == templateName) & (template_table.c.username == userName))
		  
		res = conn.execute(select_st)
		goalsList =[]
		# if (len(res) is not 1):
		#     return (True, "Programmer Error: More than one template with same username and template name, or no matching template")
		# else: 
		for row in res:
			username = row[0]
			tempName = row[1]
			jsonStr = row[2]
			template = fromJSONtoTemplate(jsonStr)

	except Exception as e:
			#conn.rollback()
			return ("True", str(e), None)
	return (False, "If this message prints, the template has been successfully retireved.", template)

def deleteTemplate(username, templateName):
	try:
		del_st = template_table.delete().where((template_table.c.username == username) & (template_table.c.templateName == templateName))
		res = conn.execute(del_st)


	except Exception as e:
		# print(Oh fuck.........
		#print str(e)
		return (True, str(e))

	# print "End of update Call no exceptions thrown "
	return (False, "The template has been successfully updated.")

def updateTemplateName(username, newName, templateJSON):
	print("Updating template name")
	print("new name is: "+ newName)
	try:
		update = template_table.update().where(
			(template_table.c.username == username) & (template_table.c.templateJSON == templateJSON)).values(templateName = newName)
		conn.execute(update)

	except Exception as e:
		print("Database Exception updateTemplateName")
		print (str(e))
		return (True, str(e))

	# print "End of update Call no exceptions thrown "
	return (False, "The template has been successfully updated.")
