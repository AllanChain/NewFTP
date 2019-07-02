# NewFTP
### General
A pygame powered GUI program to login the FTP system.
It's open source, unlike any other distribution in TG.
Feel free to edit its looking.

- [NewFTP GUI](#newftp-gui)
- [PyFTPHandler](#pyftphandler)
### Dependencies
- pygame
- pywin32
- PyYAML
- python-box
- tqdm
### Features
#### TOTALLY open source
Licensed under AGPLv3
#### thus TOTALLY free
Only installation fee is charged if you turn to us for help.
#### TOTALLY offline
Perfectly solved the server breaking down problem as former distributions do.
#### Script language
It means once python and some packages are installed, only KBs or a few MBs for brand new features and programs.
#### Changable whenever you want
Not onlyvdo we offer `config.py` and `Styles/*.yaml` to edit its behavior and looking,  those who also love python can also edit the source file and PR via github.

## NewFTP GUI
### Quick Start
1. install python 3.X. (check `add python to PATH`)
> 3.6+ if you want keep dict in order.
2. run `pip install NewFTP`
5. Double click the link (automatically generated when installing), and after two seconds or so, a blue window will be there on the left side of the screen, displaying the default teachers and blank one. Click one to log in and show the content via explorer. And the window will be minimized on the left side but somewhat upper.
6.  Click the mini window or double click the link to maximize the window.
7.  Dive into the directory `~/.NewFTP`, open `config.py` with your favorite text editor (or simply notepad) and edit the `USERS` and `PASSWORDS` dictionary.
7. Edit `SERVER` and `ENCODING` variabale to config your FTP server.
8.  Save and close it. Right click at the mini window to quit, and double click the link to restart. If no message box or nothing happened, you're supposed to have an FTP shortcut just for you. If something bad DOES happen, check your `config.py` and `log_*.txt`.

### Controlling
#### Touch control
- tap the square block to login
- slide up and down to turn the pages
- slide towards left to minimize
- tap the minimized floating window to maximize
- drag the minimized window to put it any where
- right click to quit
#### Remote control
- press `<F3>` to start (depend on the hotkey you set)
- press the number corresponding to the block to login
- `PgUp` and `PgDown` to turn the pages
- press `<F3>` again to gain focus or show window
- Enter to maximize
- left arrow to minimize
- press `<Esc>`, namely Back to quit
#### Keyboard and mouse
- I think you know it

### Advanced Usage
All the examples here are included in the default `config.py`.

- Run Command From It
> Replace the user name (e.g. `zxs`) with command you want starting with a dollar sign. (`$`)
- Open local directory or file from it
> Replace the user name with directory or file you want
- A teacher with an abnormal combinations
> Edit the second chunk of `config.py`.

### Why minimized floating window
As you know, python is a language for the 21st century,
and easy to write, read and mantain. However, it takes ages to start.
To cut down the waiting time, the minimized window is the best option.
### Why pywin32
The smoother, the more win32API should be used. (please do not complain my abusing win32API)

## PyFTPHandler
To take over the FTP file transfer when double click the file.
### Features
- a simple FTPDownloader CLI
- watching while downloading
- regular expression powered file sorting

### Quick Start
- pip install as said above
- In the directory `/.NewFTP`, edit 'config.py' to config your FTP server and your download directory.
> Note: if you wrote
```yaml
'物理': 'zxs'
```
in your 'config.py', the by default, the handler translate it into
```yaml
'zxs/(.*)': '物理'
```
as part of download rules, and there is no need to write it again. But you can override this by writing something like:
```yaml
'zxs/(.*)': '我爱物理'
'zxs/(.*)': ''
```
You could see more example in the default configuration.

- Then, when you double click the file in the explorer ftp window, the handler will automaticly copy the file to the specified directory, and open with default application.

## TO DO
#### Black Magic
- Important Ones
  - Find the better way to register PyFTPHandler.(current implementation is somewhat tricky)
  - Test on the 32 bit Win7, which seems different from the 64 bit ones.
    - if the 32 bit Win7 does not provide password in the address bar, read the config file to get it.
  - ~~Support mixed underscores and spaces in the file name. (Win7 replaced spaces with underscores)~~ **Done with the help of `difflib`**
  - Maintainers please!
- Less Important Ones
  - Add action config of the gui program:
    - HideOnMini
    - MiniDelayOnFocusLoss
    - OnAltF4
    - MiniAfterLogin
  - Support regex match with file name included.
  - Support break points for big file downloading.
  - Trace the opened file, if modified, ask if upload.
  - If local file is newer, ask upload.
  - Add title bar to the gui program to display custom information, such as:
    - CEE days
    - Class Status
  - The `__main__.py` CLI.

#### Good-looking Themes
It is obvious that we are using Microsoft Windows7 theme. What if Linux theme or other awesome software, organizations?
#### Advertising
- Good things should be shared.
- An experienced maintainer is welcomed.
