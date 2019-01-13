from os import chdir
from os.path import expanduser
try:
    chdir(expanduser('~/.NewFTP'))
except FileNotFoundError:
    from shutil import copytree
    from os.path import dirname, abspath

    src = dirname(abspath(__file__))+'\\data'
    copytree(src, expanduser('~/.NewFTP'))
    chdir(expanduser('~/.NewFTP'))
