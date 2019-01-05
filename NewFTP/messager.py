from win32api import MessageBox
import win32con
from os import _exit
from time import ctime
from traceback import print_exc

class Warner:
    
    def __init__(self,file):
        self.message = ''
        self.file = file
    def write(self,message):
        self.message += message
        return
    def __del__(self):
        MessageBox(win32con.NULL, self.message, "Warning",\
                   win32con.MB_ICONEXCLAMATION|win32con.MB_TOPMOST)
        with open(self.file,'a') as f:
            f.write('\n'+'-'*20+ctime()+'-'*20+'\n')
            f.write(self.message)
        print_exc()

def log_and_exit(file = 'log.txt',message = None, to_exit = True):
    if message is None:
        print_exc(file=Warner(file))
    else:
        warn(message)
    if to_exit == True:
        _exit(1)

warn = lambda m: MessageBox(0, str(m), "Warning",\
                            win32con.MB_ICONEXCLAMATION|win32con.MB_TOPMOST)

try:
    0/0
except:
    log_and_exit()
