##Client SandWirtschaftsSimulator

import socket
import sys

################################################################################

HOST = '127.0.0.1'
PORT = 6666

user = "Heino"
pwrt = "blah"
key = "ABCDEF"
mapp = "WSWSWSWSSWSWW"

################################################################################

def laden(user,pwrt):
    PORT = connect(user)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    print("laden")
    sende = 'laden'+'$'+user+'$'+pwrt
    sock.send(sende.encode())
    ant = sock.recv(1024).decode()
    sock.close()
    
    print(ant)
    return ant
    
    
    
def speichern(user,pwrt,mapp):
    PORT = connect(user)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    print("speichern")
    sende = 'speichern'+'$'+user+'$'+pwrt+'$'+mapp
    sock.send(sende.encode())
    ant = sock.recv(64).decode()
    sock.close()
    
    print(ant)
    return ant
    
def login(user,pwrt):
    PORT = connect(user)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    print("login")
    sende = 'login'+'$'+user+'$'+pwrt
    sock.send(sende.encode())
    ant = sock.recv(64).decode()
    sock.close()
    
    print(ant)
    return ant


def reg(user,pwrt,key):
    PORT = connect(user)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    print("reg")
    sende = 'reg'+'$'+user+'$'+pwrt+'$'+key
    sock.send(sende.encode())
    ant = sock.recv(64).decode()
    sock.close()
        
    print(ant)
    return ant


def connect(user):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    
    sende="con"
    sock.send(sende.encode())
    PORT2 = sock.recv(64).decode()
    sock.close()
    try:
        PORT2=int(PORT2)
    except:
        print("Feher Port ist kein Integer!!")
        sys.exit()
    return PORT2
    
    
################################################################################


"""
while True:
    print()
    x = input("Was ? l,s,o,r")
    if x == "l":
        laden(user,pwrt)
    elif x == "s":
        speichern(user,pwrt,mapp)
    elif x == "o":
        login(user,pwrt)
    elif x == "r":
        reg(user,pwrt,key)

 """       
"""
reg(user,pwrt,key)
speichern(user,pwrt,mapp)
laden(user,pwrt)
login(user,pwrt)
"""
while True:
    login(user,pwrt)
    
