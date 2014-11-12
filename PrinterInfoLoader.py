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

class PrinterInfoLoader():
    
    lblFont = None
    lblFontColor = None
    lblValFont = None
    lblValFontColor = None
    printerName = None
    
    lblXPos = 110
    lblValXPos = 210
    lblStatusY = 20
    lblFWY = 50
    lblSNY = 80
    lblPN = 110
    
    """*************************************************************************
                                Init Method 
    
    Inits current screen components
    *************************************************************************"""
    def __init__(self, interfaceJson):
        
        lblFontType = interfaceJson['lblFontType']
        lblFontSize = int(interfaceJson['lblSize'])
        lblFColor = interfaceJson['lblFontColor']
        lblValFontType = interfaceJson['lblValFontType']
        lblValFontSize = int(interfaceJson['lblValSize'])
        lblValFColor = interfaceJson['lblValFontColor']
        self.printerName = interfaceJson['PrinterName']
        self.lblXPos = int(interfaceJson['lbl_X'])
        self.lblValXPos = int(interfaceJson['lblVal_X'])
        self.lblStatusY = int(interfaceJson['lblStatus_Y'])
        self.lblFWY = int(interfaceJson['lblFW_Y'])
        self.lblSNY = int(interfaceJson['lblSN_Y'])
        self.lblPNY = int(interfaceJson['lblPN_Y'])
        
        if lblFontType == "Regular":
            self.lblFont = pygame.font.Font("Fonts/DejaVuSans-Regular.ttf",lblFontSize)
        elif lblFontType == "Bold":
            self.lblFont = pygame.font.Font("Fonts/DejaVuSans-Bold.ttf",lblFontSize)
        elif lblFontType == "Italic":
            self.lblFont = pygame.font.Font("Fonts/DejaVuSans-Italic.ttf",lblFontSize)
        elif lblFontType == "Light":
            self.lblFont = pygame.font.Font("Fonts/DejaVuSans-Light.ttf",lblFontSize)
        
        splitColor = lblFColor.split(",")
        self.lblFontColor = pygame.Color(int(splitColor[0]),int(splitColor[1]),int(splitColor[2]))
            
        if lblValFontType == "Regular":
            self.lblValFont = pygame.font.Font("Fonts/DejaVuSans-Regular.ttf",lblValFontSize)
        elif lblValFontType == "Bold":
            self.lblValFont = pygame.font.Font("Fonts/DejaVuSans-Bold.ttf",lblValFontSize)
        elif lblValFontType == "Italic":
            self.lblValFont = pygame.font.Font("Fonts/DejaVuSans-Italic.ttf",lblValFontSize)
        elif lblValFontType == "Light":
            self.lblValFont = pygame.font.Font("Fonts/DejaVuSans-Light.ttf",lblValFontSize)
        
        splitColor = lblValFColor.split(",")
        self.lblValFontColor = pygame.Color(int(splitColor[0]),int(splitColor[1]),int(splitColor[2]))
        
        return
    
    """
    GetlblFont
    """
    def GetlblFont(self):
        return self.lblFont
    
    """
    GetlblValFont
    """
    def GetlblValFont(self):
        return self.lblValFont
    
    """
    GetlblFontColor
    """
    def GetlblFontColor(self):
        return self.lblFontColor
    
    """
    GetlblValFontColor
    """
    def GetlblValFontColor(self):
        return self.lblValFontColor
    
    """
    GetlblXPos
    """
    def GetlblXPos(self):
        return self.lblXPos
    
    """
    GetlblValXPos
    """
    def GetlblValXPos(self):
        return self.lblValXPos
    
    """
    GetlblStatusY
    """
    def GetlblStatusY(self):
        return self.lblStatusY
    
    """
    GetlblFWY
    """
    def GetlblFWY(self):
        return self.lblFWY
    
    """
    GetlblSNY
    """
    def GetlblSNY(self):
        return self.lblSNY
    
    """
    GetlblPNY
    """
    def GetlblPNY(self):
        return self.lblPNY
    
    """
    GetPrinterName
    """
    def GetPrinterName(self):
        return self.printerName