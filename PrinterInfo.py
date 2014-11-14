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

class PrinterInfoScreen():
    
    screen = None
    
    lblText = None           #list for label text
    lbl = None               #label object
    lblFont = None           #label font
    lblFontColor = None      #label color
    
    lblVal = None               #label object
    lblValFont = None           #label font
    lblValFontColor = None      #label color
    
    status = None
    fw = None
    BEEConnect = None
    sn = None
    network = None
    ip = None
    
    interfaceLoader = None
    
    nextPullTime = None
    pullInterval = 1
    
    """*************************************************************************
                                Init Method 
    
    Inits current screen components
    *************************************************************************"""
    def __init__(self, screen, interfaceLoader):
        
        self.screen = screen
        self.interfaceLoader = interfaceLoader
        
        self.nextPullTime = time()
        self.Pull()
        
        print("Loading Printer Info Screen Components")
        
        """
        Load lists and settings from interfaceLoader
        """
        self.lblFont = self.interfaceLoader.GetlblFont()
        self.lblFontColor = self.interfaceLoader.GetlblFontColor()
        self.lblText = self.interfaceLoader.GetlblText()
        self.lblXPos = self.interfaceLoader.GetlblXPos()
        self.lblYPos = self.interfaceLoader.GetlblYPos()
        
        self.lblValFont = self.interfaceLoader.GetlblValFont()
        self.lblValFontColor = self.interfaceLoader.GetlblValFontColor()
        self.lblValXPos = self.interfaceLoader.GetlblValXPos()

    """*************************************************************************
                                handle_events Method 
    
    Received the event vector and checks if it has any event from interface items
    *************************************************************************"""
    def handle_events(self,retVal):
        """handle all events."""
        for event in retVal:
            pass
        
        return

    """*************************************************************************
                                update Method 
    
    Updates screen components
    *************************************************************************"""
    def update(self):
        
        self.lbl = []
        self.lblVal = []
        for i in range(0,len(self.lblText)):
            self.lbl.append(self.lblFont[i].render(self.lblText[i], 1, self.lblFontColor[i]))
            
            fieldText = self.lblText[i]
            valText = ""
            if fieldText == "Printer Status:":
                valText = self.status
                print("\nTODO: GET STATUS\n")
            elif fieldText == "Firmware:":
                valText = self.fw
                print("\nTODO: GET FW\n")
            elif fieldText == "BEEConnect:":
                valText = self.BEEConnect
                print("\nTODO: GET BEEConnect\n")
            elif fieldText == "SN:":
                valText = self.sn
                print("\nTODO: GET SN\n")
            elif fieldText == "Network:":
                valText = self.network
                print("\nTODO: GET Network\n")
            elif fieldText == "IP:":
                valText = self.ip
                print("\nTODO: GET IP\n")
            
            self.lblVal.append(self.lblValFont.render(valText, 1, self.lblValFontColor))
            
        return

    """*************************************************************************
                                draw Method 
    
    Draws current screen
    *************************************************************************""" 
    def draw(self):
        
        for i in range(0,len(self.lblText)):
            self.screen.blit(self.lbl[i],(self.lblXPos[i],self.lblYPos[i]))
            self.screen.blit(self.lblVal[i],(self.lblValXPos,self.lblYPos[i]))
        
        return
    
    """*************************************************************************
                                GetCurrentScreenName Method 
    
    Frees every element from memmory
    *************************************************************************""" 
    def GetCurrentScreenName(self):
        
        return "Printer Info"
    
    """*************************************************************************
                                KillAll Method 
    
    Frees every element from memmory
    *************************************************************************""" 
    def KillAll(self):
        
        self.screen = None
        self.lblText = None
        self.lbl = None
        self.lblFont = None
        self.lblFontColor = None
        self.lblVal = None
        self.lblValFont = None
        self.lblValFontColor = None
        self.status = None
        self.fw = None
        self.BEEConnect = None
        self.sn = None
        self.network = None
        self.ip = None
        self.interfaceLoader = None
        self.nextPullTime = None
        self.pullInterval = None
        
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
        
        t = time()
        if t > self.nextPullTime:
            self.nextPullTime = time() + self.pullInterval
            
            self.status = "StandBy"
            self.fw = "V00000"
            self.BEEConnect = "V11111"
            self.sn = "55555"
            self.network = "Lan?"
            self.ip = "0.0.0.0.0"
        
        return