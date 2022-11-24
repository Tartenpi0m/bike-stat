from tinydb import TinyDB, where
import datetime as dt
import numpy as np
from pylib.default_variable import *
import matplotlib.pyplot as plt
import matplotlib

def str_to_time(t : str):
    t = dt.time.fromisoformat(t)
    return dt.timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)

def process_data(data):
    data2 = {}
    data2["type"] = "tour"
    print(data["date"])

    data2["date"] = data["date"]

    data2["nombre tour"] = int(data['nombre tours'])
    data2["temps allez"] = str_to_time(data['go time']).seconds
    data2["temps retour"] = str_to_time(data['return time']).seconds
    data2["distance allez"] = float(data["distance allez"])
    data2["distance retour"] = float(data["distance retour"])
    
    data2["temps tour"] = [str_to_time(data["tour " + str(i)]).seconds    for i in range(1, data2["nombre tour"] + 1)]
    data2["distance tour"] = float(data['distance tour'])
    data2["vitesse tour"] = (data2["distance tour"] / np.array(data2['temps tour'])).tolist()
    
    data2["temps sortie"] = float(np.sum(data2['temps tour']) + data2["temps allez"] + data2["temps retour"])
    data2["distance sortie"] = float(data2["distance allez"] + data2["distance retour"] + data2["nombre tour"]*data2["distance tour"])
    data2["vitesse sortie"] = float(data2["distance sortie"] /  data2["temps sortie"])

    data2["vitesse moyenne"] = float(np.mean(data2["vitesse tour"]))

    return data2

def process_simple_data(data):
    data2 = {}
    data2["type"] = "simple"
    data2["date"] =  data["date"]
    data2["temps sortie"] = str_to_time(data["time"]).seconds
    data2["distance sortie"] = float(data["distance"])
    data2["vitesse moyenne"] = (float(data2["distance sortie"]) / float(data2["temps sortie"]))
    return data2

def update_database(data):
    db = TinyDB(DATABASE)
    db.insert(data)

def query_jour(date):
    db = TinyDB(DATABASE)

    if date == 'last':
        try:
            id = db.all()[-1].doc_id
            return db.get(doc_id=id)
        except:
            return False
    else:
        db.search(where('date') == date)[-1]

def graph_jour(d):
    matplotlib.style.use('ggplot')
    if d["type"] == 'tour':
        x = np.arange(1,d['nombre tour'] + 1)
        xticks_labels =  [str(i[0]) + "\n" + str(dt.timedelta(seconds=i[1]))[-4:].replace(':', 'm') + "\n" + str(i[0]*d['distance tour']/1000) + "km"
        for i in list(zip(x, d['temps tour']))]

        plt.figure(figsize=(20,4));
        plt.plot(x, np.array(d['vitesse tour'])*3.6, linestyle='dashdot', marker='o', markersize="11")
        plt.xticks(ticks=x, labels=xticks_labels);
        plt.ylabel("km/h")
        plt.title(f"Sortie du {d['date']} : {d['vitesse moyenne']*3.6:.1f}km/h pendant {dt.timedelta(seconds=float(np.sum(d['temps tour'])))}", color='grey')
        plt.savefig(CACHE + "jour.png", bbox_inches="tight")
    


def query_period():
    db = TinyDB(DATABASE)
    d = db.all()
    return d

def graph_period(d):
    x = np.arange(1, len(d)+1)
    #temps = []
    vitesse = []
    distance = []
    date = []

    for dd in d:
        date.append(dd['date'])
        vitesse.append(dd["vitesse moyenne"]*3.6)
        if dd["type"] == "tour":
            #temps.append(float(np.sum(dd['temps tour']))/60)
            distance.append(dd['distance tour']*dd['nombre tour']/1000)
        elif dd["type"] == "simple":
            distance.append(dd["distance sortie"])

    date.sort()

    if len(x) > 30:
        vitesse = vitesse[-30:]
        date = date[-30:]
        distance = distance[-30:]
        x = x[-30:]

    matplotlib.style.use('ggplot')
    plt.figure(figsize=(20,4))
    plt.plot(x, vitesse, linestyle='dashdot', marker='o', markersize="5")
    plt.ylabel("km/h")
    plt.xticks(x, list(map(lambda a : a[-2:] + '/' + a[-5:-3] + '\n' + a[:4],date)))
    plt.ylim(bottom=20, top=60)
    plt.savefig(CACHE + "distance.png", bbox_inches="tight")

