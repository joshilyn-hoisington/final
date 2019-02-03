import sqlite3
import csv
import json
# import itertools
import pandas as pd
import requests
import urllib
from urllib.request import urlretrieve
import shutil
from bs4 import BeautifulSoup
# import urllib.request
import urllib.parse
import re
import readchar
import os
from requests_html import HTMLSession
# import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from flask import Flask, request, render_template, redirect
import plotly.plotly as py
import plotly.graph_objs as go
import plotly.tools as tls
import html
from collections import Counter
# import multiprocessing
import requests_cache
# from Pillow import Image
import glob
import matplotlib.image as mpimg
from io import BytesIO

requests_cache.install_cache(cache_name='agencies_storage', backend='sqlite', expire_after=999)


sw = stopwords.words("english")

DBNAME = 'agencies.db'



def create_db():

    
    

    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()


    statement = '''
        DROP TABLE IF EXISTS 'AgencyOne';
    '''
    cur.execute(statement)

    statement = '''
        DROP TABLE IF EXISTS 'AgencyTwo';
    '''
    cur.execute(statement)

    statement = '''
        DROP TABLE IF EXISTS 'Logos';
    '''
    cur.execute(statement)

    
    conn.commit()

    
    
    statement = '''
        CREATE TABLE 'AgencyOne' (
            'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'Title' TEXT NOT NULL,
            'DocumentNumber' TEXT NOT NULL,
            'Html' TEXT NOT NULL,
            'Pdf' TEXT NOT NULL,
            'PublicationDate' TEXT NOT NULL,
            'FullText' TEXT NOT NULL
        );
    '''
    cur.execute(statement)

    statement = '''
        CREATE TABLE 'AgencyTwo' (
            'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'Title' TEXT NOT NULL,
            'DocumentNumber' TEXT NOT NULL,
            'Html' TEXT NOT NULL,
            'Pdf' TEXT NOT NULL,
            'PublicationDate' TEXT NOT NULL,
            'FullText' TEXT NOT NULL
        );
    '''
    cur.execute(statement)



    statement = '''
        CREATE TABLE 'Logos' (
            'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'Department' TEXT NOT NULL,
            'Logo' VARBINARY NOT NULL
        );
    '''
    cur.execute(statement)


    
    conn.commit()

    conn.close()




def populate_DB(ageOne, ageTwo):

  
    image_list = []
    name_list = []
    bigdogs = glob.iglob('cab_logos/*.png')
    for filename in bigdogs: 
        with open(filename, "rb") as TheBeachBoys:
            image_list.append((filename[10:-4].replace("-", " "), bytearray(TheBeachBoys.read())))

    

    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    

    cur.execute("BEGIN TRANSACTION;")
    for result in image_list:
        # sito_uffiziale = result['html_url']
        # fullTexto = getting_the_full_text(sito_uffiziale)
        insertion = (None, result[0], result[1])
        statement = 'INSERT INTO "Logos" '
        statement += 'VALUES (?, ?, ?)'
        cur.execute(statement, insertion)
        print(".")

    cur.execute("COMMIT;")




    

    
    print("starting now")
    cur.execute("BEGIN TRANSACTION;")
    for result in ageOne:
        # sito_uffiziale = result['html_url']
        # fullTexto = getting_the_full_text(sito_uffiziale)
        insertion = (None, result['title'], result['document_number'], result["html_url"], "blank for now", result['publication_date'], result["raw_text_url"])
        statement = 'INSERT INTO "AgencyOne" '
        statement += 'VALUES (?, ?, ?, ?, ?, ?, ?)'
        cur.execute(statement, insertion)
        print(".")

    cur.execute("COMMIT;")

    


    print("second one")
    cur.execute("BEGIN TRANSACTION;")
    for result in ageTwo:
        # sito_uffiziale = result['html_url']
        # fullTexto = getting_the_full_text(sito_uffiziale)
        insertion = (None, result['title'], result['document_number'], result["html_url"], "blank for now", result['publication_date'], result['raw_text_url'])
        statement = 'INSERT INTO "AgencyTwo" '
        statement += 'VALUES (?, ?, ?, ?, ?, ?, ?)'
        cur.execute(statement, insertion)
        print("*")
    cur.execute("COMMIT;")




    conn.commit()
    conn.close()


def getting_the_data(agencie1, agencie2):

    fed_reg_agency1 = 'http://www.federalregister.gov/api/v1/documents.json?fields%5B%5D=body_html_url&fields%5B%5D=dates&fields%5B%5D=document_number&fields%5B%5D=full_text_xml_url&fields%5B%5D=html_url&fields%5B%5D=json_url&fields%5B%5D=mods_url&fields%5B%5D=pdf_url&fields%5B%5D=president&fields%5B%5D=publication_date&fields%5B%5D=raw_text_url&fields%5B%5D=title&per_page=5&order=relevance&conditions%5Bagencies%5D%5B%5D=' + agencie1
    fed_reg_agency2 = 'http://www.federalregister.gov/api/v1/documents.json?fields%5B%5D=body_html_url&fields%5B%5D=dates&fields%5B%5D=document_number&fields%5B%5D=full_text_xml_url&fields%5B%5D=html_url&fields%5B%5D=json_url&fields%5B%5D=mods_url&fields%5B%5D=pdf_url&fields%5B%5D=president&fields%5B%5D=publication_date&fields%5B%5D=raw_text_url&fields%5B%5D=title&per_page=5&order=relevance&conditions%5Bagencies%5D%5B%5D=' + agencie2


    fed_reg1 = requests.get(fed_reg_agency1)
    fed_reg2 = requests.get(fed_reg_agency2)
    fed_data1 = json.loads(fed_reg1.text)
    fed_data2 = json.loads(fed_reg2.text)

    fed_results1 = fed_data1['results']

    fed_results2 = fed_data2['results']

    return fed_results1, fed_results2




# def getting_the_full_text(site):
#     webpage = urllib.request.urlopen(site)
#     soup = BeautifulSoup(webpage,'lxml')
#     result = soup.find_all('a')
#     for cockamayme in result:
        
#         if cockamayme.text == "XML: Original full text XML":
#             this_is_it = cockamayme.attrs['href']
#         elif cockamayme.text == "a basic text format":
#             this_is_it = cockamayme.attrs['href']
#     # print(this_is_it)
#     # try:
#     site=this_is_it
#     hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#     'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
#     'Accept-Encoding': 'none',
#     'Accept-Language': 'en-US,en;q=0.8',
#     'Connection': 'keep-alive'}

#     # req = urllib.urlopen(site, headers=hdr)


#     try:
#         omgzz = urllib.request.urlopen(this_is_it)
#         omgzz = omgzz.text
#     except:
#         session = HTMLSession()
#         omgzz = session.get(this_is_it).html.text

#     return omgzz






def gaining_access():



    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    statement = f'''
            SELECT *
            FROM AgencyOne
            ;   '''
    # conn.set_trace_callback(print)
    cur.execute(statement)

    finale = cur.fetchall()

    dicky1 = {}
    resultListOne = []   
    for haha in finale:
        dicky1[haha[2]] = (haha[5], haha[6])
        # resultListOne.append(entrie)

    cur = conn.cursor()
    statement = f'''
            SELECT *
            FROM AgencyTwo
            ;   '''
    # conn.set_trace_callback(print)
    cur.execute(statement)

    finale = cur.fetchall()

    dicky2 = {}
    resultListTwo = []   
    for haha in finale:
       
        dicky2[haha[2]] = (haha[5], haha[6])
        # resultListOne.append(entrie)
        
        
        

    return dicky1, dicky2
    conn.close()


def count_the_words(keyword, agencylist1, agencylist2):

    print("starting 2 count")
    

    counto1 = {k: ( v[0], Counter(word_tokenize(urllib.request.urlopen(v[1]).read().decode('utf-8')))[keyword] ) for k, v in agencylist1.items()}
    counto2 = {k: ( v[0], Counter(word_tokenize(urllib.request.urlopen(v[1]).read().decode('utf-8')))[keyword] ) for k, v in agencylist2.items()}
    
    print("here finisheth the counting process")
    
    return counto1, counto2




def plot_the_frequencies(return_from_count_function, aggy1, aggy2):

    x1 = []
    x2 = []
    y1 = []
    y2 = []

    for k, v in return_from_count_function[0].items():
        x1.append(v[0])
        y1.append(v[1])


    for k, v in return_from_count_function[1].items():
        x2.append(v[0])
        y2.append(v[1])
        


    trace0 = go.Scatter(
    x = x1,
    y = y1,
    name = aggy1
    )

    trace1 = go.Scatter(
    x = x2,
    y = y2,
    name = aggy2
    )

    data = [trace0, trace1]

    layout = go.Layout(
    title="Let's Compare!",
    xaxis=dict(
        title='Date',
        titlefont=dict(
            family='Courier New, monospace',
            size=18,
            color='#7f7f7f'
        )
        ),
    yaxis=dict(
        title='Word Frequency',
        titlefont=dict(
            family='Courier New, monospace',
            size=18,
            color='#7f7f7f'
        )
        )
        )

    fig = go.Figure(data=data, layout=layout)
    this_is_the_graph_ull_embed = py.plot(fig, filename='scatter-mode', auto_open=False)
    # this_is_the_graph_ull_embed = py.plot(fig, filename='basic-bar', auto_open=False)
    return this_is_the_graph_ull_embed

# print (count_the_words('a', gaining_access()[0], gaining_access()[1]))


create_db()
master_graph = None

# print( plot_the_frequencies( count_the_words("the", gaining_access()[0], gaining_access()[1])))

#################################FLASK APP BEGINS HERE#########################################

app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template('comparer.html')

@app.route('/', methods=['POST'])
def my_form_post():
    mainword = request.form['keyword']
    cabAg1 = request.form['agency1']
    cabAg2 = request.form['agency2']
    plug_in = getting_the_data(cabAg1, cabAg2)
    populate_DB(plug_in[0], plug_in[1])
    master_graph = plot_the_frequencies( count_the_words(mainword, gaining_access()[0], gaining_access()[1]), cabAg1, cabAg2)
    master_img = master_graph.replace("html", "png")
    insert = str('<div><a href=\"' + str(master_graph) + ' \"target=\"_blank\" title=\"scatter-mode\" style=\"display: block; text-align: center;\"><img src=\"' + str(master_img) + '.png\"" alt="scatter-mode\" style=\"max-width: 100%;width: 600px;\"  width=\"600\" onerror=\"this.onerror=null;this.src=\'https://plot.ly/404.png\';\" /></a></div>')
    

    ##

    conn = sqlite3.connect(DBNAME)
    
    cur = conn.cursor()
    
    statement = f'''
            SELECT Logo
            FROM Logos
            WHERE Department = "{cabAg1.replace("-", " ")}"
            ;   '''
    # conn.set_trace_callback(print)
    cur.execute(statement)

    agency1_logo = cur.fetchone()

    statement = f'''
            SELECT Logo
            FROM Logos
            WHERE Department = "{cabAg2.replace("-", " ")}"
            ;   '''
    # conn.set_trace_callback(print)
    cur.execute(statement)

    agency2_logo = cur.fetchone()

    ##

    conn.close()
 
    yakka = Image.open(BytesIO(agency1_logo[0]))
    print(yakka)
    ##logoo1 = "<img src=\"data:image/png;base64," + str(agency1_logo[0])[2:-1] + "\" alt=\"\" />"
    ##logo1 = json.dumps(logoo1)

    ##logo2 = "<img>" + agency2_logo[0].decode('utf-8', 'ignore') + "</>"

    return render_template('comparer.html', value=insert, logo1=logo1, logo2=logo2)
    



if __name__=="__main__":
    
    app.run(debug=True)




