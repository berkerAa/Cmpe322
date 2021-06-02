import socket, os, subprocess, json, ssl, threading, logging, time, selectors
from datetime import datetime
import requests
class Server:
    def __init__(self):
        self.selector =  selectors.DefaultSelector()
        self.databaseHolder = self.read()
        self.databaseWriter = lambda x : self.write(x)
        self.executeBash = lambda x: subprocess.Popen(x, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0]
        self.encoder = lambda x: x.encode()
        self.decoder = lambda x: x.decode()
        self.readMessage = lambda x: self.decoder(x.recv()) # x represents socket
        self.writeMessage = lambda x, y: x.sendall(self.encoder(y)) # x represents socket, y represents raw message
        #self.NoneGUIOperator = lambda x: self.writeMessage(x, input()) # Terminal Operatior for None GUI use case
        self.lock = threading.Lock()
        self.context = self.initContext()
        self.clients = {}
        self.wakeServer()
        self.Codes = {
            100: 'direct({}, {})'
        }
    def initContext(self) -> ssl.SSLContext:
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain('Cert/domain.crt', 'Cert/domain.key')
        return context
    def wakeServer(self):
        client = 0
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
                sock.bind(('192.168.1.102', 15000)) # needed to be configured for spesific host machine, can be automized wit using executeBash command
                sock.listen()
                ssock = self.context.wrap_socket(sock, server_side=True)
                while True:
                    print(client)
                    self.clients[client] = [0, 0]
                    #self.clients[client][1] = ssock
                    self.clients[client][0], addr = ssock.accept()
                    print('connection from: ', addr)
                    #self.clients[client] = (conn, ssock)
                    threading.Thread(target=self.clientHandler, args=(self.clients[client][0], client)).start()
                    print('Proceed')
                    client += 1
                    print(client)
        except Exception as e:
            print(e)
    
    def is_socket_closed(self, sock: socket.socket) -> bool:
        try:
            # this will try to read bytes without blocking and also without removing them from buffer (peek only)
            data = sock.sendall('Check'.encode())
            return False
        except BlockingIOError:
            return False  # socket is open and reading from it would block
        except ConnectionResetError:
            return True  # socket was closed for some other reason
        except KeyError:
            return True
        except Exception as e:
            print("unexpected exception when checking if a socket is closed")
            print(e)
            return True
        return False
    def loginNonGUI(self, conn, connID):
        schoolID = self.readMessage(conn)
        password = self.readMessage(conn)
        if schoolID in self.databaseHolder.keys():
            if password == self.databaseHolder[schoolID]['Password']:
                self.databaseHolder[schoolID]['Online'] = True
                self.clients[schoolID] = self.clients.pop(connID)
                self.writeMessage(conn, 'Server,True')
                print('all is wel')
                return 1, schoolID
            
        return 0, schoolID
    def signUp(self, conn, connID):
        #self.writeMessage(conn, 'Please enter your School ID: ')
        schoolID = self.readMessage(conn)
        self.databaseHolder[schoolID] = {}
        for key in ('Name', 'Surname', 'Mail Address', 'Citizenship', 'Password'):
            #self.writeMessage(conn, 'Please enter your {}: '.format(key))
            self.databaseHolder[schoolID][key] = self.readMessage(conn)
        self.databaseHolder[schoolID]['Online'] = False
        self.writeMessage(conn, 'Server,True')
        self.write(self.databaseHolder)
        self.clients[schoolID] = self.clients.pop(connID)
        self.databaseHolder[schoolID]['Online'] = True
        return True, schoolID
    def direct(self, direction, msg, conn, ID):
            if  self.databaseHolder[direction]['Online']:
                    if not self.is_socket_closed(self.clients[direction][0]):
                       # self.writeMessage(conn, '')
                        #msg = self.readMessage(conn)
                        with self.lock :
                            with open('Database/msgHistory.txt', 'a') as f:
                                f.write("'Sender': {},'Reciver': {},'data': {},'Time Stamp': {}\n".format(ID, direction, msg, datetime.now().strftime('%m/%d/%Y, %H:%M:%S')))
                        msg = ID + ',' + msg

                        self.writeMessage(self.clients[direction][0], msg)

                    else:
                        self.clients[direction][0].close()
            
            
    def clientHandler(self, conn: socket.socket, client: int):
        recThread, writeThread = 1, 1
        #self.writeMessage(conn, 'Hello, please enter login if you have an account, otherwise, type sign up')
        print('proceed')
        msg = self.readMessage(conn)
        print('Someone Connected')
        if msg.lower() == 'sign up':
            loginCheck, ID =  self.signUp(conn, client)
            
           # self.writeMessage(conn, 'forwarding to Login phase')
        else:
            loginCheck, ID = self.loginNonGUI(conn, client)
        if loginCheck:
            while not (self.is_socket_closed(conn)):
                    rawMessage = self.readMessage(conn)
                    print(rawMessage)
                    if rawMessage == '200':
                        self.writeMessage(conn, 'Server,' + ','.join([_id for _id in self.databaseHolder.keys() if self.databaseHolder[_id]['Online']]) + '-' + ','.join([_id for _id in self.databaseHolder.keys() if not self.databaseHolder[_id]['Online']]))
                
                    elif rawMessage != '':
                        self.direct(rawMessage.split(',')[0], ','.join(rawMessage.split(',')[1:]), conn, ID)
            self.clients[ID][0].close()
            self.databaseHolder[ID]['Online'] = False
        else:
            self.writeMessage(conn, 'Creds are wrong: ')
            self.clientHandler(self.clients[client][0], client)
    def read(self):
        with open('Cert/Database.pem', 'r') as f:
            key = ''.join([i[:-1] for i in f.readlines()]) 
        print(key)
        r = requests.post('http://192.168.1.102:15001/', json={'auth': key, 'request': 'get'})
        if r.status_code != 200:
                print('Auth Token failed')
        else:
            print(r.json())
            return r.json()
        #with open('Database/loginCreds.json', 'r') as f: 
            #return json.load(f)
        
    def write(self, data):
        with open('Cert/Database.pem', 'r') as f:
            key = ''.join([i[:-1] for i in f.readlines()]) 
        r = requests.post('http://192.168.1.102:15001/', json={'auth': key, 'request': 'write', 'info': data})
        if r.status_code != 200:
                print('Auth Token failed')
        else:
            print(r.json())
            #return r.json()
        #try: 
        #    with open('Database/loginCreds.json', 'w') as f:
        #        json.dump(data, f)
         #       return 1
        #except Exception as e:
        #    print(e)
        #    return 0
if __name__ == "__main__":
    Server()