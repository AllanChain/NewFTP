import sys
from win32gui import FindWindowEx, GetWindowText
from os import popen,makedirs,stat,_exit,chdir
from os.path import isfile
from re import match
from . import FTPDownloader
from . import messager

LOCAL_PREFIX='D:\\Desktop\\'
chdir(r'D:\Desktop\Scripts\TGScripts\NewFTP\NewFTP')
rules={'zjx/303/(.*)':'哈哈哈',
        'zjp/(.*)':'地理',
        'zjx/(.*)':'化学',
        'zm/(.*)': '语文',
        'cjun/(.*)': '数学',
        'xmh/(.*)': '英语\\课件',
        'zxs/(.*)': '物理',
        'ysh/(.*)': '地理',
        'czw/(.*)': '英语'}

##notify=lambda m: MessageBox(0, str(m), "Warning", 48)
def get_explorer_path():
    hwnd = 0
    children = ('CabinetWClass','WorkerW','ReBarWindow32','Address Band Root',
                'msctls_progress32','Breadcrumb Parent','ToolbarWindow32')
    for child_class in children:
        hwnd = FindWindowEx(hwnd,0,child_class,None)
    return GetWindowText(hwnd)

def get_local_path(ftp_path,file):
    p1=r'地址: ftp://(.*):(.*)\@6\.163\.193\.243(.*)'
    ftp_info=match(p1,ftp_path).groups()
##    if ftp_info[2]=='':
##        ftp_info=ftp_info[0:2]+('.',)
    s_path=ftp_info[0]+ftp_info[2]
    ftp_info=ftp_info[0:2]+(parse_CH(ftp_info[2]),)
    p2=r'.*\\(.*)\[.*\](.*)'
    print(p2,file)
    file_name=''.join(match(p2,file).groups())
    file_name=file_name.replace('_',' ')
    ftp_info+=(file_name,)
    #notify(str(ftp_info))
    local_path=LOCAL_PREFIX
    for k, v in rules.items():
        result=match(k,s_path)
        if not result is None:
            try:
                match_path=parse_CH(result.group(1))
                local_path+=v+'\\'+match_path
            except Exception:
                local_path+=v
    local_path=local_path.replace('/','\\')
    print(local_path,type(local_path))
    makedirs(local_path,exist_ok=True)
    return local_path+file_name,ftp_info

def compare_mtime(file,dest):
    ftp_file=stat(file)
    notify(str(ftp_file.st_size)+'\n'+str(ftp_file.st_file_attributes))
    if isfile(dest):
        local_file=stat(dest)
        print(ftp_file,local_file)
        if ftp_file.st_mtime == local_file.st_mtime:
            popen('"%s"'%dest)
            _exit(0)
        if ftp_file.st_mtime >= local_file.st_mtime:
            popen('DEL "%s"'%dest)
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
    if not message is None:
        MessageBox(win32con.NULL, message, "Warning", win32con.MB_ICONEXCLAMATION)
    with open('FTPlog.txt','a') as f:
        f.write('\n'+'-'*20+ctime()+'-'*20+'\n')
        print_exc(file=f)
    print_exc()
    _exit(1)

@messager.log_it
def main(file=None):
    if file is None:
        file=sys.argv[1]
    
    dest,ftp_info=get_local_path(get_explorer_path(),file)
    FTPDownloader.init('6.163.193.243',21,*ftp_info[0:2])
    FTPDownloader.download(*ftp_info[2:],dest=dest)

if __name__=='__main__':
    main()
