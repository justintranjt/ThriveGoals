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
from sqlalchemy import update


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


#inserts a goal directly into our database in the goals table
def insertGoal(goalNum, user, temp, goalText, completionStatus, number): 
	try:
		ins = goal_table.insert().values(
		      goalNumber = goalNum,
		      username = user, 
		      templateId = temp, 
		      goal = goalText, 
		      isComplete = completionStatus,
		      priority = number)
		conn = engine.connect()
		conn.execute(ins)

	except Exception, e:
	        #conn.rollback()
	        return (True, str(e))
	return (False, "The goal has been successfully inserted." )



def updateUsername(goalId, newUsername): 
	try:
		stmt = update(goal_table).where(goal_table.c.goalNumber==goalId).values(username=newUsername)
		res = conn.execute(stmt)
	    
	except Exception, e:
	        #conn.rollback()
	        return (True, str(e))
	return (False, "The goal has been successfully inserted." )



def updateTemplateId(goalId, newTemplateId): 
	try:
		stmt = update(goal_table).where(goal_table.c.goalNumber==goalId).values(templateId=newTemplateId)
		res = conn.execute(stmt)
	    
	except Exception, e:
	        #conn.rollback()
	        return (True, str(e))
	return (False, "The goal has been successfully inserted." )



def updateGoalContent(goalId, newGoalContent): 
	try:
		stmt = update(goal_table).where(goal_table.c.goalNumber==goalId).values(goal=newGoalContent)
		res = conn.execute(stmt)
	    
	except Exception, e:
	        #conn.rollback()
	        return (True, str(e))
	return (False, "The goal has been successfully inserted." )



def updateIsComplete(goalId, newIsComplete): 
	try:
		stmt = update(goal_table).where(goal_table.c.goalNumber==goalId).values(isComplete=newIsComplete)
		res = conn.execute(stmt)
	    
	except Exception, e:
	        #conn.rollback()
	        return (True, str(e))
	return (False, "The goal has been successfully inserted." )




def updateGoalPriority(goalId, newPriority): 
	try:
		stmt = update(goal_table).where(goal_table.c.goalNumber==goalId).values(priority=newPriority)
		res = conn.execute(stmt)
	    
	except Exception, e:
	        #conn.rollback()
	        return (True, str(e))
	return (False, "The goal has been successfully inserted." )

    



        

	