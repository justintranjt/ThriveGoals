#!/usr/bin/env python

#-----------------------------------------------------------------------
# Goal.py
# Author: Josh Gardner
#-----------------------------------------------------------------------
from goalDB import * 

class Goal (object):
    
    def __init__(self, goalId, userName, templateId, goalContent, isComplete, goalPriority, isNew):
        if isNew:
            hasError, errorMessage = insertGoal(goalId, userName, templateId, goalContent, isComplete, goalPriority)
            if hasError:
                raise Exception('Error in Goal Constructor in Goal.py: {}'.format(errorMessage))
        self._goalId = goalId
        self._username = userName
        self._templateId = templateId
        self._goalContent = goalContent
        self._isComplete = isComplete
        self._goalPriority = goalPriority

   


        
    def __str__(self):
        retStr = 'Goal Number: '+str(self._goalId)+' | User Name:'+str(self._username)+' | Template Id: '+str(self._templateId)
        retStr += '| Goal Priority: '+str(self._goalPriority)+' | Is Complete: '+str(self._isComplete)+'| Priority Number: '+str(self._goalPriority)+'\n'
        retStr += 'Goal Content: '+str(self._goalContent)
        return retStr 
        
   
        
    def getGoalId(self):
        return self._goalId 



    def setUsername(self, newUsername):
        self._username = newUsername
        hasError, errorMessage = updateUsername(self._goalId, newUsername)
        if hasError:
            raise Exception('Error in setUsername in Goal.py: {}'.format(errorMessage))

    def getUsername(self):
        return self._username


    def setTemplateId(self, newTemplateId):
        self._templateId = newTemplateId
        hasError, errorMessage = updateTemplateId(self._goalId, newTemplateId)
        if hasError:
            raise Exception('Error in setTemplateId in Goal.py: {}'.format(errorMessage))

    def getTemplateId(self):
        return self._templateId



    def setGoalContent(self, newGoalContent):
        self._goalContent = newGoalContent
        hasError, errorMessage = updateGoalContent(self._goalId, newGoalContent)
        if hasError:
            raise Exception('Error in setGoalContent in Goal.py: {}'.format(errorMessage))

    def getGoalContent(self):
        return self._goalContent



    def setIsComplete(self, newIsComplete):
        self._isComplete = newIsComplete
        hasError, errorMessage = updateIsComplete(self._goalId, newIsComplete)
        if hasError:
            raise Exception('Error in setIsComplete in Goal.py: {}'.format(errorMessage))

    def getIsComplete(self):
        return self._isComplete


    def setGoalPriority(self, newGoalPriority):
        self._goalPriority = newGoalPriority
        hasError, errorMessage = updateGoalPriority(self._goalId, newGoalPriority)
        if hasError:
            raise Exception('Error in setGoalPriority in Goal.py: {}'.format(errorMessage))

    def getGoalPriority(self):
        return self._goalPriority
    

    
        
        
        
        
   # 