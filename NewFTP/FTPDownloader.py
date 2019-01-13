from ftplib import FTP,error_perm
from sys import stdout
import time
from os import _exit,stat,utime,popen,system
from os.path import isfile,dirname,abspath,splitext
from tqdm import tqdm
import yaml
try:
    from . import messager
except ImportError:
    import messager

ftp = FTP()
USER=''
PASSWORD=''
SILENT=1024*800
PRINTING=False
with open('download_setting.yaml','r',encoding='utf-8') as f:
    rules,SERVER=yaml.load_all(f)

class FileTracker():
    def __init__(self,filename,filesize=None):
        self.file=open(filename,'wb')
        self.open_it=None
        if splitext(filename)[1] in ('.mp4','.mp3'):
            popen('explorer "%s"'%filename)
            self.open_it=False
        self.filesize=filesize
        self.pbar=tqdm(total=filesize,unit='B',unit_scale=True,ncols=60,
            bar_format='{l_bar}{n_fmt}/{total_fmt}|{rate_fmt}{bar}{remaining}')
    def write(self,buff):
        self.pbar.update(len(buff))
        self.file.write(buff)
    def  close(self):
        self.file.close()
        return self.open_it

def init(user,password):
    global USER,PASSWORD
    USER,PASSWORD=user,password
    ftp.connect(SERVER['HOST'],SERVER['PORT'])
    ftp.login(user,password)
    ftp.encoding='gbk'

def just_download(directory,filename,dest,ftp_mtime,ftp_filesize):
    if PRINTING == True:
        system('mode 100,7')
        system('color f2')
        system('title A simple downloader')
        print('This is a simple FTP downloader')
        print()
        print('File to download:',directory+'/'+filename)
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
    if isfile(dest):
        local_file=stat(dest)
        if ftp_mtime == local_file.st_mtime:
            popen('explorer "%s"'%dest)
            _exit(0)
        if ftp_mtime >= local_file.st_mtime:
            popen('DEL "%s"'%dest)
    ftp_filesize=ftp.size(filename)
    if ftp_filesize < SILENT:
        just_download(directory,filename,dest,ftp_mtime,ftp_filesize)
    else:
        downloader = dirname(abspath(__file__))+'\\FTPDownloader.py'
        cmd='python %s %s %s "%s" "%s" "%s" %d %d'\
             %(downloader,USER,PASSWORD,directory,filename,dest,ftp_mtime,ftp_filesize)
        # if you use -m NewFTP.FTPDownloader, python can't recognize the package
        #cmd='python -m NewFTP.FTPDownloader %s %s "%s" "%s" "%s" %d %d & pause'\
        #     %(USER,PASSWORD,directory,filename,dest,ftp_mtime,ftp_filesize)
        #messager.warn(cmd)
        system(cmd)


@messager.log_it(file = 'log_download.txt')
def main(user,password,directory,filename,dest,ftp_mtime,ftp_filesize):
    global PRINTING
    from sys import argv

    PRINTING=True

    init(user,password)
    ftp.cwd(directory)
    just_download(directory,filename,dest,int(ftp_mtime),int(ftp_filesize))
    time.sleep(0.5)
##messager.warn(main)
if __name__ == '__main__':
    from sys import argv
    main(*argv[1:8])
