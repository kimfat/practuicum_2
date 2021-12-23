import socket
import threading
import pickle

nickname = input("Введите ваше имя: ")
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 23232))
def code():
    sock = socket.socket()
    sock.connect(('127.0.0.1', 23232))

    p, g, a = 7, 5, 3
    A = g ** a % p
    history = open('history.txt','a')
    history.write('Ключ клиента: ')
    history.write(str(A))
    history.write('\n')
    history.close()
    sock.send(pickle.dumps((p, g, A)))

    sock.close()
def data_r():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'nickname':
                client.send(nickname.encode('utf-8'))
            else:
                print(message)
        except:
            print("Ошибка!")
            client.close()
            break

def write_to_name():
    while True:
        message = '{}: {}'.format(nickname, input(''))
        client.send(message.encode())

receive_thread = threading.Thread(target=code('utf-8'))
receive_thread.start()

receive_thread = threading.Thread(target=data_r('utf-8'))
receive_thread.start()

write_thread = threading.Thread(target=write_to_name())
write_thread.start()