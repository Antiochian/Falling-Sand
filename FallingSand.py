# -*- coding: utf-8 -*-
"""
Created on Sun Sep 22 05:40:48 2019

@author: user
"""
import pygame
import sys
import numpy as np
from FallingSand_Elements import *

def globalchecktarget(x,y):
        if allelements.get( (x,y) ) == None: #return whatever object is at target location, or False if not
            return True #if space is EMPTY return TRUE
        else: #if space is occupied, return FALSE (used to return occupier but i nixed that functionality)
            return False  #return self.allelements.get( (x,y) )

def pendraw(elementtype,x,y,pensize): #DOES NOT ACCEPT DECIMAL POSITIONS
    #this function places a suitable number of elements in a circle at the position specified    
    if pensize == 0 and globalchecktarget(x+xdisp,y+ydisp):
        allelements[(x,y)] = elementtype(x,y,allelements,SURFACE) #place 1 pixel
    else:
        for xdisp in range(-pensize,pensize): #penzize is the radius
            for ydisp in range(-pensize,pensize):
                if globalchecktarget(x+xdisp,y+ydisp):
                    allelements[(x+xdisp,y+ydisp)] = elementtype(x+xdisp,y+ydisp,allelements,SURFACE)
    return

pygame.init()
window = pygame.display.set_mode( (Nx,Ny) )
pygame.display.set_caption("Antioch's Falling Sand")

SURFACE = window.copy() #SURFACE is where all the magic will happen




###DEBUG INITIALISATION###
#
##for x in range(50,100):
##    for y in range(24,26):
##        allelements[(x,y)] = Water(x,y,allelements,SURFACE)
#    #SURFACE.fill((255,255,255), pygame.Rect(x*scale, y*scale, scale, scale))
for x in range(70,150): #build testing bucket
    y = 150
    allelements[(x,y)] = Metal(x,y,allelements,SURFACE)
    allelements[(x,y+1)] = Metal(x,y+1,allelements,SURFACE)
for y in range(138,150):
    if y in range(145,150):
        allelements[(70,y)] = Metal(70,y,allelements,SURFACE)
        allelements[(80,y)] = Metal(80,y,allelements,SURFACE)
    allelements[(149,y)] = Metal(149,y,allelements,SURFACE)
    
##########################
window.blit(SURFACE, (0,0))
clock = pygame.time.Clock()
pygame.display.update()
ActiveElement = Metal #default
pensize = 1

#INITIALISE NULLELEMENT
allelements[(None,None)]= NullElement(allelements,SURFACE)
while True:
    changed = {}
    clock.tick(FPS)
    
    for event in pygame.event.get(): #detect events
        if event.type == pygame.QUIT: #detect attempted exit
            pygame.quit()
            sys.exit()
        if pygame.mouse.get_pressed()[0]:
            pendraw(ActiveElement,int(pygame.mouse.get_pos()[0]/scale),int(pygame.mouse.get_pos()[1]/scale),pensize)
    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[49]:
        pensize = 1
        ActiveElement = Metal
    if pressed_keys[50]:
        pensize = 2
        ActiveElement = Water
    if pressed_keys[51]:
        pensize = 2
        ActiveElement = Sand
    if pressed_keys[52]:
        pensize = 2
        ActiveElement = Acid

    #update screen
    window.blit(SURFACE, (0,0))
    for element in list(allelements.keys()):
        try:
            allelements[element].update()
        except KeyError:
            pass
        
#        if element not in changed:
#            allelements[element].update()
    pygame.display.update()