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

class PrinterInfoScreen():
    
    screen = None
    lblStatus = None
    lblFW = None
    lblSN = None
    lblPN = None
    printerName = None
    lblStatusVal = None
    lblFWVal = None
    lblSNVal = None
    lblPNVal = None
    
    lblFont = None
    lblValFont = None
    
    interfaceLoader = None
    
    """*************************************************************************
                                Init Method 
    
    Inits current screen components
    *************************************************************************"""
    def __init__(self, screen, interfaceLoader):
        
        self.screen = screen
        self.interfaceLoader = interfaceLoader
        self.printerName = self.interfaceLoader.GetPrinterName()
        
        print("Loading Printer Info Screen Components")
        
        self.lblFont = self.interfaceLoader.GetlblFont()
        self.lblValFont = self.interfaceLoader.GetlblValFont()
        self.lblFontColor = self.interfaceLoader.GetlblFontColor()
        self.lblValFontColor = self.interfaceLoader.GetlblValFontColor()

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
        
        self.lblStatus = self.lblFont.render("Printer Status:", 1, self.lblFontColor)
        self.lblFW = self.lblFont.render("Firmware:", 1, self.lblFontColor)
        self.lblSN = self.lblFont.render("Serial Number:", 1, self.lblFontColor)
        self.lblPN = self.lblFont.render("Printer Name:", 1, self.lblFontColor)
        
        self.lblStatusVal = self.lblValFont.render("Stand By", 1, self.lblValFontColor)
        self.lblFWVal = self.lblValFont.render("0.0.0.0", 1, self.lblValFontColor)
        self.lblSNVal = self.lblValFont.render("1.1.1.1", 1, self.lblValFontColor)
        self.lblPNVal = self.lblValFont.render(self.printerName, 1, self.lblValFontColor)

        return

    """*************************************************************************
                                draw Method 
    
    Draws current screen
    *************************************************************************""" 
    def draw(self):
        
        self.screen.blit(self.lblStatus, (self.interfaceLoader.GetlblXPos(),
                                            self.interfaceLoader.GetlblStatusY()))
        self.screen.blit(self.lblFW, (self.interfaceLoader.GetlblXPos(),
                                            self.interfaceLoader.GetlblFWY()))
        self.screen.blit(self.lblSN, (self.interfaceLoader.GetlblXPos(),
                                            self.interfaceLoader.GetlblSNY()))
        self.screen.blit(self.lblPN, (self.interfaceLoader.GetlblXPos(),
                                            self.interfaceLoader.GetlblPNY()))
                                            
        self.screen.blit(self.lblStatusVal, (self.interfaceLoader.GetlblValXPos(),
                                            self.interfaceLoader.GetlblStatusY()))
        self.screen.blit(self.lblFWVal, (self.interfaceLoader.GetlblValXPos(),
                                            self.interfaceLoader.GetlblFWY()))
        self.screen.blit(self.lblSNVal, (self.interfaceLoader.GetlblValXPos(),
                                            self.interfaceLoader.GetlblSNY()))
        self.screen.blit(self.lblPNVal, (self.interfaceLoader.GetlblValXPos(),
                                            self.interfaceLoader.GetlblPNY()))
        
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
        self.lblStatus = None
        self.lblFW = None
        self.lblSN = None
        self.lblPN = None
        self.printerName = None
        self.lblStatusVal = None
        self.lblFWVal = None
        self.lblSNVal = None
        self.lblPNVal = None
        
        self.lblFont = None
        self.lblValFont = None
        
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