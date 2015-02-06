# helper methods to declutter the main script

import constants
import copy
import urllib2

def cleanLine(line):
	return line.replace('\n', '')

def checkForResponse(idea):
	response = urllib2.urlopen(idea[constants.IdeaUrl])
	html = response.read()
	print html

def getGraphRow(table, teamName, releaseDates):
	row = '|' + teamName + '|'
	ideas = []
	releaseCounts = [0]*len(releaseDates)
	for idea in table:
		if 'Delivered' in idea[constants.IdeaStatus]:
			ideas.append(idea)
		elif 'Targeted' in idea[constants.IdeaStatus]:
			ideas.append(idea)
	for idea in ideas:
		release = idea[constants.Update]
		if release:
			release = int(release[8:])
		else:
			release = 0
		releaseCounts[releaseDates.index(release)] += 1
	for count in releaseCounts:
		row += str(count)
		row += '|'
	row += '\n'
	return row


def getTeamNames():
	f = open('teamNames.txt', 'r')
	teamNames = []	
	for line in f:
		line = cleanLine(line)
		if line:
			teamNames.append(line)
	return teamNames

def getReleaseDates(dList, tList):
	dates = []
	for idea in dList:
		release = idea[constants.Update]
		if release:
			release = int(release[8:])
		else:
			release = 0
		if release not in dates:
			dates.append(release)
	for idea in tList:
		release = idea[constants.Update]
		if release:
			release = int(release[8:])
		else:
			release = 0
		if release not in dates:
			dates.append(release)
	return sorted(dates)

def getToolsGraphTitleRow(releaseDates):
	titleRow = '|| ||'
	for release in releaseDates:
		titleRow += str(release)
		titleRow += '||'
	titleRow += '\n'
	return titleRow

def cleanText(fileText):
        fileText = fileText.replace('&amp;', '').replace('&#39;', "'").replace('&#13;', '').replace('&quot;', '"').replace('&bulk;', '').replace('&ldquo;', '').replace('&amp;', '')
        fileText = fileText.replace('quot;', '').replace('bulk;', '')
	fileText = fileText.replace('#039;', "'")
        fileText = fileText.replace('&', '')
        return fileText

def cleanUp(table):
	for idea in table:
		if not idea[constants.Comments]:
			idea[constants.Comments] = '0'
		if not idea[constants.NetVotes]:
			idea[constants.NetVotes] = '0'
	return table

def isGreater(item1, item2):
	if int(item1[constants.NetVotes]) > int(item2[constants.NetVotes]):	
		return True
	else:
		return False

def getTopActivityRowWiki(idea):
	linkToIdea = '['+idea[constants.Idea]+'|'+idea[constants.IdeaUrl]+']'
        linkToJira = ' '
	if idea[constants.JiraId] and idea[constants.JiraUrl]:
		linkToJira = '['+idea[constants.JiraId]+'|'+idea[constants.JiraUrl]+']' 
	rowWiki = '|' + linkToIdea + '|' + idea[constants.IdeaStatus] + '|' + linkToJira + '| +' + idea[constants.NetVotes] + '| +' + idea[constants.Comments] + '|\n'
	return rowWiki

def getIdeaInSubmissionRowWiki(idea):
	linkToIdea = '['+idea[constants.Idea]+'|'+idea[constants.IdeaUrl]+']'
	linkToJira = ' '
	if idea[constants.JiraId] and idea[constants.JiraUrl]:
		linkToJira = '['+idea[constants.JiraId]+'|'+idea[constants.JiraUrl]+']'
	rowWiki = '|' + linkToIdea + '|' + linkToJira + '|' + idea[constants.NetVotes] + '|' + idea[constants.Comments] + '|\n'
	return rowWiki

def getIdeaRowWiki(idea):	
	linkToIdea = '['+idea[constants.Idea]+'|'+idea[constants.IdeaUrl]+']'
        linkToJira = ' '
	if idea[constants.JiraId] and idea[constants.JiraUrl]:
		linkToJira = '['+idea[constants.JiraId]+'|'+idea[constants.JiraUrl]+']' 
	rowWiki = '|' + linkToIdea + '|' + idea[constants.Author] + '|' + linkToJira + '|' + idea[constants.NetVotes] + '|' + idea[constants.Comments] + '|\n'
	return rowWiki

def getSelfCreatedIdeas(table, teamMembers):
	selfCreatedIdeas = []
	for idea in table:
		if idea[constants.Author] in teamMembers:
			if 'Delivered' not in idea[constants.IdeaStatus] and 'Closed' not in idea[constants.IdeaStatus]:
				selfCreatedIdeas.append(idea)
	return selfCreatedIdeas 

def getActivity(oldTable, newTable):
	actTable = []
	for i, newIdea in enumerate(newTable):
		actIdea = []
		for oldIdea in oldTable:
			if oldIdea[constants.IdeaUrl] == newIdea[constants.IdeaUrl]:
				actIdea = copy.deepcopy(newIdea)
				voteDiff = int(newIdea[constants.NetVotes]) - int(oldIdea[constants.NetVotes])
				commentDiff = int(newIdea[constants.Comments]) - int(oldIdea[constants.Comments])
				if voteDiff > 0 or commentDiff > 0:
					actIdea[constants.NetVotes] = str(voteDiff)
					actIdea[constants.Comments] = str(commentDiff)
					actTable.append(actIdea)
				break
		if not actIdea:
			if int(newIdea[constants.NetVotes]) > 0 or int(newIdea[constants.Comments]) > 0:
				actTable.append(newIdea)	
				
	return actTable

def getTopIdeasWithNoJira(table):
	noJiraList = []
	for idea in table[:10]:
		if not idea[constants.JiraId]:
			noJiraList.append(idea)
	return noJiraList	

def getSubmissionIdeasWithNoJira(submittedList):
	submissionList = []	
	for idea in submittedList:
		if not idea[constants.JiraId]:
			submissionList.append(idea)
	return submissionList

def getDeckHeader():
	return '{deck:id=deck|tablocation=top}\n'

def getDeckFooter():
	return '{deck}\n'

def getCardHeader(title):
	return '{card:label=' + title + '}\n'

def getCardFooter():
	return '{card}\n'

def getChartHeader(chartType, width, height):
	return '{chart:type='+chartType+'|dataDisplay=true|legend=true|width='+str(width)+'|height='+str(height)+'}\n'

def getChartFooter():
	return '{chart}\n'

def getSectionHeader():
	return '{section:border=false}\n'

def getSectionFooter():
	return '{section}\n'

def getColumnHeader(width):
	return '{column:width=' + str(width) + '}\n'

def getColumnFooter():
	return '{column}\n'
	
def getPanelHeader(title):
	return '{panel:title=' + title + '|borderStyle=solid|borderColor=black|titleBGColor=#0067AB|titleColor=white}\n'

def getPanelFooter():
	return '{panel}\n'

def printVotes(table):
	for idea in table:
		print idea[constants.NetVotes]
