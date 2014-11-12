#!/usr/bin/env python

"""
BEETFT v0.1

BEETFT creates a simple interface to control basic function of the BEETHEFIRST 3D printer.
BEETFT requires Pygame to be installed. Pygame can be downloaded from http://pygame.org
BEETFT is developed by Marcos Gomes
https://github.com/marcosfg/BEETFT


The MIT License (MIT)

Copyright (c) 2014 Marcos Gomes

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,p
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

__author__ = "Marcos Gomes"
__license__ = "MIT"

import os
import sys
import pygame
import pygbutton
from time import time

class FilamentChangeScreen():
    
    exit = False
    interfaceState = 0
    
    lblTopText = ["Heating Nozzle","Choose Action","Pick Color"]
    lblTop = None
    lblTopFont = None
    lblTopFontColor = None
    
    buttons = None
    
    image = None
    
    targetTemperature = 220
    nozzleTemperature = 0
    pullInterval = 0.1
    nextPullTime = None
    
    temperatureBarRect = None
    temperatureBarSurf = None
    
    firstNextReady = False
    
    """*************************************************************************
                                Init Method 
    
    Inits current screen components
    *************************************************************************"""
    def __init__(self, screen, interfaceLoader):
        
        print("Loading Filament Change Screen Components")
        
        self.exit = False
        self.firstNextReady = False
        
        self.screen = screen
        self.interfaceLoader = interfaceLoader
        
        self.interfaceState = 0
        
        self.lblTopFont = self.interfaceLoader.GetlblFont(self.interfaceState)
        self.lblTopFontColor = self.interfaceLoader.GetlblFontColor(self.interfaceState)
        
        self.buttons = self.interfaceLoader.GetLeftButtonsList(self.interfaceState)
        
        self.image = pygame.image.load(self.interfaceLoader.GetImagePath())
        
        #TODO ask the printer current Temperature
        self.nozzleTemperature = 0
        
        self.nextPullTime = time() + self.pullInterval
        

    """*************************************************************************
                                handle_events Method 
    
    Received the event vector and checks if it has any event from interface items
    *************************************************************************"""
    def handle_events(self,retVal):
        """handle all events."""
        for event in retVal:
                
            for btn in self.buttons:
                if 'click' in btn.handleEvent(event):
                    btnName = btn._propGetName()
                    
                    if btnName == "Next":
                        if self.interfaceState == 0:
                            self.interfaceState = 1
                        elif self.interfaceState == 2:
                            self.interfaceState = 1
                            
                        self.lblTopFont = None
                        self.lblTopFontColor = None
                        self.buttons = None
                        self.lblTopFont = self.interfaceLoader.GetlblFont(self.interfaceState)
                        self.lblTopFontColor = self.interfaceLoader.GetlblFontColor(self.interfaceState)
                        self.buttons = self.interfaceLoader.GetLeftButtonsList(self.interfaceState)
                            
                    elif btnName == "OK":
                        if self.interfaceState == 1:
                            self.exit = True
                    elif btnName == "Pick Color":
                        self.interfaceState = self.interfaceState + 1
                        self.lblTopFont = None
                        self.lblTopFontColor = None
                        self.buttons = None
                        self.lblTopFont = self.interfaceLoader.GetlblFont(self.interfaceState)
                        self.lblTopFontColor = self.interfaceLoader.GetlblFontColor(self.interfaceState)
                        self.buttons = self.interfaceLoader.GetLeftButtonsList(self.interfaceState)
                    elif btnName == "Load":
                        print("Load Filament")
                    elif btnName == "Unload":
                        print("Unload Filament")
        return
    

    """*************************************************************************
                                update Method 
    
    Updates screen components
    *************************************************************************"""
    def update(self):
        
        self.lblTop = self.lblTopFont.render(self.lblTopText[self.interfaceState], 1, self.lblTopFontColor)
        
        for btn in self.buttons:
            if self.interfaceState == 0:
                if btn._propGetName() == "Next":
                    btn.visible = self.firstNextReady
                else:
                    btn.visible = True
            else:
                btn.visible = True
            

        return

    """*************************************************************************
                                draw Method 
    
    Draws current screen
    *************************************************************************""" 
    def draw(self):
        
        self.screen.blit(self.lblTop, (self.interfaceLoader.GetlblTopXPos(self.interfaceState),
                                            self.interfaceLoader.GetlblTopYPos(self.interfaceState)))
        
        for btn in self.buttons:
            btn.draw(self.screen)
        
        if self.interfaceState == 0:
            # Draw Image
            x = self.interfaceLoader.GetImageX()
            y = self.interfaceLoader.GetImageY()
            self.screen.blit(self.image,(x,y))
            
            fontColor = pygame.Color(0,0,0)
            x = 110
            y = 160
            width = 200
            height = 25
            fillWidth = int((self.nozzleTemperature/self.targetTemperature)*width)
            
            self.temperatureBarRect = pygame.draw.rect(self.screen, fontColor, (x,y,width,height), 3)
            self.temperatureBarSurf = pygame.Surface((fillWidth,height))
            self.temperatureBarSurf.fill(fontColor)
            self.screen.blit(self.temperatureBarSurf, (x,y))
        
        
        
        
        return
    
    """*************************************************************************
                                GetCurrentScreenName Method 
    
    Frees every element from memmory
    *************************************************************************""" 
    def GetCurrentScreenName(self):
        
        return "Filament"
    
    """*************************************************************************
                                KillAll Method 
    
    Frees every element from memmory
    *************************************************************************""" 
    def KillAll(self):
        
        #TODO
        #CANCEL HEATING
        
        return
    
    """*************************************************************************
                                ExitCallBack Method 
    
    Tells the main class to load the default interface
    *************************************************************************""" 
    def ExitCallBack(self):
        
        #TODO
        #CANCEL HEATING
        
        return self.exit
    
    """*************************************************************************
                                Pull Method 
    
    Pull variables
    *************************************************************************""" 
    def Pull(self):
        
        t = time()
        if t > self.nextPullTime:
            self.nextPullTime = time() + self.pullInterval
            if self.nozzleTemperature <= self.targetTemperature:
                self.nozzleTemperature = self.nozzleTemperature + 20
            else:
                self.nozzleTemperature = self.targetTemperature
            
            if self.nozzleTemperature >= self.targetTemperature:
                self.nozzleTemperature = self.targetTemperature
                self.firstNextReady = True
        
        
        return