# NewFTP
### General
A pygame powered GUI program to login the FTP system.
It's open source, unlike any other distribution in TG.
Feel free to edit its looking.
### Dependencies
- pygame
- pywin32
- PyYAML
- python-box
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
Not onlyvdo we offer `config.yaml` and `Styles/*.yaml` to edit its behavior and looking,  those who also love python can also edit the source file and PR via github.

### Quick Start
1. install python 3.X. (check `add python to PATH`)
2. install all the dependencies listed above via `pip install`.
3. clone this repo to any where you like
4. create a link `pythonw D:\path\to\repo\NewFTP.pyw` and assign a hot key. (conventionally `<F3>`)
5.  Double click the link, and after two seconds or so, a blue window will be there on the left side of the screen, displaying the default teachers and blank one. Click one to log in and show the content via explorer. And the window will be minimized on the left sid but somewhat upper.
6.  Click the mini window or double click the link you created to maximize the window.
7.  Dive into the directory `NewFTP`, open `config.yaml` with your favorite text editor (or simply notepad) and edit the first chunk from `---` to `...`. Especially note that the colon must be followed by space.
8.  Save and close it. Right click at the mini window to quit, and double click the link to restart. If no message box or nothing happened, you're supposed to have an FTP shortcut just for you. If something bad DOES happen, check your `config.yaml` and `log.txt`.

### Controlling
#### Touch control
- tap the square block to login
- slide up and down to turn the pages
- slide towards left to minimize
- tap the minimized floating window to maximize
- drag the minimized window to put it any where
- right click to quit
#### Remote control
- press F3 to start (depend on the hotkey you set)
- press the number corresponding to the block to login
- PgUp and PgDown to turn the pages
- press F3 again to gain focus or show window
- Enter to maximize
- left arrow to minimize
- press Esc, namely Back to quit
#### Keyboard and mouse
- I think you know it 

### Advanced Usage
All the examples here are included in the default `config.yaml`.

- Run Command From It
> Replace the user name (e.g. `zxs`) with command you want starting with a dollar sign. (`$`)
- Open local directory from it
> Replace the user name with directory you want, ending with a slash or a back slash.
- Open local file with it
> Replace the user name with file name you want, not ending with a slash or a back slash.
- A teacher with an abnormal combinations
> Edit the second chunk of `config.yaml`. Note combinations made upvwith pure digits shoud be wrapped with quotes.

### Why minimized floating window
As you know, python is a language for the 21st century,
and easy to write, read and mantain. However, it takes ages to start.
To cut down the waiting time, the minimized window is the best option.
### Why pywin32
The smoother, the more win32API should be used. (please do not complain my abusing win32API)
### TO DO
#### Black Magic
- Dragging out the files newly uploaded from main window to the desktop. (this might be quite hard)
- or an IExplorerBrowser application with ICommDlgBrowser to hack open file event. (This may require C++ program)
#### Good-looking Themes
It is obvious that we are using Microsoft Windows7 theme. What if Linux theme or other awesome software, organizations?
#### Advertising
Good things should be shared.
