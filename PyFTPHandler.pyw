import sys
from win32com.shell.shell import SHFileOperation
from win32com.shell import shellcon
from win32gui import FindWindowEx, GetWindowText
from os import popen,makedirs
from re import match


LOCAL_PREFIX='D:\\Desktop\\'
rules={'zjx/303/(.*)':'哈哈哈',
        'zjp/(.*)':'地理',
        'zjx/(.*)':'化学',
        'zm/(.*)': '语文',
        'cjun/(.*)': '数学',
        'xmh/(.*)': '英语\\课件',
        'zxs/(.*)': '物理',
        'ysh/(.*)': '地理',
        'czw/(.*)': '英语'}
file=sys.argv[1]
def get_explorer_path():
    hwnd = 0
    children = ('CabinetWClass','WorkerW','ReBarWindow32','Address Band Root',
                'msctls_progress32','Breadcrumb Parent','ToolbarWindow32')
    for child_class in children:
        hwnd = FindWindowEx(hwnd,0,child_class,None)
    return GetWindowText(hwnd)

def get_local_path(ftp_path,file):
    p1=r'地址: ftp://(.*):.*\@6\.163\.193\.243/(.*)'
    s_path='/'.join(match(p1,ftp_path).groups())
    p2=r'.*\\(.*)\[.*\](.*)'
    print(p2,file)
    file_name=''.join(match(p2,file).groups())
    local_path=LOCAL_PREFIX
    for k, v in rules.items():
        result=match(k,s_path)
        if not result is None:
            r=result.groups()
            match_path=parse_CH(r[-1]) if len(r)>0 else ''
            print(match_path)
            local_path+=v+'\\'+match_path
    local_path=local_path.replace('/','\\')
    print(local_path,type(local_path))
    makedirs(local_path,exist_ok=True)
    return local_path+file_name

def parse_CH(s):
    l=len(s)
    i=0
    r=''
    while i<l:
        if s[i] == '%':
            hexnum=s[i+1:i+3]+s[i+4:i+6]
            print(hexnum)
            r+=bytes.fromhex(hexnum).decode('gbk')
            i+=6
        else:
            r+=s[i]
            i+=1
    return r

def log_and_exit(message = None):
    from time import ctime
    from traceback import print_exc
    from win32api import MessageBox
    import win32con
    from os import _exit
    if not message is None:
        MessageBox(win32con.NULL, message, "Warning", win32con.MB_ICONEXCLAMATION)
    with open('FTPlog.txt','a') as f:
        f.write('\n'+'-'*20+ctime()+'-'*20+'\n')
        print_exc(file=f)
    print_exc()
    _exit(1)
    
def main():
    dest=get_local_path(get_explorer_path(),file)
    print(dest)
    SHFileOperation((0,shellcon.FO_MOVE, file, dest,
                     shellcon.FOF_ALLOWUNDO,None,None))
    popen('attrib -R '+dest).read()
    popen(dest)

if __name__=='__main__':
    try:
        main()
    except Exception:
        log_and_exit()



