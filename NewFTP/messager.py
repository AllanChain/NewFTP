from win32api import MessageBox
import win32con
from os import _exit

class Warner:
    def __init__(self):
        self.message = ''
    def write(self,message):
        self.message += message
        return
    def __del__(self):
        MessageBox(win32con.NULL, self.message, "Warning", win32con.MB_ICONEXCLAMATION)
def log_and_exit(file = None,message = None):
    from time import ctime
    from traceback import print_exc
    print_exc(file=Warner())
##    if not message is None:
##        MessageBox(win32con.NULL, message, "Warning", win32con.MB_ICONEXCLAMATION)
    with open('log.txt','a') as f:
        f.write('\n'+'-'*20+ctime()+'-'*20+'\n')
        print_exc(file=f)
    print_exc()
    _exit(1)

try:
    0/0
except:
    log_and_exit()
