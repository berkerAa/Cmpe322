from Client import Ui_MainWindow
from ChatRoot import Ui_MainWindow as chatRoot
from PyQt5 import QtCore, QtGui, QtWidgets
import socket, ssl, threading, time

class Client():
    def __init__(self):
        #self.server = 'vivalarevolucion.tplinkdns.com'
        #self.port = '65320'
        self.logged = False
        self.server , self.port = '192.168.1.102', 15000
        self.Cert = 'Cert/domain.crt'
        self.context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        self.context.load_verify_locations('Cert/domain.crt')
        self.msg = {"Server": []}
        self.Online = []
        self.Offline = []
        self.flush = lambda sock, msg: sock.send(msg.encode())
    def getOnline(self):
        self.flush(self.WrappedSock, '200')
        print('Ok')
        while True:
            if len(self.msg['Server']) == 0:
                time.sleep(0.7)
            else:
                self.OnlinePersons = self.msg['Server'].pop()
                break
    def connect(self):
        self.sock = socket.create_connection((self.server, self.port))
        self.WrappedSock = self.context.wrap_socket(self.sock, server_hostname='Cmpe322')
        threading.Thread(target=self.stdOUT, args=(self.WrappedSock, )).start()
    def stdOUT(self, msg):
        while True:
            tmp = msg.recv().decode()
            print(tmp)
            if tmp != 'Check':
                key, data = tmp.split(',')[0], ','.join(tmp.split(',')[1:])
                print(key, data)
                if key in list(self.msg.keys()):
                    self.msg[key].append(data)
                else:
                    self.msg[key] = []
                    self.msg[key].append(data)
                print(self.msg)
def runLogin(client):
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    Login_ui = Ui_MainWindow(client)
    Login_ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
    return MainWindow, app
def runRoot(client, MainWindow, app):
    #MainWindow = QtWidgets.QMainWindow()
    print('??')
    Root_ui = chatRoot(client)
    Root_ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
if __name__ == "__main__":
    import sys
    client = Client()
    MainWindow, app = runLogin(client)
    