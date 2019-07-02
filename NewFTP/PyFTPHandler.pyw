import sys
from os import makedirs
from re import match
from yaml import load_all
from win32gui import FindWindowEx, GetWindowText
from . import FTPDownloader
from . import messager
from .ftp_parser import DEFAULT_PASS, get_host_port


def load_setting():
    with open('download_config.yaml', 'r', encoding='utf-8') as f:
        specials, setting = load_all(f)
    with open('gui_config.yaml', 'r', encoding='utf-8') as f:
        users = list(load_all(f))[0]
    d = [(k, v) for k, v in specials.items()]
    for k, v in users.items():
        if v.isalpha():
            d.append((v+r'/(.*)', k))
    return setting['LOCAL_PREFIX'], d


def get_explorer_path():
    hwnd = 0
    children = ('CabinetWClass', 'WorkerW', 'ReBarWindow32', 'Address Band Root',
                'msctls_progress32', 'Breadcrumb Parent', 'ToolbarWindow32')
    for child_class in children:
        hwnd = FindWindowEx(hwnd, 0, child_class, None)
    return GetWindowText(hwnd)


def get_ftp_info(ftp_path):
    server = match('地址: ftp://.*\@(.*?)/', ftp_path).group(1)
    server_re = server.replace('.', r'\.').replace(':', r'\:')
    try:
        p1 = r'地址: ftp://(.*):(.*)\@%s(.*)' % server_re
        ftp_info = match(p1, ftp_path).groups()
    except:
        p1 = r'地址: ftp://(.*)\@%s(.*)' % server_re
        ftp_info = match(p1, ftp_path).groups()
        ftp_info = (ftp_info[0], DEFAULT_PASS, ftp_info[1])
# if ftp_info[2]=='':
# ftp_info=ftp_info[0:2]+('.',)
    s_path = ftp_info[0]+ftp_info[2]
    # ftp_info (user,password,dir)
    ftp_info = ftp_info[0:2]+(parse_CH(ftp_info[2]),)
    host, port = get_host_port(server)
    return ftp_info, (host, port), s_path


def get_local_path(ftp_path, file):
    ftp_info, server_info, s_path = get_ftp_info(ftp_path)
    p2 = r'.*\\(.*)\[.*\](.*)'
    print(p2, file)
    file_name = ''.join(match(p2, file).groups())
    file_name = file_name.replace('_', ' ')
    ftp_info += (file_name,)
    # ftp_info (user,password,dir,filename)
    local_path, rules = load_setting()
    for k, v in rules:
        result = match(k, s_path+file_name)
        if not result is None:
            try:
                match_path = parse_CH(result.group(1))
                local_path += v+'\\'+match_path
                break
            except Exception:
                local_path += v
    local_path = local_path.replace('/', '\\').replace('\\\\', '\\')
    print(local_path, type(local_path))
    makedirs(split(local_path)[0], exist_ok=True)
    return local_path, ftp_info, server_info


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
    dest, ftp_info, server_info = get_local_path(get_explorer_path(), file)
    FTPDownloader.init(server_info, *ftp_info[0:2])
    FTPDownloader.download(*ftp_info[2:], dest=dest)


if __name__ == '__main__':
    main()
