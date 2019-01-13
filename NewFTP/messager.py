from win32api import MessageBox
import win32con
from os import _exit


warn = lambda m: MessageBox(0, str(m), "Warning",\
                            win32con.MB_ICONEXCLAMATION|win32con.MB_TOPMOST)


class Warner:

    def __init__(self,file,message):
        self.message = message
        self.file = file
    def write(self,message):
        self.message += message
        return
    def __del__(self):
        from time import ctime

        warn(self.message)
        with open(self.file,'a') as f:
            f.write('\n'+'-'*20+ctime()+'-'*20+'\n')
            f.write(self.message)
        print(self.message)

def log_and_exit(file = 'log.txt', message = '', to_exit = True):
    from traceback import print_exc

    print_exc(file=Warner(file, message))
    if to_exit == True:
        _exit(1)

def log_it(file = 'log.txt', to_exit = True):
    def dec(f):
        def func(*args, **kargs):
            try:
                f(*args, **kargs)
            except:
                log_and_exit(file = file, to_exit = to_exit)
        return func
    return dec


##@log_it
##def h():
##    return 0/0
##h()
