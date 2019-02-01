from .finder import find
import pygame
from pygame.locals import *
from os import popen, environ, _exit
import os.path
from win32gui import FindWindow, SetWindowPos, PostMessage, GetCursorPos,\
    SetForegroundWindow, ShowWindow
import win32con
import yaml
from box import SBox
from . import messager
from .ftp_parser import SERVER, DEFAULT_PASS


class NameManager:
    def __init__(self, usr, pas_dict, perpage):
        self.acnts = tuple(usr.items())
        self.pas_dict = pas_dict
        self.page = 0
        self.perpage = perpage
        self.maxpage = len(usr)//perpage
        self.total = len(self.acnts)

    def get_acnt(self, i):
        num = self.page*self.perpage+i
        if not 0 <= i <= self.perpage-1:
            return ('', '')
        return self.acnts[num] if num < self.total else ('', '')

    def get_usr(self, i):
        return self.get_acnt(i)[1]

    def get_name(self, i):
        return self.get_acnt(i)[0]

    def pageturn(self, pg):
        self.page = max(0, min(self.maxpage, self.page+pg))

    def launch(self, num):
        name = self.get_usr(num)
        print(num)
        if name.startswith('$'):
            # Out command
            # e.g. $python -m some_module
            cmd = name[1:]
        elif '/' in name or '\\' in name:
            # Directory, open with explorer.exe
            # Or open file with default application
            # e.g. D:\Desctop\mess\
            # e.g. ~/PythonPro/
            # e.g. D:\Desctop\1.txt
            cmd = 'start explorer "%s"' % name
        elif name.isalpha() or name == '':
            # Ensure tha acnt is valid
            name1 = name+':'+str(self.pas_dict.get(name, DEFAULT_PASS))\
                + '@' if name else ''
            # If name is '', no :@ needed
            # here get(name,'123') means default password is '123'
            print(name1)
            cmd = 'start explorer ftp://%s%s' % (name1, SERVER)
        popen(cmd)


def C(color):
    '''Color converting'''
    if isinstance(color, tuple):
        return color
    if isinstance(color, int):
        # In case that color is 580646 stuff
        color = str(color)
    if isinstance(color, str):
        if color.startswith('#'):
            color = color[1:]
        if len(color) == 6:
            n = int(color, base=16)
            return (n >> 16) % 256, (n >> 8) % 256, n % 256


def get_mouse_direction(start_pos, end_pos):
    relx, rely = end_pos[0]-start_pos[0], end_pos[1]-start_pos[1]
    if relx**2+rely**2 > 20:
        if abs(relx) > 2*abs(rely):
            gox = int(relx/abs(relx))
            goy = 0
        elif abs(rely) > 2*abs(relx):
            goy = int(rely/abs(rely))
            gox = 0
        else:
            return 0, 0
        return gox, goy
    return 0, 0


def load():
    with open('gui_config.yaml', 'r', encoding='utf-8') as f:
        usr, pas, sty = yaml.load_all(f)
    try:
        with open('styles/' + sty['style'] + '.yaml', encoding='utf-8') as f:
            # Here store some attributes to access them conveniently
            new_style = SBox(yaml.load(f))
        parents = [sty['style']]
        while 'parent' in new_style and not new_style['parent'] in parents:
            parents.append(new_style['parent'])
            with open('styles/%s.yaml' % new_style['parent'], encoding='utf-8') as f:
                older_style = SBox(yaml.load(f))
                new_style = older_style.update(new_style)
                new_style = older_style
        if not 'Win7' in parents:
            with open('Styles/Win7.yaml', encoding='utf-8') as f:
                # Using Win7 as ultimate parent
                style = SBox(yaml.load(f))
                style.update(new_style)
        else:
            style = new_style
    except FileNotFoundError:
        messager.warn("样式文件不可用！将使用默认样式")
        with open('Styles/Win7.yaml', encoding='utf-8') as f:
            style = SBox(yaml.load(f))
    style.maximum.width = style.maximum.cols*style.maximum.block.width
    style.maximum.height = style.maximum.rows*style.maximum.block.height
    mgr = NameManager(usr, pas, style.maximum.cols*style.maximum.rows-1)
    return mgr, style


def draw_bg(style):
    BGSurf = pygame.surface.Surface(
        (style.maximum.width, style.maximum.height))
    BGSurf.fill(C(style.maximum.color.background))
    for i in range(style.maximum.cols):
        for j in range(style.maximum.rows):
            pygame.draw.rect(BGSurf, C(style.maximum.color.border),
                             (i*style.maximum.block.width,
                              j*style.maximum.block.height,
                              style.maximum.block.width,
                              style.maximum.block.height),
                             style.maximum.border)
    if not style.maximum.image is None:
        BG = pygame.image.load('Styles/'+style.maximum.image.path)
        BG = pygame.transform.scale(
            BG, (style.maximum.width, style.maximum.height))
        BG.set_alpha(style.maximum.image.alpha)
        BGSurf.blit(BG, (0, 0))
    BGMSurf = pygame.surface.Surface(
        (style.minimum.width, style.minimum.height))
    BGMSurf.fill(C(style.minimum.color.background))
    pygame.draw.rect(BGMSurf, C(style.minimum.color.border), (0, 0, style.minimum.width,
                                                              style.minimum.height), style.minimum.border)
    return BGSurf, BGMSurf


@messager.log_it(file='log_gui.txt')
def main():
    global MINI
    find()
    try:
        mgr, style = load()
    except Exception:
        messager.log_and_exit(message="配置文件加载失败！")
    environ['SDL_VIDEO_WINDOW_POS'] = '%d,%d' % (
        style.maximum.pos.x, style.maximum.pos.y)
    DIS = pygame.display.set_mode(
        (style.maximum.width, style.maximum.height), NOFRAME)
    MINI = False
    MOVING = False
    find()
    pygame.display.set_caption('oh-my-ftp')
    hwnd = FindWindow(None, 'oh-my-ftp')
    BGSurf, BGMSurf = draw_bg(style)
    mini_clock = pygame.time.Clock()
    mini_clock.tick()
    pygame.font.init()
    FontObj = pygame.font.SysFont(style.font.font, style.font.size)

    def draw_text():
        if MINI == True:
            DIS.blit(BGMSurf, (0, 0))
            txt = FontObj.render(str(mgr.page), True, C(style.font.color))
            rect = txt.get_rect()
            rect.center = (style.minimum.width//2, style.minimum.height//2)
            DIS.blit(txt, rect)
        else:
            DIS.blit(BGSurf, (0, 0))
            for n in range(mgr.perpage):
                i, j = n//style.maximum.cols, n % style.maximum.cols
                name = mgr.get_name(n)
                txt = FontObj.render(name, True, C(style.font.color))
                rect = txt.get_rect()
                rect.center = ((j+0.5)*style.maximum.block.width,
                               (i+0.5)*style.maximum.block.height)
                DIS.blit(txt, rect)
        pygame.display.update()
    draw_text()

    def mini():
        global MINI
        if MINI == False:
            MINI = True
            SetWindowPos(hwnd, win32con.HWND_DESKTOP,
                         style.minimum.pos.x, style.minimum.pos.y,
                         style.minimum.width, style.minimum.height,
                         win32con.SWP_NOACTIVATE)  # win32con.SWP_NOSIZE)
            DIS.blit(BGMSurf, (0, 0))
            pygame.display.update()
            pygame.event.get([MOUSEMOTION, MOUSEBUTTONUP])

    def maxi():
        global MINI
        if MINI == True:
            MINI = False
            mini_clock.tick()
            mgr.page = 0
            # recreate the window may be the most efficient one
            SetWindowPos(hwnd, win32con.HWND_DESKTOP,
                         style.maximum.pos.x, style.maximum.pos.y,
                         style.maximum.width, style.maximum.height,
                         win32con.SWP_SHOWWINDOW)
            draw_text()
    while True:
        for event in pygame.event.get():
            if MINI == False:
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        start_pos = event.pos
                elif event.type == MOUSEBUTTONUP:
                    if event.button == 1:
                        x0, y0 = event.pos
                        x, y = get_mouse_direction(start_pos, event.pos)
                        if y == 1 or y == -1:
                            mgr.pageturn(-y)
                            draw_text()
                        elif x == -1:
                            mini()
                        elif (3 < x0 < style.maximum.width-3 or
                              3 < y0 < style.maximum.height-3):
                            # to avoid misclicking or launch the shortcut while maximized
                            mgr.launch((y0//style.maximum.block.height)*style.maximum.cols +
                                       x0//style.maximum.block.width)
                            mini()
                    elif event.button in (5, 4):
                        mgr.pageturn(event.button*2-9)
                        draw_text()
                elif event.type == KEYDOWN:
                    if event.key == 276:
                        mini()
                elif event.type == ACTIVEEVENT:
                    # lose focus
                    if event.gain == 0 and event.state == 2:
                        time = mini_clock.tick()
                        print(time)
                        if time > 700:
                            mini()
            elif MINI == True:
                if event.type == MOUSEBUTTONUP:
                    if event.button == 1:
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
                                     y0-style.minimum.height//2, 0, 0,
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
                elif event.key in (280, 281):
                    mgr.pageturn(event.key * 2-561)
                    draw_text()
                elif event.key == K_F4 and event.mod != 0:
                    ShowWindow(hwnd, win32con.SW_HIDE)
            elif event.type == MOUSEBUTTONUP:
                if event.button == 3:
                    pygame.quit()
                    return

        pygame.time.wait(50)


if __name__ == '__main__':
    main()
