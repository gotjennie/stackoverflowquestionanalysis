import urllib2
import requests
import json
import pickle
import pprint as pp

url = "https://api.stackexchange.com/2.2/info?site=stackoverflow"
urlForQuestions = "https://api.stackexchange.com/2.2/questions?fromdate=1494288000&todate=1494892800&order=desc&sort=activity&tagged=python&site=stackoverflow&filter=withbody"

# r = requests.get(urlForQuestions).json()
# pickle.dump(r, open("stackoverflowJSON.txt", "wr"))

r = pickle.load(open("stackoverflowJSON.txt"))

questions = []

for key in r:
	pp.pprint(key)
	pp.pprint(r[key])

print "size"
print type(r.items)

# for key in r.items:
# 	print key
# print urllib2.urlopen(url).read()index, 