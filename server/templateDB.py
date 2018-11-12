#!/usr/bin/env python

#-----------------------------------------------------------------------
# dbModule.py
# Author: Josh Gardner
#-----------------------------------------------------------------------
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
from Goal import * 
from goalDB import*


db_uri = "postgres://wrlppbbvqcauzp:764db7ff9a698abcadb0ecf37e5d3f6405fb5acf6a1f1802f2febad6f6e52dfe@ec2-50-16-196-138.compute-1.amazonaws.com:5432/d7p8464rd276rt"
#conn = psycopg2.connect(db_uri, sslmode='require')
#os.environ['DATABASE_URL']
engine = create_engine(db_uri)
conn = engine.connect()
metadata = MetaData(engine, reflect=True)
#print(metadata.tables)

# Get Table
userPassword_table = metadata.tables['users']
goal_table = metadata.tables['goals']


#returns a list of goals ordered by priority for a given template 
def getTemplateGoals(templateIdNum): 
	try:
		select_st = select([goal_table]).where(
   				goal_table.c.templateId == templateIdNum ).order_by(
   				goal_table.c.priority.asc())
		res = conn.execute(select_st)
		goalsList =[]
		for row in res:
			goalId =  row[0]
			#print str(goalId)
			userName = row[1]
			templateNum = row[2]
			goalContent = row[3]
			isComplete = row[4]
			goalPriority = row[5]
			curGoal = Goal(goalId, userName, templateNum, goalContent, isComplete, goalPriority, False)
			goalsList.append(curGoal)

	except Exception, e:
            #conn.rollback()
            return ("True", str(e), goalsList)
	return (False, "If this message prints, the goal has been successfully inserted.", goalsList )
    



# hasError, message = insertGoal(0, "Eisgruber", 0, "Mediate conflicts between orange and black squirrels", False, 3 )
# if hasError:
# 	print message 
# hasError, message = insertGoal(1, "Eisgruber", 0, "Increase the number of squirrel friendly locations on campus", False, 2 )
# if hasError:
# 	print message 
# hasError, message = insertGoal(2, "Eisgruber", 0, "Decrease grad student hostility towards squirrels", False, 1 )
# if hasError:
# 	print message 


goal1 = Goal(0, "Eisgruber", 0, "Mediate conflicts between orange and black squirrels", False, 3, True)
goal2 = Goal(1, "Eisgruber", 0, "Increase the number of squirrel friendly locations on campus", False, 2, True)
goal3 = Goal(2, "Eisgruber", 0, "Decrease grad student hostility towards squirrels", False, 1, True)
hasError, message, goalsList = getTemplateGoals(0)
if hasError:
	print message 
print "Template Id 1       User: Eisgruber       Higher Order Goal: Improve Human Squirrel Realtions"
if goalsList is not None:
	for goal in goalsList:
		print str(goal)

print " "
print " "
print " "
#print "Template Id: 2        User: Eisgruber     Higher Order Goal: Increase Number of students going into consulting  "


print " Testing: setUserName"
print "Template Id 1       User: Reburgsie            Higher Order Goal: Improve Human Squirrel Realtions"

# goal4 = Goal(4, "Eisgruber", 1, "Discourage students from learning useful technical skills", False, 3, True)
# goal5 = Goal(5, "Eisgruber", 1, "Increase reliance on social networks and eating clubs", False, 2, True)
# goal6 = Goal(6, "Eisgruber", 1, "Break will through grade deflation and systematic policy initiatives", False, 1, True)

goal1.setUsername("Reburgsie")
goal2.setUsername("Reburgsie")
goal3.setUsername("Reburgsie")

hasError, message, goalsList = getTemplateGoals(0)
if hasError:
	print message 
if goalsList is not None:
	for goal in goalsList:
		print str(goal)


print " "
print " "
print " "
print " Testing: setTemplateId"
goal1.setTemplateId(5)
goal2.setTemplateId(5)
goal3.setTemplateId(5)
hasError, message, goalsList = getTemplateGoals(5)
if hasError:
	print message 
if goalsList is not None:
	for goal in goalsList:
		print str(goal)



print " "
print " "
print " "
print " Testing: setGoalContent"
goal1.setGoalContent("Defeat Grade Deflation")
goal2.setGoalContent("Become Mork Zoinkerboinker")
goal3.setGoalContent("Steal app from the Wonkerbonk twins")
hasError, message, goalsList = getTemplateGoals(5)
if hasError:
	print message 
if goalsList is not None:
	for goal in goalsList:
		print str(goal)





print " "
print " "
print " "
print " Testing: setIsComplete"
goal1.setIsComplete(True)
goal2.setIsComplete(True)
goal3.setIsComplete(True)
hasError, message, goalsList = getTemplateGoals(5)
if hasError:
	print message 
if goalsList is not None:
	for goal in goalsList:
		print str(goal)




print " "
print " "
print " "
print " Testing: setGoalPriority"
goal1.setGoalPriority(1)
goal2.setGoalPriority(2)
goal3.setGoalPriority(3)
hasError, message, goalsList = getTemplateGoals(5)
if hasError:
	print message 
if goalsList is not None:
	for goal in goalsList:
		print str(goal)
