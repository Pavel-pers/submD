import numpy
import matplotlib.pyplot as plt
import matplotlib


def tour(tlist: list):
    fig, ax = plt.subplots()

    tours = {}
    for ti in tlist:
        axLabel = str(ti.diff) + '(' + ("virtual" if ti.isVirtual else "real") + ')'

        if axLabel not in tours.keys():
            tours[axLabel] = []

        tours[axLabel].append(ti)
    dates = []
    for axLabel in tours.keys():
        xt = []
        yt = []

        for tour in tours[axLabel]:
            xt.append(numpy.datetime64(tour.time))
            dates.append(tour.time)
            yt.append(int(tour.score))
        ax.plot(xt, yt, label=axLabel)

    cdf = matplotlib.dates.ConciseDateFormatter(ax.xaxis.get_major_locator())
    ax.xaxis.set_major_formatter(cdf)
    ax.legend()
    fig.show()


def problems(plist):
    tagsCnt = {}

    sm = 0
    for i in plist:
        for tag in i.topic.split(','):
            if tag == '': continue
            if tag not in tagsCnt:
                tagsCnt[tag] = 0
            tagsCnt[tag] += 1
            sm += 1

    def makeText():
        def forEach(kf):
            return str(int(kf * sm / 100))
        return forEach

    plt.pie(tagsCnt.values(), labels=tagsCnt.keys(), autopct=makeText())
    plt.show()