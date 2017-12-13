import urllib2
import json

url = 'http://127.0.0.1:9000/api/issues/search?p=1&ps=50&s=FILE_LINE&asc=true&additionalFields=_all&facets=severities%2Cresolutions%2Cresolutions%2Cassigned_to_me&resolved=false'

def printTestIssue():
	u = urllib2.urlopen(url)
	data = u.read()

	j = json.loads(data)
	each = j['issues']

	issue=[]
	index = 0
	print "[Index]\t[Severity]\t[Project]\t[Type]\t\t[Message]\n"
	for msg in each:
   		tag = msg['tags'][0]
		if msg['project'] == 'testForFeedback':
   			print "[%d]\t[%s] \t[%s]\t\t[%s]\t<%s>" % (index, msg['severity'], msg['project'], tag, msg['message'])
	                issue.append((msg['severity'],tag,msg['message']))
   		index = index + 1
	return issue
#printTestIssue();
