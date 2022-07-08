# need ipython!

## https://www.geeksforgeeks.org/how-to-parse-local-html-file-in-python/
## https://realpython.com/python-web-scraping-practical-introduction
## https://stackoverflow.com/questions/15138614/how-can-i-read-the-contents-of-an-url-with-python
## https://lerneprogrammieren.de/beautiful-soup-tutorial/

# Importing BeautifulSoup class from the bs4 module
import bs4 
import requests
import urllib.request
import urllib
import time

# import argparse
from xml.dom import minidom
import codecs
from kellermeisterdef import *

Map = {
'Alkoholgehalt':     ['alcoholStrength', '% Vol.'],  # : : 13,76% Vol.
'Restzucker':        ['sugar',           ' g/l'],    # : 3,7 g/l
'Gesamtsäure':       ['acidity',         ' g/l'],    # : 4,4 g/l
'Kategorie':         [None,              ''],        # : Wein 
'Land':              ['country',         ''],        # : Frankreich
'Region':            ['region',          ''],        # : Lirac, Rhônetal
'Qualitätsstufe':    ['appellation',     ''],        # : Lirac Appellation d’Origine Protégée
'Füllmenge':         ['volume',          ' Liter'],  # : 0,75 Liter
'Rebsorten':         ['varietal',        ''],        # : Syrah, Grenache, Mourvèdre
'Weinstil':          [None,              ''],        # : körperreich & vollmundig
'Trinkreife':        [None,              ''],        # KOMPLIZIERTER
# 'Trinkreife':      ['bestAge',         ''],        # : jetzt und weitere 3-4 Jahre
'Trinktemperatur':   [None,              ' °C'],     # :  # : 16 °C
'Verschlussart':     [None,              ''],        # : Kork
'Artikelnummer':     [None,              '']         # : 25623
}

def debug(s):
    return None

def replaceText(node, newText):
    if node.firstChild.nodeType != node.TEXT_NODE:
        raise Exception("node does not contain text")
    node.firstChild.replaceWholeText(newText)
  
def jacques(link,e) :
    Ret = []
    
    # Opening the html file
    ## HTMLFile = open("index.htm", "r")
    # link = 'https://www.jacques.de/dm.php?p=1&m=25623&g=1'
    HTMLFile = urllib.request.urlopen(link)
    
    if HTMLFile is None : 
        return None
    
    # Reading the file
    index = HTMLFile.read()
    
    if index is None : 
        return None
    
    # Creating a BeautifulSoup object and specifying the parser
    S = bs4.BeautifulSoup(index, 'lxml')
    
    P = S.find(class_="name")
    if P is not None:
        # Ret.append((m[0],t))
        print("Könnte den Namen verwenden: " + P.text)

    P = S.find(class_="region")
    if P is not None:
        Ret.append(('region',P.text))

    P = S.find(class_="details")
    ## hier noch: Typus: Rotwein

    P = S.find(class_="products-informations")
    if P is None : 
        return Ret
    R = P.find_all(class_="row")
    for l in R :
        a = l.find(class_="colA")
        c = l.find(class_="colC")
        if a is not None  :
            debug(str(a.text) + ' : ' + str(c.text))
            m = Map[a.text.strip(':')]
            if m[0] is not None :
                d = len(m[1])
                t = c.text
                if d > 0 : 
                    T = t.replace(",",".") # ersetze , durch . in Zahlen
                    t = T[:-d]             # lösche Maßangaben
                    print('Ersetze ' + str(m[0]) + ' durch ' + t + ' strip ' + str(d) + ' chars')
                else :
                    print('Ersetze ' + str(m[0]) + ' durch ' + t)
                debug('Set Attribute ' + m[0] + ' to ' + t)
                Ret.append((m[0],t))
    return Ret

for s in storage :
    R = None
    c = getEntry(s,'scancode').decode(codec)
    if "jacques.de" in c :
        debug(c)
        if "http" in c : 
            R = jacques(c,s)
        else :
            R = jacques('http://' + c,s)
    if R is not None :
        for r in R :
                node = s.getElementsByTagName(r[0])
                if len(node) > 0 :
                    debug('Replace ' + r[0] + ' by ' + r[1])
                    replaceText(node[0],r[1])

# Opening a file using a "with open" block automatically
# closes it at the end of the block
with open('storages.tmp', 'w') as f:
    for s in storage :
        print(s.toxml(),file=f)

