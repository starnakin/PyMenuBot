import subprocess
import os
import inspect
from .GetData import gettheuserid,check_login_recursive
from threading import Thread
folder=inspect.getfile(gettheuserid).split("site-packages")[0]
folder=folder+"site-packages\\bot_studio\\"
def start_studio():
    try:
        folderr=folder+"DataKund.exe"
        subprocess.run([folderr, "start"])
        #os.system(folder+"DataKund.exe start")
    except Exception as e:
        print("Exception is",e)
def main():
    Thread(target = start_studio).start()
    check_login_recursive()