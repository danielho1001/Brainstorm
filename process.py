# parses xml files and processes community information and renders in wiki for confluence

import xml.etree.ElementTree as ET
import re
import sys
import constants
import resources
import helpers

submittedList = []
candidateList = []
targetedList = []
deliveredList = []
team = ''
currFileName = ''
oldFileName = ''
wikiFileName = ''


def writeSelfCreatedTable(currTable, file):
	selfTable = helpers.getSelfCreatedIdeas(currTable, resources.getTeamMembers(team))
	file.write(helpers.getPanelHeader('Self Created Ideas'))
	file.write('||Title||Author||JIRA||Vote||Comment||\n')
	for idea in selfTable:
		file.write(helpers.getIdeaRowWiki(idea))
	file.write(helpers.getPanelFooter())

def findRecentTopActivity(currTable):	
	oldFile = open(oldFileName, 'r')
	oldFileText = oldFile.read()
	oldTable = buildTable(oldFileText)
	diffTable = helpers.getActivity(oldTable, currTable)
	quick_sort(diffTable)	
	return diffTable[:10]

def writeActivityTable(currTable,file):
	diffTable = findRecentTopActivity(currTable)
	file.write(helpers.getPanelHeader('Top Recent Activities'))	
	file.write('||Title||Status||JIRA||Vote Change||Comment Change||\n')
	for idea in diffTable:
		file.write(helpers.getTopActivityRowWiki(idea))
	file.write(helpers.getPanelFooter())

def createBottomSection(currTable, file):
	file.write(helpers.getSectionHeader())
	file.write(helpers.getColumnHeader(50))
	writeTopSubmissionTable(file)
	file.write(helpers.getColumnFooter())
	file.write(helpers.getColumnHeader(50))
	writeSelfCreatedTable(currTable, file)
	file.write(helpers.getColumnFooter())	
	file.write(helpers.getSectionFooter())		

def writeTopSubmissionTable(file):
	file.write(helpers.getPanelHeader('Top Ideas in Submission'))	
	file.write('||Title||JIRA||Vote||Comment||\n')
	for idea in submittedList[:10]:	
		file.write(helpers.getIdeaInSubmissionRowWiki(idea))
	file.write(helpers.getPanelFooter())

def writeStatsTable(table, file):
	file.write(helpers.getPanelHeader('Stats Table'))
	file.write('||Category||Count||\n')
	file.write('|Num of Top 10 w/o a JIRA|' + str(len(helpers.getTopIdeasWithNoJira(submittedList))) + '|\n')
	file.write('|Num of Ideas in Submission|' + str(len(submittedList)) + '|\n')
	file.write('|Num of Ideas in Submission w/o a JIRA|' + str(len(helpers.getSubmissionIdeasWithNoJira(submittedList))) + '|\n')
	file.write('|Num of Ideas in Candidate|' + str(len(candidateList)) + '|\n')
	file.write('|Num of Ideas Targeted|' + str(len(targetedList)) + '|\n')
	file.write('|Num of Ideas Delivered|' + str(len(deliveredList)) + '|\n')
	file.write(helpers.getPanelFooter())

def writeResourcesTable(file):
	links = resources.getResources(team)	
	file.write(helpers.getPanelHeader('Resources'))
	file.write('[Brainstorm Filtered List|' + links[0] + ']\n')
	file.write('[JIRA Dashboard|' + links[1] + ']\n')
	file.write('[Brainstorm Excel Export|' + links[2] + ']\n')
	file.write(helpers.getPanelFooter())

def createTopSection(table, file):
	file.write(helpers.getSectionHeader())
	file.write(helpers.getColumnHeader(40))	
	writeStatsTable(table, file)
	writeResourcesTable(file)
	file.write(helpers.getColumnFooter())
	file.write(helpers.getColumnHeader(60))
	writeActivityTable(table, file)
	file.write(helpers.getColumnFooter())
	file.write(helpers.getSectionFooter())

def categorizeIdeas(table):
	for idea in table:
		if 'Submitted' in idea[constants.IdeaStatus]:
			submittedList.append(idea)
		elif 'Candidate' in idea[constants.IdeaStatus]:
			candidateList.append(idea)
		elif 'Targeted' in idea[constants.IdeaStatus]:
			targetedList.append(idea)
		elif 'Delivered' in idea[constants.IdeaStatus]:
			deliveredList.append(idea)	

def quick_sort(items):
	if len(items) > 1:
		pivot_index = len(items) / 2
		smaller_items = []
		larger_items = []

		for i, val in enumerate(items):
		    if i != pivot_index:
			if helpers.isGreater(items[i], items[pivot_index]):
			    smaller_items.append(val)
			else:
			    larger_items.append(val)

		quick_sort(smaller_items)
		quick_sort(larger_items)
		items[:] = smaller_items + [items[pivot_index]] + larger_items
		return items

def buildTable(fileText):
	fileText = helpers.cleanText(fileText)
	root = ET.fromstring(fileText)
	table = [0]*1000
	row = 0
	for elem in root.iter():
		if 'Row' in elem.tag:
			table[row] = []
			row += 1
		if 'Data' in elem.tag:
			if row > 1:
				table[row-2].append(elem.text)		
	table = helpers.cleanUp(table[:row-1])
	return table

def main(t, cf, of, wf):
	file = open(currFileName, 'r')
	fileText = file.read()
	file.close()
	table = buildTable(fileText)
	
	quick_sort(table)
	categorizeIdeas(table)

	wikiFile = open(wikiFileName, 'w')
	createTopSection(table, wikiFile)
	createBottomSection(table, wikiFile)
	wikiFile.close()	

team = sys.argv[1]
currFileName = sys.argv[2]
oldFileName = sys.argv[3]
wikiFileName = sys.argv[4]
main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
