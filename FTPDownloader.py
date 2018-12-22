from ftplib import FTP
from sys import stdout
import time
from os import _exit,stat,utime,popen
from os.path import isfile


class FileTracker():
    def __init__(self,filename,filesize=None):
        self.file=open(filename,'wb')
        self.filesize=filesize
        self.current_size=0
    def write(self,buff):
        self.current_size+=len(buff)
        ratio=self.current_size/self.filesize
        percentage=str(int(ratio*100))+'%'
        bar='#'*int(ratio*40)
        size=format_size(self.current_size)
        stdout.write(' |'.join((percentage,size,bar))+'\r')
        stdout.flush()
        self.file.write(buff)
    def  __del__(self):
        self.file.close()

def init(host,port,user,password):
    ftp.connect(host,port)
    ftp.login(user,password)
    ftp.encoding='utf-8'

def download(directory,filename,dest):
    ftp.cwd(directory)
    ftp_mtime=compare_mtime(filename,dest)
    local_file=FileTracker(dest,ftp.size(filename))
    ftp.retrbinary('RETR %s'%filename,local_file.write)
    del local_file
    utime(dest,(ftp_mtime,ftp_mtime))
    print(stat(dest))
    #ftp.dir()

def compare_mtime(filename,dest):
    L=ftp.sendcmd('MDTM %s'%filename)
    dir_t=L[4:8]+'-'+L[8:10]+'-'+L[10:12]+' '+L[12:14]+':'+L[14:16]+':'+L[16:18]
    timeArray = time.strptime(dir_t, "%Y-%m-%d %H:%M:%S")
    ftp_mtime = int(time.mktime(timeArray))
    if isfile(dest):
        local_file=stat(dest)
        print(ftp_mtime,local_file)
        if ftp_mtime == local_file.st_mtime:
            popen('"%s"'%dest)
            _exit(0)
        if ftp_mtime >= local_file.st_mtime:
            popen('DEL "%s"'%dest)
    return ftp_mtime
def format_size(size):
    for i in ('B','K','M','G'):
        if size>900:
            size/=1024
        else:
            return '{:.1f}'.format(size)+i
##download('新文件夹','新建 文本文档.txt')

ftp = FTP()
if __name__ == '__main__':
    init('192.168.123.99',2121,'ac','123')
    download('documents','申请表.pdf','123.pdf')
    input()
    ##ftp.dir()

