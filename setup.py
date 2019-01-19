import setuptools
from setuptools.command.install import install

def short_target(filename,dest,arg):
    import os, sys
    import pythoncom
    from win32com.shell import shell, shellcon


    desktop_path = shell.SHGetFolderPath (0, shellcon.CSIDL_DESKTOP, 0, 0)
    shortcut_path = os.path.join (desktop_path, filename)
    if not os.path.exists(shortcut_path):
        shortcut = pythoncom.CoCreateInstance (
            shell.CLSID_ShellLink,
            None,
            pythoncom.CLSCTX_INPROC_SERVER,
            shell.IID_IShellLink
        )
        with open (shortcut_path,'w'):
            pass
        persist_file = shortcut.QueryInterface (pythoncom.IID_IPersistFile)
        persist_file.Load (shortcut_path)
        shortcut.SetPath(dest)
        shortcut.SetArguments(arg)
        shortcut.SetHotkey(114)
        persist_file.Save (shortcut_path, 0)

def register(command):
    import winreg
    key=winreg.OpenKey(winreg.HKEY_CLASSES_ROOT,
                           r'ftp\shell\open\command',
                           0,winreg.KEY_WRITE)
    winreg.SetValueEx(key, "", 0, winreg.REG_SZ, command)
    key=winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                       r'Software\Microsoft\Windows\Shell\Associations\UrlAssociations\ftp\UserChoice',
                       0,winreg.KEY_WRITE)
    winreg.SetValueEx(key, "Progid", 0, winreg.REG_SZ, "")

class CustomInstall(install):
    def run(self):
        from shutil import copytree
        from os.path import dirname, abspath, expanduser, isdir, split
        from sys import executable
        install.run(self)
        if not isdir(expanduser('~/.NewFTP')):
            src = dirname(abspath(__file__))+'\\NewFTP\\data'
            copytree(src, expanduser('~/.NewFTP'))
        short_target("FTP.lnk",'"%s\\pythonw.exe"'%split(executable)[0],
                     '-m NewFTP.NewFTP')
        register('"{0}\\pythonw.exe" -m NewFTP.PyFTPHandler "\%1"'\
                 .format(split(executable)[0]))

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="NewFTP",
    version="0.0.2a0",
    author="AllanChain",
    author_email="txsmlf@gmail.com",
    description="A GUI program to login the FTP system and a background program to manage FTP file downloading",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AllanChain/NewFTP",
    packages=setuptools.find_packages(),
    package_data={
        '':['*.pyw','data/*','data/Styles/*','data/Styles/Img/*']},
    install_requires=["PyYAML","python-box","pygame","tqdm","pywin32"],
    cmdclass={'install': CustomInstall},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: Microsoft :: Windows :: Windows 7",
        "Development Status :: 3 - Alpha",
    ],
)
