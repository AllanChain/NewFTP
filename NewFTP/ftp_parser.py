import yaml


def get_host_port(server):
    if ':' in server:
        return server.split(':')
    else:
        return server, 21


with open('ftp_server.yaml', 'r', encoding='utf-8') as f:
    consts = yaml.load(f)
SERVER = COMPLETE_SERVER = consts['server']
ENCODING = consts['encoding']
DEFAULT_PASS = str(consts['default_password'])
SILENT = consts['silent']
