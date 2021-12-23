import socket
import os
import datetime
import bs4, requests
global image,text,application, statuses
text=[".txt",".css",".html"]
image=[".png",".jpeg"]
application=[".js"]
statuses={200: "OK", 403:"Forbidden",404: "Not Found"}
def file_format(file):
    return os.path.splitext(file)[1]
def zapis(log_file,file,code):
    global statuses
    date=datetime.datetime.now()
    ip=get_ip()
    if os.path.exists(log_file):
        mod="a"
    else:
        mod="w+"
    with open(log_file,mod) as f:
        f.write("Date: {}\nIP: {}\nFile: {}\nCode: {} {}\n\n".format(date,ip,file,code,statuses[code]))
def text_(file):
    global text
    if file_format(file) in text:
        return True
    return False
def per(file,content,code = 200):
    global statuses
    http="HTTP/1.1"
    server="Self-Made Server v0.0.1"
    date = datetime.datetime.now()
    contenttype = types(file_format(file))
    contentlength = len(content)
    connection="close"
    response="{} {} {}\nDate: {}\nServer: {}\nContent-type: {}\nContent-length: {}\nConnection: {}\n\n{}".format(http,code,
                                                                                                                 statuses[code],date,server,contenttype,
                                                                                                                 contentlength,connection,content)
    return response
def picture(file):
    global image
    if file_format(file) in image:
        return True
    return False
def format(file,formats=[".jpeg",".txt",".png",".css",".html", ".js"]):
    if file_format(file) in formats:
        return True
    return False
def show_picture(file):
    with open(file,"rb") as f:
        content=f.read()
        return content
def types(extension):
    global text,image,application
    c = str()
    if extension in text:
        c="text/"
    elif extension in image:
        c="image/"
    elif extension in application:
        c="application/"
    if c is not None:
        return c+extension[1:]
    return None
def set_server(settings_file,sep=";"):
    settings = list()
    with open(settings_file) as f:
        settings = f.read().split(sep)
        return (int(settings[0]),int(settings[1]),int(settings[2]),settings[3])
def get_ip():
    s = requests.get('https://2ip.ua/ru/')
    b = bs4.BeautifulSoup(s.text, "html.parser")
    a = b.select(" .ipblockgradient .ip")[0].getText()
    return a.strip()
def readtext(file):
    content=str()
    with open(file,"r",encoding="utf-8") as f:
        for line in f:
            content+=line
    return content
def adressform(file,path):
    if path != "":
        file = os.path.join(path,file)
    if file == "/":
        file="index.html"
    if file[0] == "/":
        file = file[1:]
    return file
sock = socket.socket()
port,backup_port,bufsize,path = set_server("settings.txt")
try:
    sock.bind(('', port))
    print("Using port {}".format(port))
except OSError:
    sock.bind(('', backup_port))
    print("Using port {}".format(backup_port))
sock.listen(5)
while True:
    conn, addr = sock.accept()
    print("Connected", addr)
    data = conn.recv(bufsize)
    msg = data.decode()
    content=""
    code = int()
    print(msg)
    file = msg.split("\n")[0].split(" ")[1] 
    file = adressform(file,path)
    if not format(file):
        code = 403
        file="403.html"
    elif not os.path.exists(file):
        code = 404
        file="404.html"
    else:
        code = 200
    if picture(file):
        content=show_picture(file)
        conn.send(content)
    elif text_(file):
        content=readtext(file)
        resp = per(file,content,code)
        print(resp)
        conn.send(resp.encode(encoding="utf-8"))
    zapis("log.txt",file,code)
conn.close()