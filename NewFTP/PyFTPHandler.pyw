import sys
from os import makedirs
from os.path import split
from re import match
from collections import namedtuple

from . import FTPDownloader, messager
from .setting import DEFAULT_PASS, get_host_port


def load_setting():
    from .setting import specials, LOCAL_PREFIX, USERS
    d = [(k, v) for k, v in specials.items()]
    for k, v in USERS.items():
        if v.isalpha():
            d.append((v+r'/(.*)', k))
    return LOCAL_PREFIX, d


def get_local_path(ftp_path):
    ftp_path = parse_CH(ftp_path)
    ftp_info = list(match('ftp://(.*):(.*)@(.*?)((/.*){0,1}/(.*?))$',
                          ftp_path).groups())
    # ftp_info 
    if ftp_info[4] is None:
        ftp_info[4] = '/'
    Info = namedtuple('Info', ['user', 'password', 'server', 'path', 'dir', 'file_name'])
    ftp_info = Info(*ftp_info)
    s_path = ftp_info.user + ftp_info.path
    host, port = get_host_port(ftp_info.server)
    local_path, rules = load_setting()
    for k, v in rules:
        result = match(k, s_path)
        if not result is None:
            try:
                match_path = result.group(1)
                local_path += v+'\\'+match_path
                break
            except Exception:
                local_path += v + ftp_info.file_name
    else:
        local_path += ftp_info.file_name
    local_path = local_path.replace('/', '\\').replace('\\\\', '\\')
    print(local_path, type(local_path))
    makedirs(split(local_path)[0], exist_ok=True)
    return local_path, ftp_info, (host, port)


def parse_CH(s):
    l = len(s)
    i = 0
    r = ''
    while i < l:
        if s[i] == '%':
            hexnum = s[i+1:i+3]
            while s[i+3] == '%':
                i += 3
                hexnum += s[i+1:i+3]
            i += 3
            r += bytes.fromhex(hexnum).decode('gbk')
        else:
            r += s[i]
            i += 1
    return r


@messager.log_it(file='log_handler.txt')
def main(file=None):
    if file is None:
        file = sys.argv[1]
    dest, ftp_info, server_info = get_local_path(file)
    # messager.warn(dest)
    FTPDownloader.init(server_info, ftp_info.user, ftp_info.password)
    FTPDownloader.download(ftp_info.dir, ftp_info.file_name, dest=dest)


if __name__ == '__main__':
    main()
