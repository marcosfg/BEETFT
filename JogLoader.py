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
import json
import BEETFT_Button

class JogLoader():
    
    interfaceJson = None
    lblJson = None
    ButtonsJson = None
    
    lblFont = None
    lblFontColor = None
    lblXPos = None
    lblYPos = None
    
    interfaceButtons = []
    
    """*************************************************************************
                                Init Method 
    
    Inits current screen components
    *************************************************************************"""
    def __init__(self, interfaceJson):
        
        self.interfaceJson = interfaceJson
        self.lblJson = json.loads(json.dumps(self.interfaceJson['TopLabel']))
        self.ButtonsJson = json.loads(json.dumps(self.interfaceJson['Buttons']))
        
        lblFontType = self.lblJson['FontType']
        lblFontSize = int(self.lblJson['FontSize'])
        lblFColor = self.lblJson['lblFontColor']
        self.lblXPos = int(self.lblJson['X'])
        self.lblYPos = int(self.lblJson['Y'])
        
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
        
        
        for btn in self.ButtonsJson:
            btnX = int(btn['X'])
            btnY = int(btn['Y'])
            btnWidth = int(btn['Width'])
            btnHeight = int(btn['Height'])
            btnType = btn['ButtonType']
            
            if btnType == "Text":
                btnTitle = btn['Title']
                bgColor = btn['bgColor'].split(",")
                fColor = btn['FontColor'].split(",")
                fType = btn['FontType']
                fSize = int(btn['FontSize'])
                btnName = btn['ButtonName']
                
                jogBtn = BEETFT_Button.Button(btnX,btnY,btnWidth,btnHeight,btnTitle,
                                                int(bgColor[0]),int(bgColor[2]),int(bgColor[2]),
                                                int(fColor[0]),int(fColor[2]),int(fColor[2]),
                                                fType,fSize, None, None, None, btnName)
                newBtn = jogBtn.GetTextButton()
                newBtn._propSetName(btnTitle)
                self.interfaceButtons.append(newBtn)
            elif btnType == "Img":
                btnTitle = btn['Title']
                normalPath = btn['NormalPath']
                downPath = btn['DownPath']
                highlightedPath = btn['HighlightedPath']
                btnName = btn['ButtonName']
                
                jogBtn = BEETFT_Button.Button(btnX,btnY,btnWidth,btnHeight,None,
                                                None,None,None,None,None,None,
                                                None,None,
                                                normalPath,downPath,highlightedPath,
                                                btnName)
                newBtn = jogBtn.GetImageButton()
                newBtn._propSetName(btnTitle)
                self.interfaceButtons.append(newBtn)
                
        return
    
    """
    GetLeftButtonsList(self)
    
    returns the list with the jog buttons
    """
    def GetLeftButtonsList(self):
        
        return self.interfaceButtons
    
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
    