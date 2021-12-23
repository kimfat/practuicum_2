import socket
import os
import shutil
from datetime import datetime
print(
'show - показывает рабочую директорию \n'
'ls - показывает, что хранится в директрии \n'
'send - отправляет содержимое файла \n'
'mkdir - создаёт папку \n'
'rmdir - удаляет папку \n'
'remove - удалить файл \n'
'rename (Сначало старое имя потом через пробел новое) - переименовать файл \n'
'copyserv -  с клиента серверу \n'
'copyclient - с сервера клиенту \n'
'exit - отключение \n'
'login ')
def change(port,server_socket):
    while(True):
        try:
            server_socket.bind(('',port))
        except socket.error:
            port+=1
        else:
            break
    return port
def check(path):
    global userdir
    fullpath = str() 
    if os.path.isabs(path):
        fullpath = path
    else:
        fullpath = os.path.join(userdir,path)
    if userdir in fullpath:
        return True
    else:
        print("Доступ запрещён!")
    return False
def show():
    global userdir
    return "Директория пользователя " + userdir
def ls(path):
    return "Содержимое директории " + path + ":\n" + "; ".join(os.listdir(path))
def sm(filename):
    global userdir
    fullpath = str()
    content = str()
    if os.path.isabs(filename):
        fullpath = filename
    else:
        fullpath = os.path.join(userdir,filename)
    if os.path.exists(fullpath):
        with open(fullpath, "r") as f:
            for line in f:
                content+=line
        return "Содержимое файла " + fullpath + ":\n" + content
def mkdir(path):
    global userdir
    if check(path):
        fullpath = os.path.join(userdir,path)
        if not os.path.exists(fullpath):
            os.mkdir(fullpath)
            return "Создана папка " + fullpath
    return "Ошибка доступа к директории " + path
def rmdir(path):
    global userdir
    fullpath=""
    if not os.path.isabs(filename):
        fullpath=os.path.join(userdir,filename)
    if check(fullpath) and os.path.exists(fullpath):
        shutil.rmtree(fullpath)
        return  "Удалена папка " + fullpath
    return "Ошибка доступа к директории " + path
def remove(filename):
    global userdir
    fullpath=""
    if not os.path.isabs(filename):
        fullpath=os.path.join(userdir,filename)
    if check(fullpath) and os.path.exists(fullpath):
        os.remove(fullpath)
        return "Удалён файл " + fullpath
    return "Ошибка доступа к директории " + fullpath
def copyclient(filename_from,filename_to):
    global userdir
    if not os.path.isabs(filename_from):
        filename_from=os.path.join(userdir,filename_from)
    if not os.path.isabs(filename_to):
        filename_to=os.path.join(os.getcwd(),filename_to)
    shutil.copyfile(filename_from, filename_to)
    return filename_from + " скопирован в " + filename_to
def copyserver(filename_from, filename_to):
    global userdir
    if not os.path.isabs(filename_from):
        filename_from=os.path.join(os.getcwd(),filename_from)
    if not os.path.isabs(filename_to):
        filename_to=os.path.join(userdir,filename_to)
    shutil.copyfile(filename_from, filename_to)
    return filename_from + " скопирован в " + filename_to
def process(req):
    global userdir
    res= str()
    if req == "show":
        res = show()
    elif req == "ls":
        res = ls(userdir)
    elif req.split()[0]=="send":
        res = sm(req.split()[1])
    elif req.split()[0]=="mkdir":
        res = mkdir(req.split()[1])
    elif req.split()[0]=="rmdir":
        res = rmdir(req.split()[1])
    elif req.split()[0]=="remove":
        res = remove(req.split()[1])
    elif req.split()[0]=="copyclient":
        res = copyclient(req.split()[1],req.split()[2])
    elif req.split()[0]=="copyserv":
        res = copyserver(req.split()[1],req.split()[2])
    elif req.split()[0]=="login":
        userdir=os.path.join(os.getcwd(), req.split()[1])
        current_user=req.split()[1]
        res = "Пользователь {} вошёл в систему ".format(req.split()[1])
    elif req=="exit":
        return "Выход"
    else:
        res="bad request"
    return res
def log(message,file):
    if os.path.exists(os.path.join(os.getcwd(),file)):
        mod="a"
    else:
        mod="w+"
    with open(file,mod) as f:
        f.write(str(datetime.now()) + ": "+ message+"\n")
userdir = os.path.join(os.getcwd(), "docs") #директория по умолчанию
current_user=""
sock = socket.socket()
port = change(int(input("Введите номер порта ")),sock)
sock.listen()
print("Прослушиваем порт ", port)
while True:
    conn, addr = sock.accept()
    request = conn.recv(1024).decode()
    print(request)
    response = process(request)
    conn.send(response.encode())
    log(response,"log.txt")
conn.close()
