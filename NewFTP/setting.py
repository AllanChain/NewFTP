def get_host_port(server):
    if ':' in server:
        return server.split(':')
    else:
        return server, 21

with open('config.py', encoding='utf-8') as config:
    exec(config.read())
