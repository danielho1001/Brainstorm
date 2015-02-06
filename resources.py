# resources.py
import sys
import re

def cleanLine(line):
	return line.replace('\n', '').replace('[', '%5B').replace(']', '%5D')

def getResources(team):
	resources = []
	file = open('resources.txt', 'r')
	index = 0
	for line in file:
		if index == 0 and line.startswith('.') and team in line:
			index += 1
		elif index >= 1 and index < 5:
			resources.append(cleanLine(line))
			index += 1
		elif index == 5:
			break		
	file.close()
	return resources

def getTeamMembers(team):
	members = []
	file = open('teamMembers.txt', 'r')
	for line in file:
		members.append(cleanLine(line))
	file.close()
	return members	
		


