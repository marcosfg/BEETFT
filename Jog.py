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

import pygame
import BEECommand

class JogScreen():
    
    screen = None
    
    lblFont = None
    lblTop = None
    lblFontColor = None
    
    jogButtons = None
    
    multiplier = "1"
    multiplierRect = None
    
    interfaceLoader = None
    
    beeConnect = None
    
    """*************************************************************************
                                Init Method 
    
    Inits current screen components
    *************************************************************************"""
    def __init__(self, screen, interfaceLoader, beeConnect):
        
        self.beeConnect = beeConnect
        
        self.screen = screen
        self.interfaceLoader = interfaceLoader
        
        self.lblFont = self.interfaceLoader.GetlblFont()
        self.lblFontColor = self.interfaceLoader.GetlblFontColor()
        
        self.jogButtons = self.interfaceLoader.GetLeftButtonsList()
        
        self.multiplier = 1
        
        print("Loading Jog Screen Components")
        
        

    """*************************************************************************
                                handle_events Method 
    
    Received the event vector and checks if it has any event from interface items
    *************************************************************************"""
    def handle_events(self,retVal):
        """handle all events."""
        for event in retVal:
            
            for btn in self.jogButtons:
                if 'click' in btn.handleEvent(event):
                    btnName = btn._propGetName()
                    
                    if (btnName == '0.1') or (btnName == '1') or (btnName == '10'):
                        self.multiplier = btnName
                    elif btnName == "HomeXY":
                        print("G28 X0 Y0")
                        comm =BEECommand.Command()
                        comm.homeXY()
                    elif btnName == "HomeZ":
                        print("G28 Z0")
                        comm =BEECommand.Command()
                        comm.homeZ()
                    elif btnName == "X+":
                        val = float(self.multiplier)
                        print("X",val)
                        comm =BEECommand.Command()
                        comm.move(val,None,None,None)
                    elif btnName == "X-":
                        val = -1 * float(self.multiplier)
                        print("X",val)
                        comm =BEECommand.Command()
                        comm.move(val,None,None,None)
                    elif btnName == "Y+":
                        val = float(self.multiplier)
                        print("Y",val)
                        comm =BEECommand.Command()
                        comm.move(None,val,None,None)
                    elif btnName == "Y-":
                        val = -1 * float(self.multiplier)
                        print("Y",val)
                        comm =BEECommand.Command()
                        comm.move(None,val,None,None)
                    elif btnName == "Z+":
                        val = float(self.multiplier)
                        print("Z",val)
                        comm =BEECommand.Command()
                        comm.move(None,None,val,None)
                    elif btnName == "Z-":
                        val = -1 * float(self.multiplier)
                        print("Z",val)
                        comm =BEECommand.Command()
                        comm.move(None,None,val,None)
                        
        
        return

    """*************************************************************************
                                update Method 
    
    Updates screen components
    *************************************************************************"""
    def update(self):
        
        self.lblTop = self.lblFont.render("Jog as you like:", 1, self.lblFontColor)
        
        for btn in self.jogButtons:
            btn.visible = True

        return

    """*************************************************************************
                                draw Method 
    
    Draws current screen
    *************************************************************************""" 
    def draw(self):
        
        self.screen.blit(self.lblTop, (self.interfaceLoader.GetlblXPos(),
                                            self.interfaceLoader.GetlblYPos()))
                                            
        for btn in self.jogButtons:
            btn.draw(self.screen)
            if btn._propGetName() == str(self.multiplier):
                pygame.draw.rect(self.screen, btn._propGetFgColor(), btn._propGetRect(), 3)
        
        #pygame.draw.rect(screen, color, (x,y,width,height), thickness)
        
        return
    
    """*************************************************************************
                                GetCurrentScreenName Method 
    
    Frees every element from memmory
    *************************************************************************""" 
    def GetCurrentScreenName(self):
        
        return "Jog"
    
    """*************************************************************************
                                KillAll Method 
    
    Frees every element from memmory
    *************************************************************************""" 
    def KillAll(self):
        
        self.lblFont = None
        self.lblTop = None
        self.lblFontColor = None
        
        self.jogButtons = None
        
        self.multiplier = "1"
        self.multiplierRect = None
        
        self.interfaceLoader = None
        
        return
    
    """*************************************************************************
                                ExitCallBack Method 
    
    Tells the main class to load the default interface
    *************************************************************************""" 
    def ExitCallBack(self):
        
        return False
    
    """*************************************************************************
                                Pull Method 
    
    Pull variables
    *************************************************************************""" 
    def Pull(self):
        
        return