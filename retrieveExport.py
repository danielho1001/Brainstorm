import urllib2
import resources
import sys

team = sys.argv[1]
links = resources.getResources(team)
fileUrl = links[2]

response = urllib2.urlopen(fileUrl)
html = response.read()
print html
