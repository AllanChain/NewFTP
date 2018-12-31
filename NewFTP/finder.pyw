import win32con
from win32gui import FindWindow, PostMessage, SetForegroundWindow
from os import _exit
def find():
    hwnd = FindWindow(None,'oh-my-ftp')
    if hwnd:
        PostMessage(hwnd, win32con.WM_LBUTTONDOWN, 0,(1<<16)+1)
        PostMessage(hwnd, win32con.WM_LBUTTONUP, 0,(1<<16)+1)
        SetForegroundWindow(hwnd)
        _exit(0)
    return
find()
