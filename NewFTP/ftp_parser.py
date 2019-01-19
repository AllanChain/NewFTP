with open('ftp_server.txt','r',encoding='utf-8') as f:
    COMPLETE_SERVER = f.readline()[:-1].split(':')
    ENCODING = f.readline()[:-1]
HOST,PORT = COMPLETE_SERVER
PORT = int(PORT)
if PORT == 21:
    SERVER = HOST
else:
    SERVER = COMPLETE_SERVER
