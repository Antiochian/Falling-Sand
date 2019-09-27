# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 06:43:46 2019

@author: user
"""

#from FallingSand import Particle
import random
import pygame

scale = 2
aircolor = (0,0,0)    
allelements = {}
changed = {}
(Nx,Ny) = (400,450)
FPS =20

yellow = (181,137,0)
beige = (238,232,213)
darkbeige = (171, 152, 92)
orange = (203,75,22) #orange
blue = (38, 139, 210) #blue
red =  (220,50,47)
green = (133,153,0) 
grey = (88,	110, 117)
magenta = (211,54,130)
class Particle:
    def __init__(self,x,y,allelements,SURFACE):
        #allelements is a REFERENCE to a dictionary containing all element instances
        self.x = x
        self.y = y
        self.allelements = allelements
        self.SURFACE = SURFACE
    
    def checkkill(self,x,y): #checks to see if particle can be deleted
        if not 0 <= self.x <= Nx:
            self.draw(x,y,aircolor) #wipe pixel
            del self.allelements[(x,y)]
            return True
        elif not 0 <= self.y <= 300:
            self.draw(x,y,aircolor)
            del self.allelements[(x,y)]
            return True
        return False
        
    def checktarget(self,x,y):
        if self.allelements.get( (x,y) ) == None: #return whatever object is at target location, or False if not
            return True #if space is EMPTY return TRUE
        else: #if space is occupied, return FALSE (used to return occupier but i nixed that functionality)
            #return self.allelements.get( (x,y) )
            return False
    
    def targetcolor(self,x,y): #very similar to the above, but instead of returning boolean, returns occupier object
        if self.allelements.get( (x,y) ) == None: #return whatever object is at target location, or False if not
            return self.allelements.get( (None,None) ).color #if space is empty return NULLELEMENT
        else:
            return self.allelements.get( (x,y) ).color
    
    def draw(self,x,y,color):
        self.SURFACE.fill(color, pygame.Rect(x*scale, y*scale, scale, scale))
        return

    def goto(self, newx,newy, overwritechance = 0.0):
        global changed
        #SAND/WATER interaction - sand changes color and overwrites water
        if (self.color == beige or self.color == darkbeige) and self.targetcolor(newx,newy) == blue:
            self.color = darkbeige #CHANGE SAND COLOR TO WETSAND COLOR
            self.draw(newx,newy,self.color)
            overwritechance = 1 #set overwrite
        #WATER/SAND interaction - sand changes color but is not overwritten by water
        if self.color == blue and self.targetcolor(newx,newy) == beige:
            self.allelements[(newx,newy)].color = darkbeige
            self.draw(newx,newy,darkbeige)
        #WETSAND/DRYSAND interaction (wetness should spread slowly through sand)
        if self.color == darkbeige and self.targetcolor(newx,newy) == beige and random.random() < 0.08:
            self.allelements[(newx,newy)].color = darkbeige
            self.draw(newx,newy,darkbeige)
        #LIQUID/LIQUID interaction
        
        #DEFAULT behaviour
        if (self.checktarget(newx,newy) ) or random.random()<overwritechance: #go ahead with move IF space is free
            (oldx,oldy) = (self.x,self.y)
            del self.allelements[(oldx,oldy)] #delete current location from instance dictionary
            #self.SURFACE.fill(aircolor, pygame.Rect(oldx*self.scale, oldy*self.scale, self.scale, self.scale))
            self.draw(oldx,oldy,aircolor) #delete old pixel
            (self.x,self.y) = (newx,newy)
            self.allelements[(newx,newy)] = self
            self.draw(newx,newy,self.color)
            #self.SURFACE.fill(self.color, pygame.Rect(newx*self.scale, newy*self.scale, self.scale, self.scale))
            #mark locations as changed
            changed[(oldx,oldy)] = True
            changed[(newx,newy)] = True
            return True
        return False #otherwise return "failed" boolean
        
class Metal(Particle): #metal just sits there and doesnt move
    def __init__(self,x,y,allelements,SURFACE):
        self.type = "solid"
        self.color = grey
        Particle.__init__(self,x,y,allelements,SURFACE) 
        self.draw(self.x, self.y,self.color) 
        
    def update(self):
        pass
    
class Water(Particle): #water should flow and fall
    def __init__(self,x,y,allelements,SURFACE):
        self.type = "liquid"
        self.color = blue
        Particle.__init__(self,x,y,allelements,SURFACE)
        self.draw(self.x, self.y,self.color) 
        
    def debug(self): #just to check if something exists
        print("Hello world, I am water!")
        print("My color is: ",self.color)
        
        
    def update(self):
        """
        Water behaviour is like so: water is allowed to make 2-3 "actions" per turn
        it first tries to fall downward, with a chance to move left or right as it does so
        if it cant fall down it is then almost guaranteed to flow left or right
        if it hits a wall it will "reflect" off and move in the other direction
        """
        if self.checkkill(self.x,self.y):
            return
        updates = 0 #start with zero actions
        flowdirection = random.randint(0,1) * 2 - 1 #returns +-1, decides if particle moves left or right
        if random.random() > 0.9: #small chance to not flow at all
            flowdirection = 0 #i.e: dont flow   
        while updates < 2:
            if self.goto( self.x, self.y + 1):
                updates +=1 #log one cycle as complete
                if self.goto( self.x, self.y + 1):
                    updates +=1#log one cycle as complete
            if self.goto(self.x + flowdirection, self.y): #if space is available to go sideways
                pass
            elif self.goto(self.x - flowdirection, self.y): #if one side is blocked, "reflect" off other way
                flowdirection *= -1
            updates += 0.67
            
class Acid(Particle): #like water, can eat through metal
    def __init__(self,x,y,allelements,SURFACE):
        self.type = "liquid"
        self.color = green
        Particle.__init__(self,x,y,allelements,SURFACE)
        self.draw(self.x, self.y,self.color) 
        
    def debug(self): #just to check if something exists
        print("Hello world, I am acid!")
        print("My color is: ",self.color)
        
        
    def update(self):
        """
        ACID behaves like water but has a certain chance to eat through containing
        materials, defined in the variable "acidchance"
        """
        if self.checkkill(self.x,self.y):
            return
        acidchance = 0.01
        updates = 0 #start with zero actions
        flowdirection = random.randint(0,1) * 2 - 1 #returns +-1, decides if particle moves left or right
        if random.random() > 0.9: #small chance to not flow at all
            flowdirection = 0 #i.e: dont flow   
        while updates < 2:
            if self.goto( self.x, self.y + 1,acidchance):
                updates +=1 #log one cycle as complete
                if self.goto( self.x, self.y + 1,acidchance):
                    updates +=1 #log one cycle as complete
            if self.goto(self.x + flowdirection, self.y,acidchance): #if space is available to go sideways
                pass
            elif self.goto(self.x - flowdirection, self.y,acidchance): #if one side is blocked, "reflect" off other way
                pass
            updates += 1
    
class Sand(Particle): #sand behaves like a very viscous liquid, BUT is CLASSED as a solid
    def __init__(self,x,y,allelements,SURFACE):
        self.type = "solid"
        self.color = beige
        self.flowchance = 0.05 #chance to behave as liquid per tick (CAN CHANGE IF WET)
        Particle.__init__(self,x,y,allelements,SURFACE)
        self.draw(self.x, self.y,self.color) 
        
    def debug(self): #just to check if something exists
        print("Hello world, I am sand!")
        print("My color is: ",self.color)
        
        
    def update(self):
        """
        Sand is like water but it hardly ever flows sideways, and if it gets wet
        then it solidifies and becomes immovable. Wet sand slowly "infects" nearby dry sand
        (This behaviour is codified inside the goto function)
        """
        if self.checkkill(self.x,self.y):
            return
        updates = 0 #start with zero actions
        
        if self.color == beige:
            flowchance = 0.05 #5% chanc eto flow per tick if dry
        elif self.color == darkbeige:
            flowchance = 0 #never flow if wet
            
        flowdirection = random.randint(0,1) * 2 - 1 #returns +-1, decides if particle moves left or right
        if random.random() > flowchance: #LARGE chance to not flow at all for sand
            flowdirection = 0 #i.e: dont flow   
        while updates < 2:
            if self.goto( self.x, self.y + 2): #if space is available to fall down 2 spaces
                updates += 2
            elif self.goto( self.x, self.y + 1):
                updates +=1 #log one cycle as complete
            if self.goto(self.x + flowdirection, self.y): #if space is available to go sideways
                pass
#            elif self.goto(self.x - flowdirection, self.y): #if one side is blocked, "reflect" off other way
#                pass
            updates += 2
            
class NullElement(Particle): #this placeholder sits at (None,None) and does NOTHING
    def __init__(self,allelements,SURFACE):
        self.color = None
        self.x = None
        self.y = None
        Particle.__init__(self,self.x,self.y,allelements,SURFACE)
    def update(self):
        pass
        