import socket
import threading
import pickle

HOST = '127.0.0.1'
PORT = 23232    
massage_ = []


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
nicknames = []


def trade(message):
    for client in clients:
        client.send(message)

def masseger(client):
    while True:
        try:
            message = client.recv(1024)
            massage_.append(message)
            trade(message)
            file = open('massage_history.txt',mode='a')
            file.write(str(message))
            file.write('\n')
            file.close()
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            trade('{} left!'.format(nickname).encode('utf-8'))
            nicknames.remove(nickname)
            break

def data_r():
    while True:
        client, address = server.accept()
        print("Соединение с {}".format(str(address)))
        client.send('nickname'.encode())
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)
        print("Подключился {}".format(nickname))
        trade("{} подключился!".format(nickname).encode('utf-8'))
        client.send('Приятного время провождения!'.encode('utf-8'))
        thread = threading.Thread(target=masseger, args=(client,))
        thread.start()

data_r()
