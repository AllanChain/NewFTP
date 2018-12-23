from ftplib import FTP
from sys import stdout
import time
from os import _exit,stat,utime,popen,system
from os.path import isfile
from tqdm import tqdm

class FileTracker():
    def __init__(self,filename,filesize=None):
        self.file=open(filename,'wb')
        self.filesize=filesize
        self.current_size=0
        self.pbar=tqdm(total=filesize,unit='B',unit_scale=True,ncols=60,
                       bar_format='{l_bar}{n_fmt}|{rate_fmt}{bar}{remaining}')
    def write(self,buff):
##        self.current_size+=len(buff)
##        ratio=self.current_size/self.filesize
##        percentage=str(int(ratio*100))+'%'
##        bar='#'*int(ratio*40)+'_'*int(40-ratio*40)+'|'
##        size=format_size(self.current_size)
##        stdout.write(' |'.join((percentage,size,bar))+'\r')
##        stdout.flush()
        self.pbar.update(len(buff))
        self.file.write(buff)
    def  close(self):
        self.file.close()

def init(host,port,user,password):
    global USER,PASSWORD
    USER,PASSWORD=user,password
    ftp.connect(host,port)
    ftp.login(user,password)
    ftp.encoding='utf-8'

def just_download(directory,filename,dest,ftp_mtime,ftp_filesize):
    #ftp_mtime,ftp_filesize=compare_mtime(directory,filename,dest)
    
    if PRINTING == True:
        print('File to download:',directory+'/'+filename)
        print('Remote file size:',format_size(ftp_filesize))
        print('Remote file modify time:',ftp_mtime)
        print('Local file name:',dest)
        print()
        local_file=FileTracker(dest,ftp_filesize)
    else:
        local_file=open(dest,'wb')
##    ftp.dir()
    ftp.retrbinary('RETR %s'%filename,local_file.write)
    local_file.close()
    utime(dest,(ftp_mtime,ftp_mtime))
    popen('"%s"'%dest)
    #print(stat(dest))
    #ftp.dir()

def download(directory,filename,dest):
    ftp.cwd(directory)
    L=ftp.sendcmd('MDTM %s'%filename)
    dir_t=L[4:8]+'-'+L[8:10]+'-'+L[10:12]+' '+L[12:14]+':'+L[14:16]+':'+L[16:18]
    timeArray = time.strptime(dir_t, "%Y-%m-%d %H:%M:%S")
    ftp_mtime = int(time.mktime(timeArray))
    if isfile(dest):
        local_file=stat(dest)
        if ftp_mtime == local_file.st_mtime:
            popen('"%s"'%dest)
            _exit(0)
        if ftp_mtime >= local_file.st_mtime:
            popen('DEL "%s"'%dest)
    ftp_filesize=ftp.size(filename)
    if ftp_filesize < SILENT:
        just_download(directory,filename,dest,ftp_mtime,ftp_filesize)
    else:
        cmd='python FTPDownloader.py %s %s %s %s %s %d %d'\
             %(USER,PASSWORD,directory,filename,dest,ftp_mtime,ftp_filesize)
        system(cmd)
def format_size(size):
    for i in ('B','K','M','G'):
        if size>900:
            size/=1024
        else:
            return '{:.1f}'.format(size)+i
##download('新文件夹','新建 文本文档.txt')

ftp = FTP()
USER=''
PASSWORD=''
SILENT=1024*800
if __name__ == '__main__':
    from sys import argv

    user,password,directory,filename,dest,ftp_mtime,ftp_filesize=argv[1:8]
    PRINTING=True
    system('mode 100,10')
    system('color f2')
    system('title A simple downloader')
    print('This is a simple FTP downloader')
    print()
    init('192.168.123.99',2121,user,password)
    ftp.cwd(directory)
    just_download(directory,filename,dest,int(ftp_mtime),int(ftp_filesize))
    time.sleep(0.5)
else:
    PRINTING=False
    ##ftp.dir()
