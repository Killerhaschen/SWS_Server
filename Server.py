##Server SandWirtschaftsSimulator

import socket
import threading
import sys
import random

################################################################################hu



global user
global pwrt
global key
global mapp
global userkey

global PORTS
global HOST
global BAKCLOG

HOST = ''
BACKLOG = 5
PORTS = [6666]

user = []
pwrt = []
userkey = []
mapp = []
key = []

################################################################################

def verarbeite(daten,connection,PORT):
    #print()
    #print(user,pwrt,mapp,userkey,key)
    daten = daten.decode()
    part=daten.split("$")
    if part[0]== "laden":
        laden(part,connection,PORT)
    if part[0]== "speichern":
        speichern(part,connection,PORT)
    if part[0]== "login":
        login(part,connection,PORT)  
    if part[0]== "reg":
        reg(part,connection,PORT)
    else:
        print()


def laden(daten,connection,PORT):                       ##lädt die auf dem server gespeicherte map
    global user
    global pwrt
    global mapp
    #print("laden",daten[1])
    if daten[1] in user:
        i = user.index(daten[1])
        if daten[2] == pwrt[i]:
            connection.send(mapp[i].encode())
        else:
            print("Fail")
            connection.send("FLL,Falsches Passwort".encode())
    else:
        print("Fail")
        connection.send("FLL,Falscher Benutzername".encode())

    portdel(PORT)
    
def speichern(daten,connection,PORT):                   ##empfängt map vom spieler und spichert diese
    global user
    global pwrt
    global mapp
    #print("speichern",daten[1])
    if daten[1] in user:
        i = user.index(daten[1])
        if daten[2] == pwrt[i]:
            mapp[i] = daten[3]
            save()
            connection.send("OKS".encode())
        else:
            print("Fail")
            connection.send("FLS,Falsches Passwort".encode())

    else:
        print("Fail")
        connection.send("FLS,Falscher Benutzername".encode())

 
    portdel(PORT)

    
def login(daten,connection,PORT):                       ##wenn sich jemand einloggen will
    global user
    global pwrt
    #print("login",daten[1])
    if daten[1] in user:
        i = user.index(daten[1])
        if daten[2] == pwrt[i]:
            connection.send("OKO".encode())
        else:
            print("Fail")
            connection.send("FLO,Falsches Passwort".encode())
    else:
        print("Fail")
        connection.send("FLO,Falscher Benutzername".encode())


    portdel(PORT)
    
def reg(daten,connection,PORT):                         ##wenn jemand sich registrieren will
    global user
    global pwrt
    global key
    global mapp
    global userkey
    #print("reg",daten[1])
    if daten[3] in key:
        for i in range (len(key)-1):
            if daten[3]==key[i]:
                del key[i]
        user.append(daten[1])
        pwrt.append(daten[2])
        userkey.append(daten[3])
        mapp.append("empty")
        datei = open("key.txt", "w+")
        datei.write("§".join(key))
        datei.close()
        save()
        connection.send("OKR".encode())
    else:
        print("Fail")
        connection.send("FLR,Ungultiger Key".encode())


    portdel(PORT)


def load():                             ##lädt keys und spieler aus key.txt und log.txt
    global user
    global pwrt
    global userkey
    global key
    global mapp
    datei = open("key.txt", "r")        ##lade keys aus key.txt
    for line in datei:
        teil = line.split("§")
        for i in range(len(teil)):
            key.append(teil[i])
    print("gelesende keys:",key)
    datei.close()
    
    datei = open("log.txt", "r")        ##lade daten aus log.txt
    kram = datei.readlines()
    temp = kram[0].strip()
    user = temp.split("§")
    temp = kram[1].strip()
    pwrt = temp.split("§")
    temp = kram[2].strip()
    mapp = temp.split("§")
    temp = kram[3].strip()
    userkey = temp.split("§")
    datei.close()

    print("gelesen:",user,pwrt,mapp,userkey)



def save():                             ##speichert daten in log.txt
    global user
    global pwrt
    global key
    global mapp
    global userkey
    datei = open("log.txt", "w+")
    datei.write("§".join(user))
    datei.write("\n")
    datei.write("§".join(pwrt))
    datei.write("\n")
    datei.write("§".join(mapp))
    datei.write("\n")
    datei.write("§".join(userkey))
    datei.write("\n")
    datei.close()

def portgen():
    global PORTS
    print("ports0",PORTS)
    while True:
        p = random.randint(6666,6676)
        if not p in PORTS:
            PORTS.append(p)
            return p
            break

def portdel(PORT):
    global PORTS
    print("ports1",PORTS)
    del PORTS[PORTS.index(PORT)]
    print("ports2",PORTS)
    sys.exit()
    

def connect():
    global HOST
    global BACKLOG
    PORTx = 6666
    sockel = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sockel.bind((HOST,PORTx))
    sockel.listen(BACKLOG)
    while True:
        connection, remoteadress = sockel.accept()
        while True:
            daten = connection.recv(512)
            if not daten:
                break
            elif daten.decode()=="con":
                PORT = portgen()
                #print(PORT,PORTS)
                connection.send(str(PORT).encode())
                connection.close()
                event = threading.Event()
                haupt = threading.Thread(target=mainwt, args=(PORT, event))
                haupt.start()
                break
            else:
                print(daten.decode())




def mainwt(PORT,event):
    print("MAIN",PORT)
    global HOST
    global BAKCLOG
    PORT = int(PORT)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST,PORT))
    sock.listen(BACKLOG)
    while True:
        connection, remoteadress = sock.accept()
        #print("Verbindung mit IP: ",remoteadress)
        while True:
            daten = connection.recv(512)
            if not daten:
                break
            verarbeite(daten,connection,PORT)
        connection.close()


def main(PORT):
    global HOST
    global BAKCLOG
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST,PORT))
    sock.listen(BACKLOG)
    while True:
        try:
            connection, remoteadress = sock.accept()
            print("Verbindung mit IP: ",remoteadress)
            while True:
                daten = connection.recv(512)
                if not daten:
                    break
                verarbeite(daten,connection)
            connection.close()
        except:
            print("Verbindung getrennt")
            print()
            print()

def terminal():
    while True:
        bef = str(input("Server:"))
        if bef =="stop":
            print("Server fährt runter")
            sys.exit()
        elif bef =="p":
            print(user,pwrt,mapp,userkey)


################################################################################

load()
console = threading.Thread(target=terminal)
connect = threading.Thread(target=connect)

#console.start()
connect.start()
