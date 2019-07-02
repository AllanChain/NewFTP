def get_host_port(server):
    if ':' in server:
        host, port = server.split(':')
        return host, int(port)
    else:
        return server, 21

with open('config.py', encoding='utf-8') as config:
    exec(config.read())
