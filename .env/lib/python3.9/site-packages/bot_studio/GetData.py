import socket
import string
import json
import random
import requests
import json
import webbrowser
import time
def getipaddress():
    hostname = socket.gethostname()
    ipaddress = socket.gethostbyname(hostname)
    ipaddress=ipaddress.replace('.','-')
    return ipaddress
def gettheuserid():
    dta={}
    try:
        userid=getipaddress()
    except:
        userid="unknown"
    return userid
def check_login():
    try:
        headers = {'Content-type': 'application/json'}
        res=requests.post(url = "http://127.0.0.1:5000/check_login", data = json.dumps({}), headers=headers)
        res=json.loads(res.text)
        status=res["status"]
    except:
        status=False
    return status
def open_global_browser():
    try:
        headers = {'Content-type': 'application/json'}
        res=requests.post(url = "http://127.0.0.1:5000/open_global_browser", data = json.dumps({}), headers=headers)
    except:
        pass
def wait_till_server_started():
    while(True):
        try:
            res=requests.get(url = "http://127.0.0.1:5000/exeruning")
            res=json.loads(res.text)
            status=res["status"]
            if(status=="DataKund"):
                break
        except:
            pass
def check_login_recursive():
    wait_till_server_started()
    status=check_login()
    if(status==False):
        webbrowser.open('https://datakund.com/account/login', new=2)
        print("Please login in browser first to continue.....")
    else:
        open_global_browser()
        return 0
    while(True):
        status=check_login()
        if(status==True):
            break
        time.sleep(2)
    open_global_browser()
    print("Logged in successfully..")