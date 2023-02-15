import sqlite3
import uuid

import numpy

class Prob:
    idf: str
    name: str
    topic: list
    diff: int
    score: int

    def __init__(self, name, diff, topic: list, scr, idf = False):
        if not idf:
            idf = str(uuid.uuid4())
        self.idf = idf
        self.name = name
        self.topic = topic
        self.diff = diff
        self.score = scr


class Tour:
    idf: str
    name: str
    problems: list
    time: numpy.datetime64
    diff: int
    isVirtual: bool
    score: int

    def __init__(self, name, prob: list, time, diff, isVirtual, scr, idf = False):
        if not idf:
            idf = str(uuid.uuid4())
        self.idf = idf
        self.name = name
        self.problems = prob
        self.time = time
        self.diff = diff
        self.isVirtual = isVirtual
        self.score = scr



db = sqlite3.connect("trackData.db")
cur = db.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS problems(idf text, name text, topic text, diff text, scr int)")
cur.execute("CREATE TABLE IF NOT EXISTS tours(idf, name, problems, time, complexity, isVirtual, scr)")
db.commit()


def insertProblem(p: Prob):
    if not cur.execute("SELECT idf FROM problems WHERE idf = ?", (p.idf, )).fetchone():
        topic = ""
        for i in p.topic:
            topic += i
            topic += ','
        cur.execute("INSERT INTO problems VALUES(?,?,?,?,?)",
                    (p.idf, p.name, topic, p.diff, int(p.score)))
        db.commit()


def insertTour(tq: Tour):
    probs = ""
    for pi in tq.problems:
        probs += pi.idf
        probs += ','
    cur.execute("INSERT INTO tours VALUES(?,?,?,?,?,?,?)",
                (tq.idf, tq.name, probs, numpy.datetime_as_string(tq.time, unit='D'), tq.diff, tq.isVirtual, tq.score))
    db.commit()


def initNewTour(probs:list, name, time, diff, isV, score):
    problemId = []
    for i in probs:
        insertProblem(i)
        problemId += [i]

    insertTour(Tour(name, problemId, time, diff, isV, score))


def getProblems():
    data = cur.execute("SELECT * FROM problems").fetchall()
    for i in range(len(data)):
        data[i] = Prob(data[i][0], data[i][1], data[i][2], data[i][3], data[i][4])

    return data

def problemById(idp):
    data = cur.execute("SELECT * FROM problems WHERE idf = ?", (idp,)).fetchone()
    return Prob(data[1], data[2], data[3], data[4], idp)

def tours():
    data = cur.execute("SELECT * FROM tours").fetchall()

    for i in range(len(data)):
        probs = []
        for j in data[i][2].split(',')[-1]:
            probs += [problemById(j)]
        data[i] = Tour(data[i][1], data[i][2], numpy.datetime64(data[i][3]), data[i][4], data[i][5], data[i][6], data[i][0])
    return data
