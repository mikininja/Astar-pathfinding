# -*- coding: utf-8 -*-
"""
Created on Sun Feb 25 16:59:58 2018

@author: miki1
"""

import pygame
from pygame.locals import Rect
from random import randint
from math import sqrt
from math import floor
L=1000
f=10
SIZEX=L
SIZEY=L
width=floor(L/f)
height=floor(L/f)
grid=[]
openset=[]
closeset=[]
start=None
end=None
def heuristic(p1,p2):
    return sqrt((p1.i-p2.i)**2+(p1.j-p2.j)**2)
def onstart():
    global grid,openset,closeset,start,end
    grid=[]
    openset=[]
    closeset=[]
    start=None
    end=None
    for i in range(0,width):
        grid.append([])
        for j in range(0, height):
            grid[i].append(Punto(i,j))
    for v in grid:
        for p in v:
            p.setvicini()
            print(p.vicini)
    start=grid[0][0]
    end=grid[width-1][height-1]
    start.obstacle=False
    end.obstacle=False
    openset.append(start)
class Punto(object):
    def __init__(self,i,j):
        self.i=i
        self.j=j
        self.f=0
        self.g=0
        self.h=0
        self.vicini=[]
        self.prev=None
        self.obstacle= True if randint(0,100)<=40 else False
    def __str__(self):
        return (self.i,self.j)
    def __repr__(self):
        return "%d %d" %(self.i, self.j)
    def setvicini(self):
        for i in range(-1,2):
            for j in range(-1,2):
                if i+self.i>=0 and i+self.i<width and j+self.j>=0 and j+self.j<height:
                    if i+self.i!=self.i or j+self.j!=self.j:    
                        self.vicini.append(grid[i+self.i][j+self.j])
        
        
class Board(object):
    def __init__(self,sx,sy):
        self.x=sx
        self.y=sy
        pygame.init()
        self.rekt=Rect(0,0,sx,sy)
        self.screen=pygame.display.set_mode(self.rekt.size,0)
        self.bg=pygame.Surface(self.rekt.size)
        self.path=[]
    def printsquares(self):
        for v in grid:
            for p in v:
                if p.obstacle:
                    pygame.draw.rect(self.screen,(0,0,0),Rect(p.i*f,p.j*f,f,f),0)
                else:
                    pygame.draw.rect(self.screen,(0,0,0),Rect(p.i*f,p.j*f,f,f),1)
        for o in openset:
            pygame.draw.rect(self.screen,(0,255,0),Rect(o.i*f,o.j*f,f,f),0)
        for o in closeset:
            pygame.draw.rect(self.screen,(255,0,0),Rect(o.i*f,o.j*f,f,f),0)
    def drawpath(self):
        for p in self.path:
            pygame.draw.rect(self.screen,(0,0,255),Rect(p.i*f,p.j*f,f,f),0)
            
    def buildpath(self,n):
        self.path=[]
        temp=n
        self.path.append(temp)
        while temp.prev:
            self.path.append(temp.prev)
            temp=temp.prev
    def blit(self):
        self.screen.fill((255,255,255))
        self.printsquares()
        if len(openset)>0:
            cur=openset[0]
            for o in openset:
                if o.f<cur.f:
                    cur=o
            if cur==end:
                print("done")
            else:
                openset.remove(cur)
                closeset.append(cur)
                for nei in cur.vicini:
                    if ((not(nei in closeset)) and (not nei.obstacle)):
                        tg=cur.g+1
                        newp=False
                        if nei in openset:
                            if tg<nei.g:
                                nei.g=tg
                                newp=True
                        else:
                            nei.g=tg
                            openset.append(nei)
                            newp=True
                        if newp:
                            nei.h=heuristic(nei,end)
                            nei.f=nei.h+nei.g
                            nei.prev=cur
            self.buildpath(cur)
        else:
            print("nessun percorso")
        
        self.drawpath()
        
        
        pygame.display.update()

    def run(self):
        while 1:
            self.blit()
            pygame.time.delay(2)
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self._running = False
                    pygame.quit()
                if e.type == pygame.MOUSEBUTTONDOWN:
                    self.path=[]
                    onstart()
                
            

class Splash(object):
    def __init__(self):
        self.x=SIZEX
        self.y=SIZEY

if __name__=="__main__":
    for i in range(0,width):
        grid.append([])
        for j in range(0, height):
            grid[i].append(Punto(i,j))
    for v in grid:
        for p in v:
            p.setvicini()
            print(p.vicini)
    start=grid[0][0]
    end=grid[width-1][height-1]
    start.obstacle=False
    end.obstacle=False
    openset.append(start)
    game=Board(SIZEX,SIZEY)
    game.run()