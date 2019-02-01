import win32con
from win32gui import FindWindow, PostMessage, SetForegroundWindow
from os import _exit


def find():
    hwnd = FindWindow(None, 'oh-my-ftp')
    if hwnd:
        PostMessage(hwnd, win32con.WM_LBUTTONDOWN, 0, (1 << 16)+1)
        PostMessage(hwnd, win32con.WM_LBUTTONUP, 0, (1 << 16)+1)
        try:
            SetForegroundWindow(hwnd)
        except:
            # if current window lost focus
            # (mainly because the user hit FTP.lnk for 3+ times to quick)
            # do nothing
            pass
        _exit(0)
    return


find()
