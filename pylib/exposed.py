import eel
from pylib.default_variable import *
import pylib.data_processing as dp
from numpy import round
from datetime import timedelta
import os



def return_html(html_filename, f_string=False, div_dir=DIV_DIR):
    with open(div_dir + html_filename, 'r') as html_f:
        html = html_f.read()
    if f_string != False:
        html = html.format(**f_string)
    return html

@eel.expose
def div_dashboard():
    filename = PAGE1
    html = return_html(filename)
    return html

@eel.expose
def div_complete(n):

    #SUB HTML
    filename_tour = PAGE2_SUB
    sub_html = ""
    n = int(n)
    for i in range(1,n+1):
        f_string = {"i" : i}
        sub_html += return_html(filename_tour, f_string)

    filename = PAGE2
    f_string = {"div_tour_input" : sub_html, "distance_tour" : DISTANCE_TOUR, "distance_allez" : DISTANCE_ALLEZ, "distance_retour" : DISTANCE_RETOUR}
    html = return_html(filename, f_string)
    return html

@eel.expose
def div_simple():
    return return_html(SIMPLE_FORM)

@eel.expose
def div_stat(data):
    f_string = {"data" : data["date"], "distance" : data["distance sortie"], "time" : data["temps sortie"], "vitesse" : data["vitesse moyenne"]}
    html =  return_html(DIV_STAT, f_string)
    with open(CACHE + "stat.html", 'w') as f:
        f.write(str(html))
    return html

@eel.expose
def div_stat_tmp():
    return return_html("stat.html", div_dir=CACHE);

@eel.expose
def receive_data(data):
    data = dp.process_data(data)
    dp.update_database(data)
    return data

@eel.expose
def receive_data_simple(data):
    data = dp.process_simple_data(data)
    dp.update_database(data)
    data["distance sortie"] = str(round(data["distance sortie"] / 1000, 1)) + ' km'
    data["vitesse moyenne"] = str(round(data["vitesse moyenne"]*3.6 ,1)) + ' km/h'
    data["temps sortie"] = str(timedelta(seconds=data["temps sortie"]))
    return data

@eel.expose
def query_jour(date):
    ans = dp.query_jour(date)
    if ans == False:
        return
    dp.graph_jour(ans)
    if os.path.exists(CACHE + "stat.html"):
        os.remove(CACHE + "stat.html")

@eel.expose
def query_period():
    ans = dp.query_period()
    if ans != []:
        dp.graph_period(ans)

@eel.expose
def stat_or_tour():
    if os.path.exists(CACHE + "stat.html"):
        return 1
    else:
        return 0
        



   