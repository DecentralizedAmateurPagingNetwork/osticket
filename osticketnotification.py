#!/usr/bin/python
# -*- coding: utf-8 -*-

# adapted from https://github.com/DL7FL/DAPNET/blob/master/DAPNET/senden.py

import MySQLdb as mdb
import sys
import requests
from requests.auth import HTTPBasicAuth
import os
import json


###############################################################################
#  Daten in Variablen Speichern
###############################################################################

# Konstante

login = 'osticket'    #  DAPNET Benutzername
passwd = 'nothere'  #  DAPNET Passwort


url = 'http://www.hampager.de:8080/calls'  #  Versenden uebers Internet

callsign_list = ["dh3wr"]  # eins oder mehrere Emfaenger Rufzeichen
txgroup = "dl-all"  #  Sendergruppe zB. DL-all für alle Sender in Deutschland

###############################################################################
# Funktionen definieren
###############################################################################

def send(text, callsign, txgroup, login, passwd, url): # json modul
        # print(callsign)
        json_string = '''{"text": "''' + text + '''", "callSignNames": ["''' + callsign + '''"], "transmitterGroupNames": ["''' + txgroup + '''"], "emergency": false}'''
#       print(json_string)
        response = requests.post(url, data=json_string, auth=HTTPBasicAuth(login, passwd)) # Exception handling
        print(response.status_code) # return

def sendmulti(text, callsign_list, txgroup, login, passwd, url): # json modul
        # print(callsign)
        json_string = '''{"text": "''' + text + '''", "callSignNames": ''' + callsign_list + ''', "transmitterGroupNames": ["''' + txgroup + '''"], "emergency": false}'''
#        print(json_string)
        response = requests.post(url, data=json_string, auth=HTTPBasicAuth(login, passwd)) # Exception handling
        print(response.status_code) # return


def Single_Callsign(callsign_list):  #  Rufzeichen vereinzelt und ruft mit jedem Rufzeichen die Senden Funktion auf.
        for callsign in callsign_list:
                # print(callsign)
                send(text, callsign, txgroup, login, passwd, url)



try:
    con = mdb.connect('localhost', 'osticket', 'NOTTHISONE', 'osticket');

    cur = con.cursor(mdb.cursors.DictCursor)
    delstatement = "DELETE FROM `notifications` WHERE `id` = %s"


# Get current agents and their callsigns
    cur.execute("SET NAMES 'utf8'")
    cur.execute("SELECT `username` FROM `ost_staff` WHERE `onvacation` = 0")
    rows = cur.fetchall()
    callsign_list = [row["username"] for row in rows]
#    print callsign_list
    callsign_list_json = json.dumps(callsign_list)
#    print callsign_list_json


# Created tickets
    cur.execute("SELECT id, subject, timestamp FROM `notifications` WHERE `state`='created'")
    rows = cur.fetchall()
    for row in rows:
        text = "NEW DAPNET Ticket %s"%(row["subject"])
        print text
        sendmulti(text, callsign_list_json, txgroup, login, passwd, url)
        cur.execute(delstatement, (row["id"],))
        con.commit()

# Assigned tickets
    cur.execute("SELECT id, username, assignedusername, subject, timestamp FROM `notifications` WHERE `state`='assigned'")
    rows = cur.fetchall()
    for row in rows:
        text = "DAPNET Ticket assigned to %s by %s:%s "%(row["assignedusername"],row["username"],row["subject"])
        print text
        sendmulti(text, callsign_list_json, txgroup, login, passwd, url)
        cur.execute(delstatement, (row["id"],))
        con.commit()

# Closed tickets
    cur.execute("SELECT id, username, subject, timestamp FROM `notifications` WHERE `state`='closed'")
    rows = cur.fetchall()
    for row in rows:
        text = "DAPNET Ticket closed by %s:%s "%(row["username"],row["subject"])
        print text
        sendmulti(text, callsign_list_json, txgroup, login, passwd, url)
        cur.execute(delstatement, (row["id"],))
        con.commit()


except mdb.Error, e:

    print "Error %d: %s" % (e.args[0],e.args[1])
    sys.exit(1)

finally:

    if con:
        con.close()
