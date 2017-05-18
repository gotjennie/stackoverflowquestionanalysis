import urllib2
import requests
import json
import pickle
import pprint as pp
from BeautifulSoup import BeautifulSoup
import re

def getCodeInfo(body):
	info = {}

	# info["body"] = body

	preCodeStartTag = "<pre><code>"
	preCodeEndTag = "<\/code><\/pre>"
	preCode = findTextBetweenTags(body, preCodeStartTag, preCodeEndTag)
	numPreCode = len(preCode)
	linesPreCode = map(lambda x: x.count("\n"), preCode)
	info["linesInEachPreCodeSnippet"] = linesPreCode

	# codeStartTag = "([^>]<code>)|(^<code>)"
	# codeEndTag = "(<\/code>[^<])|(<\/code>$)"
	# code = findTextBetweenTags(body, codeStartTag, codeEndTag)
	# linesCode = map(lambda x: len(x), code)
	# info["lengthEachCodeSnippet"] = linesPreCode

	imgStartTag = "<img"
	imgEndTag = ">"
	imgs = findTextBetweenTags(body, imgStartTag, imgEndTag)
	info["numberImages"] = len(imgs)

	linkStartTag = "<a"
	linkEndTag = "<\/a>"
	links = findTextBetweenTags(body, linkStartTag, linkEndTag)
	info["numberLinks"] = len(links)

	english = getEnglish(body)

	# info["bodyText"] = english
	info["englishNumChars"] = len(english)
	info["englishNumWords"] = english.count(' ')

	info["numQuestionMarks"] = english.count('?')

	return info

def getEnglish(body):
	# english = ""

	codeRegex = "(<code>[^<]*<\/code>)"
	linkRegex = "(<a.*<\/a>)"

	body = re.sub(codeRegex, '', body)
	body = re.sub(linkRegex, '', body)

	body = BeautifulSoup(body).text
	return body




def findTextBetweenTags(body, startTagString, endTagString):
	startTag =  [t.start() for t in re.finditer(startTagString, body)]
	endTag =  [t.start() for t in re.finditer(endTagString, body)]
	
	inBetween = [];

	for i in range(len(startTag)):
		code = body[startTag[i]+len(startTagString):endTag[i]]

		inBetween.append(code)

	return inBetween


def getStats(body):
	# print body
	info = getCodeInfo(body)
	return info

url = "https://api.stackexchange.com"
customFiltering = "/2.2/questions?fromdate=1493596800&todate=1495065600&order=desc&sort=votes&tagged=python&site=stackoverflow"
urlForQuestions = url+ customFiltering+ "&filter=withbody"

# r = requests.get(urlForQuestions).json()
# pickle.dump(r, open("sortVotes.txt", "wr"))

r = pickle.load(open("sortVotes.txt"))

pp.pprint(r)

for questionObject in r['items']:
	#print questionObject.keys()
	questionInfo = {};

	#print questionObject['score']
	body = questionObject['body']
	info = getStats(body)
	if "accepted_answer_id" in questionObject:
		info["answerId"] = questionObject["accepted_answer_id"]
		#answerInfo = getAnswerStats()	
		#info += answerInfo

	else:
		info["answerId"] = None


	pp.pprint(info)






# for key in r.items:
# 	print key
# print urllib2.urlopen(url).read()index, 