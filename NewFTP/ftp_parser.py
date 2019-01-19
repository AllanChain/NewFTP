import yaml

def parse_ellipsis(comp_server):
    host,port = comp_server.split(':')
    port = int(port)
    if port == 21:
        server = host
    else:
        server = comp_server
    return server, host, port
def get_host_port(sever):
    if ':' in sever:
        return server.split(':')
    else:
        return sever,21
with open('ftp_server.txt','r',encoding='utf-8') as f:
    consts = yaml.load(f)
COMPLETE_SERVER = consts['server']
ENCODING = consts['encoding']
DEFAULT_PASS = str(consts['default_password'])
SERVER, HOST, PORT = parse_ellipsis(COMPLETE_SERVER)
