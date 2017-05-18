import urllib2
import requests
import json
import pickle
import pprint as pp
from bs4 import BeautifulSoup
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
	info["totalLinesOfCode"] = sum(linesPreCode)
	info["numberOfCodeSnippets"] = len(linesPreCode)
	if(len(linesPreCode) > 0):
		info["averageLengthOfCodeSnippet"] = float(sum(linesPreCode))/len(linesPreCode)
	else:
		info["averageLengthOfCodeSnippet"] = 0

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

	body = BeautifulSoup(body, "lxml").text
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
	info = getCodeInfo(body)
	return info

def getAcceptedAnswerScore(acceptedAnswers, current_accepted_answer_id):
	for d in acceptedAnswers['items']:
		if d['answer_id'] == current_accepted_answer_id:
			return d['score']
	return None

url = "https://api.stackexchange.com"
customFiltering = "/2.2/questions?fromdate=1493596800&todate=1495065600&order=desc&sort=votes&tagged=python&site=stackoverflow"
urlForQuestions = url+ customFiltering+ "&filter=withbody"

# r = requests.get(urlForQuestions).json()
# pickle.dump(r, open("sortVotes.txt", "wr"))

r = pickle.load(open("sortVotes.txt"))
r2 = pickle.load(open("acceptedAnswers.txt"))

questionsWithAccepted = []
questionsWithOut = []
acceptedAnswerIds = "" # re: Getting the answers -- this string will be used for the API call for accepted answers.

for questionObject in r['items']:
	#print questionObject.keys()
	questionInfo = {};

	#print questionObject['score']
	body = questionObject['body']
	if "accepted_answer_id" in questionObject:
		info = getStats(body)
		info["link"] = questionObject["link"]
		info["acceptedAnswerId"] = questionObject["accepted_answer_id"]
		acceptedAnswerIds += str(questionObject["accepted_answer_id"]) + ";" # answers-by-ids documentation page says "{ids} can contain up to 100 semicolon delimited ids"

		info["acceptedAnswerScore"] = getAcceptedAnswerScore(r2, questionObject["accepted_answer_id"])
		questionsWithAccepted.append(info)
	else:
		info = getStats(body)
		questionsWithOut.append(info)

pp.pprint(questionsWithAccepted)
# pickle.dump(questionsWithAccepted, open("questionsWithAccepted.txt", "wr"))

### Getting the answers -- https://api.stackexchange.com/docs/answers-by-ids
# print acceptedAnswerIds[:-1] # indexing [:-1] because the API call doesn't want the {ids} string to end with a semicolon
urlForAcceptedAnswerIds = url + '/2.2/answers/' + acceptedAnswerIds[:-1]  + '?order=desc&sort=activity&site=stackoverflow&filter=withbody'
# print urlForAcceptedAnswerIds
# r2 = requests.get(urlForAcceptedAnswerIds).json()
# pickle.dump(r2, open("acceptedAnswers.txt", "wr"))
r2 = pickle.load(open("acceptedAnswers.txt"))
# pp.pprint(r2['items'])
# pp.pprint(r2['items'][0]["answer_id"])
# print getAcceptedAnswerScore(r2, 44012152)
# print getAcceptedAnswerScore(r2, 43723651)
# print getAcceptedAnswerScore(r2, 43988809)
