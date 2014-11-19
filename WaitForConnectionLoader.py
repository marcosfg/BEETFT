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

class WaitForConnectionLoader():
    
    jsonPath = "WaitForConnectionConfiguration.json"
    
    interfaceJson = None
    
    lblsJson = None
    lblFontColor = None
    lblXPos = None
    lblYPos = None
    lblText = None
    lblFont = None
    
    imgJson = None
    imagePath = None
    imageX = None
    imageY = None
    
    """*************************************************************************
                                Init Method 
    
    Inits current screen components
    *************************************************************************"""
    def __init__(self):
        
        ff = FileFinder.FileFinder()
        
        """
        Get wait screen Configuration
        """
        f = open(ff.GetAbsPath(self.jsonPath),'r')                          #load json as text file
        self.interfaceJson = json.load(f)                                     #parse the json file
        
        self.wait4connectionJson = self.interfaceJson['WaitForConnection'][0]
        
        self.lblsJson = []
        self.lblFontColor = []
        self.lblXPos = []
        self.lblYPos = []
        self.lblText = []
        self.lblFont = []
        
        self.lblsJson.append(json.loads(json.dumps(self.wait4connectionJson['Labels'])))
        self.imgJson = json.loads(json.dumps(self.wait4connectionJson['Image']))
        
        """
        Load Labels Configuration
        """
        for lbls in self.lblsJson:
            lblJson = json.loads(json.dumps(lbls))
            for lbl in lblJson:
                lblFontType = lbl['FontType']
                lblFontSize = int(lbl['FontSize'])
                lblFColor = lbl['FontColor']
                self.lblXPos.append(int(lbl['X']))
                self.lblYPos.append(int(lbl['Y']))
                self.lblText.append(lbl['Text'])
                self.lblFont.append(self.GetFont(lblFontType,lblFontSize))
                
                splitColor = lblFColor.split(",")
                fontColor = pygame.Color(int(splitColor[0]),int(splitColor[1]),int(splitColor[2]))
                self.lblFontColor.append(fontColor)
        
        """
        Loade Image Configurtation
        """
        self.imagePath = ff.GetAbsPath(self.imgJson['ImgPath'])
        self.imageX = int(self.imgJson['X'])
        self.imageY = int(self.imgJson['Y'])
        
        f.close()
        
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
    GetLblsText
    """
    def GetLblsText(self):
        return self.lblText
    
    """
    GetLblsFont
    """
    def GetLblsFont(self):
        return self.lblFont
    
    """
    GetLblsFontColor
    """
    def GetLblsFontColor(self):
        return self.lblFontColor
    
    """
    GetLblsXPos
    """
    def GetLblsXPos(self):
        return self.lblXPos
    
    """
    GetLblsYPos
    """
    def GetLblsYPos(self):
        return self.lblYPos
    
    """
    GetImagePath
    """
    def GetImagePath(self):
        return self.imagePath    
    """
    GetImageX
    """
    def GetImageX(self):
        return self.imageX
    
    """
    GetImageY
    """
    def GetImageY(self):
        return self.imageY