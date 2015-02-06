# parses all tools data for Erin

import xml.etree.ElementTree as ET
import re
import sys
import constants
import resources
import helpers

def drawDeliveredIdeasGraph(dList, tList, teamName, file):
	file.write(helpers.getPanelHeader('Delivered/Targeted Ideas by ' + teamName))
	file.write(helpers.getChartHeader('bar', 400, 200))
	releaseDates = helpers.getReleaseDates(dList, tList)
	file.write(helpers.getToolsGraphTitleRow(releaseDates))
	table = dList + tList
	file.write(helpers.getGraphRow(table, teamName, releaseDates))
	file.write(helpers.getChartFooter())
	file.write(helpers.getPanelFooter())

def drawDeliveredIdeasGraphForTools(dList, tList, file):
	file.write(helpers.getPanelHeader('Delivered/Targeted Ideas by Tools'))
	file.write(helpers.getChartHeader('bar', 400, 200))
	releaseDates = helpers.getReleaseDates(dList, tList)
	file.write(helpers.getToolsGraphTitleRow(releaseDates))
	table = dList + tList
	file.write(helpers.getGraphRow(table, 'Tools', releaseDates))
	file.write(helpers.getChartFooter())
	file.write(helpers.getPanelFooter())

def drawDeliveredIdeasGraphByTeam(dList, tList, teamTables, file):
	file.write(helpers.getPanelHeader('Delivered/Targeted Ideas by Teams'))
	file.write(helpers.getChartHeader('bar', 700, 350))
	releaseDates = helpers.getReleaseDates(dList, tList)
	file.write(helpers.getToolsGraphTitleRow(releaseDates))	
	teamNames = helpers.getTeamNames()
	for i, table in enumerate(teamTables):
		file.write(helpers.getGraphRow(table, teamNames[i], releaseDates))
	file.write(helpers.getChartFooter())
	file.write(helpers.getPanelFooter())

def writeStatsTable(submittedList, candidateList, targetedList, deliveredList, file):
	file.write(helpers.getPanelHeader('Tools Stats'))
	file.write('||Category||Count||\n')
	file.write('|Num of Ideas in Submission|' + str(len(submittedList)) + '|\n')
	file.write('|Num of Top 10 w/o a JIRA|' + str(len(helpers.getTopIdeasWithNoJira(submittedList))) + '|\n')
	file.write('|Num of Ideas in Submission w/o a JIRA|' + str(len(helpers.getSubmissionIdeasWithNoJira(submittedList))) + '|\n')
	file.write('|Num of Ideas in Candidate|' + str(len(candidateList)) + '|\n')
	file.write('|Num of Ideas Targeted|' + str(len(targetedList)) + '|\n')
	file.write('|Num of Ideas Delivered|' + str(len(deliveredList)) + '|\n')
	file.write(helpers.getPanelFooter())

def categorizeIdeas(table, submittedList, candidateList, targetedList, deliveredList):
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

def buildToolsContent(table, teamTables, file):
	quick_sort(table)	
	submittedList = []
	candidateList = []
	targetedList = []
	deliveredList = []
	categorizeIdeas(table, submittedList, candidateList, targetedList, deliveredList)
	file.write(helpers.getSectionHeader())
	file.write(helpers.getColumnHeader('70%'))
	drawDeliveredIdeasGraphByTeam(deliveredList, targetedList, teamTables, file)
	file.write(helpers.getColumnFooter())
	file.write(helpers.getColumnHeader('30%'))
	drawDeliveredIdeasGraphForTools(deliveredList, targetedList, file)
	writeStatsTable(submittedList, candidateList, targetedList, deliveredList, file)
	file.write(helpers.getColumnFooter())
	file.write(helpers.getSectionFooter())
	return table

def buildIndividualTeamContent(table, teamName, file):
	quick_sort(table)	
	submittedList = []
	candidateList = []
	targetedList = []
	deliveredList = []
	categorizeIdeas(table, submittedList, candidateList, targetedList, deliveredList)
	writeStatsTable(submittedList, candidateList, targetedList, deliveredList, file)
	drawDeliveredIdeasGraph(deliveredList, targetedList, teamName, file)
	return table

def buildTable(fText):
	fText = helpers.cleanText(fText)
        root = ET.fromstring(fText)
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


def getTeamTableFromFile(team):
	fileName = "data/{}.xml".format(team)
	f = open(fileName, 'r')
	fText = f.read()
	table = buildTable(fText)
	return table

def createBottomSection(teamTables, file):
	file.write(helpers.getSectionHeader())
	file.write(helpers.getDeckHeader())
	teamNames = helpers.getTeamNames()
	for i, table in enumerate(teamTables):	
		file.write(helpers.getCardHeader(teamNames[i]))
		buildIndividualTeamContent(table, teamNames[i], file)
		file.write(helpers.getCardFooter())
	file.write(helpers.getDeckFooter())
	file.write(helpers.getSectionFooter())

def main():
	teamNames = helpers.getTeamNames()
	wikiFile = open('wiki/erinsDashboard', 'w')
	toolsTable = []
	teamTables = []
	for team in teamNames:
		table = getTeamTableFromFile(team)
		toolsTable.extend(table)
		teamTables.append(table)
	buildToolsContent(toolsTable, teamTables, wikiFile)
	createBottomSection(teamTables, wikiFile)

	wikiFile.close()

main()
