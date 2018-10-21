import pygame
from pygame.locals import *
from os import popen, environ, _exit
from win32gui import FindWindow, SetWindowPos, PostMessage, GetCursorPos, SetForegroundWindow
import direction
import win32con
import yaml

size = 75
size2 = 30
startx, starty = 0, 500

class NameManager:
    def __init__(self,usr,pas_dict):
        self.acnts=tuple(usr.items())
        self.pas_dict=pas_dict
        self.page = 0
        self.maxpage = len(usrs)//8
        self.total=len(self.acnts)
    def get_acnt(self, i):
        num = self.page*8+i
        if not 0 <= i <= 7:
            return ''
        return self.acnts[num] if num<self.total else ('','')
    def get_usr(self,i):
        return self.get_acnt(i)[1]
    def get_name(self, i):
        return self.get_acnt(i)[0]
    def pageturn(self,pg):
        self.page = max(0,min(self.maxpage, self.page+pg))
    def launch(self, num):
        name=self.get_usr(num)
        name1 = name+':'+self.pas_dict.get(name,'123')+'@' if name else ''
        print (name1)
        popen('start explorer ftp://%s6.163.193.243'%name1)
def get_grid_num(x, y):
    print('redirecting',(x, y))
    return((y//size)*3+x//size)

def find():
    hwnd = FindWindow(None,'oh-my-ftp')
    if hwnd:
        pygame.quit()
        SetWindowPos(hwnd, win32con.HWND_DESKTOP, startx, starty,
                     3*size, 3*size, win32con.SWP_NOSIZE)
        PostMessage(hwnd, win32con.WM_LBUTTONDOWN, 0,(1<<16)+1)
        PostMessage(hwnd, win32con.WM_LBUTTONUP, 0,(1<<16)+1)
        _exit(0)
        return
def main():
    global MINI
    find()
    environ['SDL_VIDEO_WINDOW_POS']='%d,%d'%(startx, starty)
    DIS = pygame.display.set_mode((3*size, 3*size), NOFRAME)
    MINI = False
    MOVING = False
    find()
    pygame.display.set_caption('oh-my-ftp')
    hwnd = FindWindow(None,'oh-my-ftp')
    BGSurf = pygame.surface.Surface((3*size, 3*size))
    BGSurf.fill((9, 68, 134, 10))
    for i in range(3):
        for j in range(3):
            pygame.draw.rect(BGSurf,(13, 140, 235, 10),
                             (i*size, j*size, size, size), 10)
    BG = pygame.image.load('bg.jpg')
    BG = pygame.transform.scale(BG,(3*size, 3*size))
    BG.set_alpha(45)
    BGSurf.blit(BG,(0, 0))        
    pygame.font.init()
    FontObj = pygame.font.SysFont('stliti', 24)
    mgr = NameManager()
    def draw_text():
        DIS.blit(BGSurf,(0, 0))
        for n in range(8):
            i, j = n//3, n%3
            name = mgr.get_name(n)
            txt = FontObj.render(name, True,(255, 255, 255))
            rect = txt.get_rect()
            rect.center=(j*size+size/2, i*size+size/2)
            DIS.blit(txt, rect)
        pygame.display.update()
    draw_text()
    def mini():
        global MINI
        if MINI == False:
            SetWindowPos(hwnd, win32con.HWND_DESKTOP,\
                         0, 5*size, size2, size2, win32con.SWP_NOACTIVATE)#win32con.SWP_NOSIZE)
            DIS.fill((9, 68, 134, 10))
            pygame.draw.rect(DIS,(13, 140, 235, 10),(0, 0, size2, size2), 4)
            pygame.display.update()
            pygame.event.get([MOUSEMOTION, MOUSEBUTTONUP])
        MINI = True
    def maxi():
        global MINI
        if MINI == True:
##            environ['SDL_VIDEO_WINDOW_POS']='%d,%d'%(startx, starty)
##            DIS = pygame.display.set_mode((3*size, 3*size), NOFRAME)
            mgr.page = 0
            #it is quite strange that SetWindowPos should be added
            SetWindowPos(hwnd, win32con.HWND_DESKTOP,\
                         startx, starty, 3*size, 3*size, win32con.SWP_SHOWWINDOW)
            SetForegroundWindow(hwnd)
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
                        if (x0 < 3 or x0 > size*3-3 or y0 < 3 or y0 > size*3-3):
                            continue
                        x, y = direction.get_mouse_direction(
                            start_pos, event.pos)
                        if y == 1 or y == -1:
                            mgr.pageturn(y)
                            draw_text()
                        elif x == -1:
                            mini()
                        else:
                            mgr.launch(get_grid_num(*event.pos))
                            mini()
                    elif event.button == 3:
                        pygame.quit()
                        return
                    elif event.button in (5, 4):
                        mgr.pageturn(event.button*2-9)
                        draw_text()
                elif event.type == KEYDOWN:
                    elif event.key in (280, 281):
                        mgr.pageturn(event.key *2-561)
                        draw_text()
                    elif event.key == 276:
                        mini()
                    elif event.key == 13:
                        maxi()
                elif event.type == ACTIVEEVENT:
                    if event.gain == 0 and event.state == 2:
                        mini()
            if MINI == True:
                if event.type == MOUSEBUTTONDOWN and event.type == MOUSEBUTTONUP:
                    if MOVING == False:
                        print('maximizing', event.pos)
                        maxi()
                    else:
                        MOVING = False
                elif event.type == MOUSEMOTION:
                    if MINI == True and event.buttons == (1, 0, 0):
                        MOVING = True
                        x0, y0 = GetCursorPos()
                        SetWindowPos(hwnd, win32con.HWND_DESKTOP,
                                     x0-size2//2, y0-size2//2, size2, size2,
                                     win32con.SWP_NOSIZE)
                        pygame.event.get([MOUSEMOTION, MOUSEBUTTONUP])
            if event.type == QUIT:
                pygame.quit()
                return
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    return
                elif 49 <= event.key <= 57:
                    mgr.launch(event.key-49)
                    mini()

        pygame.time.wait(20)
if  __name__  == '__main__':
    main()
