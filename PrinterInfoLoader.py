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

import json

import FileFinder
import pygame

class PrinterInfoLoader():
    
    interfaceJson = None
    
    lblJson = None
    lblValJson = None
    
    lblFont = None
    lblFontColor = None
    lblXPos = None
    lblYPos = None
    lblText = None
    
    lblValFont = None
    lblValFontColor = None
    
    lblValXPos = None
    lblValFont = None
    lblValFontColor = None
    
    """*************************************************************************
                                Init Method 
    
    Inits current screen components
    *************************************************************************"""
    def __init__(self, interfaceJson):
        
        self.interfaceJson = interfaceJson
        
        
        self.lblJson = json.loads(json.dumps(self.interfaceJson['Labels']))
        self.lblValJson = json.loads(json.dumps(self.interfaceJson['ValuesSettings']))
        
        """
        Values Labels Configuration
        
        "X":"220",
                    "FontType":"Bold",
                    "FontSize":"12",
                    "FontColor":"0,0,0"
        """
        self.lblValXPos = int(self.lblValJson['X'])
        lblValFontType = self.lblValJson['FontType']
        lblValFontSize = int(self.lblValJson['FontSize'])
        self.lblValFont = self.GetFont(lblValFontType,lblValFontSize)
        lblValFColor = self.lblValJson['FontColor']
        splitColor = lblValFColor.split(",")
        self.lblValFontColor = pygame.Color(int(splitColor[0]),int(splitColor[1]),int(splitColor[2]))
        
        """
        Load Labels Configuration
        """
        self.lblText = []
        self.lblXPos = []
        self.lblYPos = []
        self.lblFont = []
        self.lblFontColor = []
        
        for lbl in self.lblJson:
            lblFontType = lbl['FontType']
            lblFontSize = int(lbl['FontSize'])
            lblFColor = lbl['FontColor']
            
            self.lblXPos.append(int(lbl['X']))
            self.lblYPos.append(int(lbl['Y']))
            self.lblText.append(lbl['Text'])
            
            font = self.GetFont(lblFontType,lblFontSize)
            
            self.lblFont.append(font)
            
            splitColor = lblFColor.split(",")
            fontColor = pygame.Color(int(splitColor[0]),int(splitColor[1]),int(splitColor[2]))
            self.lblFontColor.append(fontColor)
        
        return
    
    """
    GetFont
    """
    def GetFont(self,fontType,fontSize):
        
        ff = FileFinder.FileFinder()
        
        font = None
        if fontType == "Regular":
            font = pygame.font.Font(ff.GetAbsPath("Fonts/DejaVuSans-Regular.ttf"),fontSize)
        elif fontType == "Bold":
            font = pygame.font.Font(ff.GetAbsPath("Fonts/DejaVuSans-Bold.ttf"),fontSize)
        elif fontType == "Italic":
            font = pygame.font.Font(ff.GetAbsPath("Fonts/DejaVuSans-Italic.ttf"),fontSize)
        elif fontType == "Light":
            font = pygame.font.Font(ff.GetAbsPath("Fonts/DejaVuSans-Light.ttf"),fontSize)
            
        return font
    
    """
    GetlblText(self)
    
    returns the list with the label text
    """
    def GetlblText(self):
        return self.lblText
    
    """
    GetlblFont
    """
    def GetlblFont(self):
        return self.lblFont
    
    """
    GetlblFontColor
    """
    def GetlblFontColor(self):
        return self.lblFontColor
    
    
    """
    GetlblXPos
    """
    def GetlblXPos(self):
        return self.lblXPos
    
    """
    GetlblYPos
    """
    def GetlblYPos(self):
        return self.lblYPos
    
    """
    GetlblValFont
    """
    def GetlblValFont(self):
        return self.lblValFont
    
    """
    GetlblValFontColor
    """
    def GetlblValFontColor(self):
        return self.lblValFontColor
    
    
    """
    GetlblValXPos
    """
    def GetlblValXPos(self):
        return self.lblValXPos