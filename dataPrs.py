import db
import requests
from bs4 import BeautifulSoup
import numpy


def parseCF(submUrl="https://codeforces.com/submissions/pavel..pers"):
    data = BeautifulSoup(requests.get(submUrl).text, 'html.parser')
    data = data.find(class_="status-frame-datatable")
    data = data.find_all('tr', partymemberids = ";779169;")

    for subm in data:
        if subm.find('span', submissionverdict = "OK"):
            timeP = subm.find('span', "format-time").text
            timeP = numpy.datetime64(timeP[6:10] + '-' + timeP[3:5] + '-' + timeP[0:2])
            probId = ""
            prob = ""
            for aTag in subm.find_all('td'):
                if aTag.get('data-problemid'):
                    probId = aTag.find('a').get('href')
                    prob = aTag.find('a').text.strip()
                    break

            bs = BeautifulSoup(requests.get("https://codeforces.com" + probId).text, 'html.parser')
            tags = bs.find_all("span", "tag-box")
            tagsP = []
            dif = '-'
            for i in range(len(tags)):
                if tags[i].get('title') != "Difficulty":
                    tagsP += [tags[i].text.strip()]
                else:
                    dif = tags[i].text.strip()

            if dif[0] == '*':
                dif = dif[1:]

            db.insertProblem(db.Prob(prob, dif, tagsP, 100, probId))

def parseTours(p):
    with open(p, 'r') as f:
        fl = f.readlines()
        for i in range(0, len(fl), 5):
            name, time, diff, isV, s = fl[i].split()
            time = numpy.datetime64(time)
            isV = isV == 'vrt'
            s = int(s)

            problems = []

            for j in range(i + 1, i + 5):
                nameP, topicP, diffP, scrP = fl[j].split()
                problems += [db.Prob(nameP, diffP, topicP.split(','), scrP)]

            db.initNewTour(problems, name, time, diff, isV, s)