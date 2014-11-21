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



class CalibrationScreen():
    
    calibrationState = 0
    
    interfaceLoader = None
    lbl = None
    lblText = ["Adjust Bed Height","Adjust Left Bolt","Adjust Right Bolt"]
    
    buttons = None
    
    exit = False
    
    """
    Images
    """
    rightBoltImgPath = None
    leftBoltImgPath = None
    rightBoltImgX = 0
    rightBoltImgY = 0
    leftBoltImgX = 0
    leftBoltImgY = 0
    
    """*************************************************************************
                                Init Method 
    
    Inits current screen components
    *************************************************************************"""
    def __init__(self, screen, interfaceLoader):
        
        print("Loading Calibration Screen Components")
        
        self.exit = False
        
        self.screen = screen
        self.interfaceLoader = interfaceLoader
        
        self.calibrationState = 0
        
        self.lblFont = self.interfaceLoader.GetlblFont(self.calibrationState)
        self.lblFontColor = self.interfaceLoader.GetlblFontColor(self.calibrationState)
        
        self.buttons = self.interfaceLoader.GetLeftButtonsList(self.calibrationState)
        
        self.rightBoltImg = pygame.image.load(self.interfaceLoader.GetRightImgPath())
        self.leftBoltImg = pygame.image.load(self.interfaceLoader.GetLeftImgPath())
        self.rightBoltImgX = self.interfaceLoader.GetRightImgX()
        self.rightBoltImgY = self.interfaceLoader.GetRightImgY()
        self.leftBoltImgX = self.interfaceLoader.GetLeftImgX()
        self.leftBoltImgY = self.interfaceLoader.GetLeftImgY()
        
        
        
        

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
                        self.calibrationState = self.calibrationState + 1
                        if self.calibrationState > 2:
                            self.exit = True
                            self.calibrationState = 0
                        else:
                            self.lblFont = None
                            self.lblFontColor = None
                            self.buttons = None
                            self.lblFont = self.interfaceLoader.GetlblFont(self.calibrationState)
                            self.lblFontColor = self.interfaceLoader.GetlblFontColor(self.calibrationState)
                            self.buttons = self.interfaceLoader.GetLeftButtonsList(self.calibrationState)
                    
                    elif btnName == "+0.5mm":
                        print("Move +0.5mm")
                    elif btnName == "+0.05mm":
                        print("Move +0.05mm")
                    elif btnName == "-0.05mm":
                        print("Move -0.05mm")
                    elif btnName == "-0.5mm":
                        print("Move -0.5mm")
                    
        return

    """*************************************************************************
                                update Method 
    
    Updates screen components
    *************************************************************************"""
    def update(self):
        
        self.lbl = self.lblFont.render(self.lblText[self.calibrationState], 1, self.lblFontColor)
        
        for btn in self.buttons:
            btn.visible = True
        
        return

    """*************************************************************************
                                draw Method 
    
    Draws current screen
    *************************************************************************""" 
    def draw(self):
        
        self.screen.blit(self.lbl, (self.interfaceLoader.GetlblXPos(self.calibrationState),
                                            self.interfaceLoader.GetlblYPos(self.calibrationState)))
        
        for btn in self.buttons:
            btn.draw(self.screen)
        
        if self.calibrationState == 1:
            # Draw Image
            self.screen.blit(self.leftBoltImg,(self.leftBoltImgX,self.leftBoltImgY))
        elif self.calibrationState == 2:
            # Draw Image
            self.screen.blit(self.rightBoltImg,(self.rightBoltImgX,self.rightBoltImgY))
        
        
        return
    
    """*************************************************************************
                                GetCurrentScreenName Method 
    
    Frees every element from memmory
    *************************************************************************""" 
    def GetCurrentScreenName(self):
        
        return "Calibration"
    
    """*************************************************************************
                                KillAll Method 
    
    Frees every element from memmory
    *************************************************************************""" 
    def KillAll(self):
        
        self.calibrationState = None
        self.interfaceLoader = None
        self.lbl = None
        self.lblText = None
        self.buttons = None
        self.exit = None
        self.rightBoltImgPath = None
        self.leftBoltImgPath = None
        self.rightBoltImgX = None
        self.rightBoltImgY = None
        self.leftBoltImgX = None
        self.leftBoltImgY = None
        
        return
    
    """*************************************************************************
                                ExitCallBack Method 
    
    Tells the main class to load the default interface
    *************************************************************************""" 
    def ExitCallBack(self):
        
        return self.exit
    
    """*************************************************************************
                                Pull Method 
    
    Pull variables
    *************************************************************************""" 
    def Pull(self):
        
        return