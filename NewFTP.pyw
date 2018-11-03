import pygame
from pygame.locals import *
from os import popen, environ, _exit
from win32gui import FindWindow, SetWindowPos, PostMessage, GetCursorPos, SetForegroundWindow
import direction
import win32con
import yaml
from dotted_dict import DottedDict

##size = 75
##size2 = 30
##startx, starty = 0, 500

class NameManager:
    def __init__(self,usr,pas_dict,perpage):
        self.acnts=tuple(usr.items())
        self.pas_dict=pas_dict
        self.page = 0
        self.perpage = perpage
        self.maxpage = len(usr)//perpage
        self.total=len(self.acnts)
    def get_acnt(self, i):
        num = self.page*self.perpage+i
        if not 0 <= i <= self.perpage-1:
            return ('','')
        return self.acnts[num] if num<self.total else ('','')
    def get_usr(self,i):
        return self.get_acnt(i)[1]
    def get_name(self, i):
        return self.get_acnt(i)[0]
    def pageturn(self,pg):
        self.page = max(0,min(self.maxpage, self.page+pg))
    def launch(self, num):
        name=self.get_usr(num)
        print(num)
        if '/' in name or '\\' in name:
            popen('start explorer %s'%name)
        else:
            name1 = name+':'+self.pas_dict.get(name,'123')+'@' if name else ''
            print (name1)
            popen('start explorer ftp://%s6.163.193.243'%name1)

def load():
    with open('config.yaml','r') as f:
        usr,pas,sty = yaml.load_all(f)
    with open('styles/' + sty['style'] + '.yaml') as f:
        style = yaml.load(f)
    style = DottedDict(style)
    style.maximum.width = style.maximum.rows*style.maximum.block.width
    style.maximum.height = style.maximum.cols*style.maximum.block.height
    mgr = NameManager(usr,pas,style.maximum.rows*style.maximum.cols-1)
    #print(usr,pas)
    return mgr,style 

def draw_bg(style):
    BGSurf = pygame.surface.Surface((style.maximum.width,style.maximum.height))
    BGSurf.fill(style.maximum.color.background)
    for i in range(style.maximum.rows):
        for j in range(style.maximum.cols):
            pygame.draw.rect(BGSurf,style.maximum.color.border,
                             (i*style.maximum.block.width,
                              j*style.maximum.block.height,
                              style.maximum.block.width,
                              style.maximum.block.height),
                             style.maximum.border)
    BG = pygame.image.load('Styles/'+style.maximum.image.path)
    BG = pygame.transform.scale(BG,(style.maximum.width,style.maximum.height))
    BG.set_alpha(style.maximum.image.alpha)
    BGSurf.blit(BG,(0, 0))
    BGMSurf = pygame.surface.Surface((style.minimum.width,style.minimum.height))
    BGMSurf.fill(style.minimum.color.background)
    pygame.draw.rect(BGMSurf,style.minimum.color.border,(0, 0, style.minimum.width,
                    style.minimum.height), style.minimum.border)
    return BGSurf, BGMSurf
def find():
    hwnd = FindWindow(None,'oh-my-ftp')
    if hwnd:
        pygame.quit()
        PostMessage(hwnd, win32con.WM_LBUTTONDOWN, 0,(1<<16)+1)
        PostMessage(hwnd, win32con.WM_LBUTTONUP, 0,(1<<16)+1)
        _exit(0)
        return
def main():
    global MINI
    find()
    mgr,style = load()
    environ['SDL_VIDEO_WINDOW_POS']='%d,%d'%(style.maximum.pos.x,style.maximum.pos.y)
    DIS = pygame.display.set_mode((style.maximum.width,style.maximum.height), NOFRAME)
    MINI = False
    MOVING = False
    find()
    pygame.display.set_caption('oh-my-ftp')
    hwnd = FindWindow(None,'oh-my-ftp')
    BGSurf,BGMSurf = draw_bg(style)
    pygame.font.init()
    FontObj = pygame.font.SysFont(style.font.font, style.font.size)
    def draw_text():
        DIS.blit(BGSurf,(0, 0))
        for n in range(mgr.perpage):
            i, j = n//style.maximum.rows, n%style.maximum.rows
            name = mgr.get_name(n)
            txt = FontObj.render(name, True,style.font.color)
            rect = txt.get_rect()
            rect.center=((j+0.5)*style.maximum.block.width,
                         (i+0.5)*style.maximum.block.height)
            DIS.blit(txt, rect)
        pygame.display.update()
    draw_text()
    def mini():
        global MINI
        if MINI == False:
            SetWindowPos(hwnd, win32con.HWND_DESKTOP,\
                         style.minimum.pos.x,style.minimum.pos.y,
                         style.minimum.width,style.minimum.height,
                         win32con.SWP_NOACTIVATE)#win32con.SWP_NOSIZE)
            DIS.blit(BGMSurf, (0,0))
            pygame.display.update()
            pygame.event.get([MOUSEMOTION, MOUSEBUTTONUP])
        MINI = True
    def maxi():
        global MINI
        if MINI == True:
            mgr.page = 0
            # recreate the window may be the most efficient one
            SetWindowPos(hwnd, win32con.HWND_DESKTOP,\
                         style.maximum.pos.x,style.maximum.pos.y,
                         style.maximum.width,style.maximum.height,
                         win32con.SWP_SHOWWINDOW)
            DIS = pygame.display.set_mode((style.maximum.width,style.maximum.height),NOFRAME)
            draw_text()
        MINI = False
    while True:
        for event in pygame.event.get():
            if MINI == False:
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        start_pos = event.pos
                elif event.type == MOUSEBUTTONUP:
                    if event.button == 1:
                        x0, y0 = event.pos
                        x, y = direction.get_mouse_direction(start_pos, event.pos)
                        if y == 1 or y == -1:
                            mgr.pageturn(-y)
                            draw_text()
                        elif x == -1:
                            mini()
                        elif (3 < x0 < style.maximum.width-3 or\
                              3 < y0 < style.maximum.height-3):
                            #to avoid misclicking or launch the shortcut while maximized
                            mgr.launch((y0//style.maximum.block.height)*style.maximum.rows+
                                       x0//style.maximum.block.width)
                            mini()
                    elif event.button in (5, 4):
                        mgr.pageturn(event.button*2-9)
                        draw_text()
                elif event.type == KEYDOWN:
                    if event.key in (280, 281):
                        mgr.pageturn(event.key *2-561)
                        draw_text()
                    elif event.key == 276:
                        mini()
                elif event.type == ACTIVEEVENT:
                    if event.gain == 0 and event.state == 2:
                        mini()
            elif MINI == True:
                if event.type == MOUSEBUTTONUP:
                    if MOVING == False:
                        print('maximizing', event.pos)
                        maxi()
                    else:
                        MOVING = False
                elif event.type == MOUSEMOTION:
                    if event.buttons == (1, 0, 0):
                        MOVING = True
                        x0, y0 = GetCursorPos()
                        SetWindowPos(hwnd, win32con.HWND_DESKTOP,
                                     x0-style.minimum.width//2,
                                     y0-style.minimum.height//2,0,0,
                                     win32con.SWP_NOSIZE)
                        pygame.event.get([MOUSEMOTION, MOUSEBUTTONUP])
                if event.type == KEYDOWN:
                    if event.key == 13:
                        maxi()
            if event.type == QUIT:
                pygame.quit()
                return
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    return
                elif 49 <= event.key <= 57:
                    mgr.launch(event.key-49)
                    mini()
            elif event.type == MOUSEBUTTONUP:
                if event.button == 3:
                    pygame.quit()
                    return

        pygame.time.wait(20)
if  __name__  == '__main__':
    main()
