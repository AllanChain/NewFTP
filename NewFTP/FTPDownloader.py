from ftplib import FTP,error_perm
from sys import stdout
import time
from os import _exit,stat,utime,popen,system
from os.path import isfile,dirname,abspath
from tqdm import tqdm
from . import messager

class FileTracker():
    def __init__(self,filename,filesize=None):
        self.file=open(filename,'wb')
        self.filesize=filesize
        #self.current_size=0
        system('mode 100,7')
        system('color f2')
        system('title A simple downloader')
        print('This is a simple FTP downloader')
        print()
        self.pbar=tqdm(total=filesize,unit='B',unit_scale=True,ncols=60,
                       bar_format='{l_bar}{n_fmt}/{total_fmt}|{rate_fmt}{bar}{remaining}')
    def write(self,buff):
        self.pbar.update(len(buff))
        self.file.write(buff)
    def  close(self):
        self.file.close()

def init(host,port,user,password):
    global USER,PASSWORD
    USER,PASSWORD=user,password
    ftp.connect(host,port)
    ftp.login(user,password)
    ftp.encoding='gbk'

def just_download(directory,filename,dest,ftp_mtime,ftp_filesize):
    if PRINTING == True:
        print('File to download:',directory+'/'+filename)
        print('Local file name:',dest)
        print()
        local_file=FileTracker(dest,ftp_filesize)
    else:
        local_file=open(dest,'wb')
##    ftp.dir()
    ftp.retrbinary('RETR %s'%filename,local_file.write)
    local_file.close()
    utime(dest,(ftp_mtime,ftp_mtime))
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
    just_download(directory,filename,dest,ftp_mtime,ftp_filesize)
    #if ftp_filesize < SILENT:
        #just_download(directory,filename,dest,ftp_mtime,ftp_filesize)
    #else:
        #downloader = dirname(abspath(__file__))+'\\FTPDownloader.py'
        #cmd='python %s %s %s "%s" "%s" "%s" %d %d'\
             #%(downloader,USER,PASSWORD,directory,filename,dest,ftp_mtime,ftp_filesize)
        #cmd = 'python d:\\Desktop\\123.py'
        #messager.warn(cmd)
        #system(cmd)

ftp = FTP()
USER=''
PASSWORD=''
SILENT=1024*800
PRINTING=False

@messager.log_it
def main(user,password,directory,filename,dest,ftp_mtime,ftp_filesize):
    global PRINTING
    from sys import argv

    PRINTING=True

##    init('192.168.123.99',2121,user,password)
    init('6.163.193.243',21,user,password)
    ftp.cwd(directory)
    just_download(directory,filename,dest,int(ftp_mtime),int(ftp_filesize))
    time.sleep(0.5)
##messager.warn(main)
if __name__ == '__main__':
    from sys import argv
    main(*argv[1:8])
