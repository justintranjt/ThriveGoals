#!/usr/bin/env python

#-----------------------------------------------------------------------
# testDB.py
# Author: Hamza Mahmood, Josh Gardner
#-----------------------------------------------------------------------

from updateDB3 import *
from goalObject import *


print("Creating goal object")
first = Goal('My first goal', False, [], None, 'hmahmood', False)
print(first)

#"Deleting the template associated with goal"
#deleteTemplate('hmahmood', 'My first goal')

print('-----------------------------')
print("Getting the template associated with goal")
# make sure that gettemplate returns nothing -- seems ok
print(getTemplate('My first goal', 'hmahmood'))

print('-----------------------------')
print("Updating the template name!")
first.setGoalContent("GOAL")
print(getTemplate('GOAL', 'hmahmood'))

print(getTemplate('My first goal', 'hmahmood'))
print(first)
