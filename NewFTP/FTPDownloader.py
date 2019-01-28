from ftplib import FTP,error_perm
import time
from os import _exit,stat,utime,popen,system
from os.path import isfile,dirname,abspath,splitext
from tqdm import tqdm
try:
    from . import messager
    from .ftp_parser import ENCODING, SILENT
except ImportError:
    import messager
    from ftp_parser import ENCODING, SILENT

ftp = FTP()
ftp.encoding = ENCODING
PRINTING=False
ASK_FILE = '''检测到本地文件{0}，
是否覆盖？

Local file already exist.
Copy any way?
'''
STREAMS = ('.mp4','.mp3','.flv','.avi','.wmv','.rmvb')
class FileTracker():
    def __init__(self,filename,filesize=None):
        self.file=open(filename,'wb')
        self.open_it=None
        if splitext(filename)[1].lower() in STREAMS:
            popen('explorer "%s"'%filename)
            self.open_it=False
        self.filesize=filesize
        self.pbar=tqdm(total=filesize,unit='B',unit_scale=True,ncols=60,
            bar_format='{l_bar}{n_fmt}/{total_fmt}|{rate_fmt}{bar}{remaining}')
    def write(self,buff):
        self.pbar.update(len(buff))
        self.file.write(buff)
    def close(self):
        self.file.close()
        return self.open_it

def init(server_info,user,password):
    global USER,PASSWORD,HOST,PORT
    USER,PASSWORD=user,password
    HOST,PORT=server_info
    ftp.connect(HOST,PORT)
    ftp.login(user,password)

def file_conflict(time,size):
    from win32api import MessageBox
    import win32con

    def compare(a,b):
        if a == b:return 0
        elif a > b:return 1
        else:return -1

    status = (compare(*time),compare(*size))
    if 1 in status:
        time_description = {1:'较新',-1:'较旧'}
        size_description = {1:'较大',-1:'较小'}
        description = time_description.get(status[0],'')+\
                      size_description.get(status[1],'')
        result = MessageBox(win32con.NULL,ASK_FILE.format(description),\
                            '文件冲突 (File Conflict)',\
                            win32con.MB_YESNO|win32con.MB_ICONQUESTION|\
                            win32con.MB_TOPMOST)
        # Yes:6, No:7
        return 7-result
    elif status == (0,0):
        return 0
    else:
        return 1

def just_download(directory,filename,dest,ftp_mtime,ftp_filesize):
    if PRINTING == True:
        system('mode 100,7')
        system('color f2')
        system('title A simple downloader')
        print('This is a simple FTP downloader')
        print()
        print('File to download:',directory+filename)
        print('Local file name:',dest)
        print()
        local_file=FileTracker(dest,ftp_filesize)
    else:
        local_file=open(dest,'wb')
    ftp.retrbinary('RETR %s'%filename,local_file.write)
    open_flag=local_file.close()
    utime(dest,(ftp_mtime,ftp_mtime))
    if open_flag is None:
        popen('explorer "%s"'%dest)

def download(directory,filename,dest):
    ftp.cwd(directory)
    try:
        L=ftp.sendcmd('MDTM %s'%filename)
    except error_perm:
        filename=filename.replace(' ','_')
        L=ftp.sendcmd('MDTM %s'%filename)
    dir_t=L[4:8]+'-'+L[8:10]+'-'+L[10:12]+' '+L[12:14]+':'+L[14:16]+':'+L[16:18]
    timeArray = time.strptime(dir_t, "%Y-%m-%d %H:%M:%S")
    ftp_mtime = int(time.mktime(timeArray))
    ftp_filesize=ftp.size(filename)
    if isfile(dest):
        local_file=stat(dest)
        result = file_conflict((local_file.st_mtime,ftp_mtime),
                               (local_file.st_size,ftp_filesize))
        if result == 0:
            popen('explorer "%s"'%dest)
            ftp.close()
            _exit(0)
    if ftp_filesize < SILENT:
        just_download(directory,filename,dest,ftp_mtime,ftp_filesize)
    else:
        downloader = dirname(abspath(__file__))+'\\FTPDownloader.py'
        cmd='python %s %s %d %s %s "%s" "%s" "%s" %d %d'\
             %(downloader,HOST,PORT,USER,PASSWORD,directory,filename,dest,ftp_mtime,ftp_filesize)
        # if you use -m NewFTP.FTPDownloader, python can't recognize the package
        #cmd='python -m NewFTP.FTPDownloader %s %s "%s" "%s" "%s" %d %d & pause'\
        #     %(USER,PASSWORD,directory,filename,dest,ftp_mtime,ftp_filesize)
        system(cmd)
    ftp.close()

@messager.log_it(file = 'log_download.txt')
def main(host,port,user,password,directory,filename,dest,ftp_mtime,ftp_filesize):
    global PRINTING
    from sys import argv

    PRINTING=True
    init((host,int(port)),user,password)
    ftp.cwd(directory)
    just_download(directory,filename,dest,int(ftp_mtime),int(ftp_filesize))
    ftp.close()
    time.sleep(0.5)

if __name__ == '__main__':
    from sys import argv
    print(argv)
    main(*argv[1:10])
