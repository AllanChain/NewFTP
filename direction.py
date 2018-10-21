'''In this module , a positive x means it goes right,
and a positive y means it goes down.'''
from pygame.locals import *
class Direction:
     def __init__(self,x,y):
          self.x=x
          self.y=y
          self.direc=(x,y)
     def __str__(self):
          return ('x:%s y:%s'%(self.x,self.y))
     def __repr__(self):
          return ('x:%s y:%s'%(self.x,self.y))
class Pattern:
     def __init__(self,up,down,left,right):
          self.up=up
          self.down=down
          self.right=right
          self.left=left
          self._tuple=(up,down,left,right)
     def get_direction(self,key):
          if key in self._tuple:
               num=self._tuple.index(key)
               if num<=1:
                    return Direction(0,num*2-1)
               else:
                    return Direction(num*2-5,0)
patterns={
     'UDLR':Pattern(273,274,276,275),
     'WSAD':Pattern(119,115,97,100),}

def get_key_direction(key_event):
     #direction_dict={}
     for key,pattern in patterns.items():
          tp=pattern.get_direction(key_event.key)
          if tp:
               return key,tp
     #return direction_dict
def add_pattern(string):
     assert len(string)==4,'Must four'
     #print(Pattern(*(list(map(lambda x:ord(x),string.lower())))))
     patterns.update({string:Pattern(*(list(map(lambda x:ord(x),string.lower()))))})
def remove_pattern(string):
     patterns.pop(string,None)
def get_mouse_direction(start_pos,end_pos)          :
     relx,rely=end_pos[0]-start_pos[0],end_pos[1]-start_pos[1]
     if relx**2+rely**2>20:
          if abs(relx)>2*abs(rely):
               gox=int(relx/abs(relx))
               goy=0
          elif abs(rely)>2*abs(relx):
               goy=int(rely/abs(rely))
               gox=0
          else:return 0,0
          return gox,goy
     return 0,0
