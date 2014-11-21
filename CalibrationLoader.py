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

class CalibrationLoader():
    
    interfaceJson = None
    lblJson = []
    buttonsJson = []
    
    lblFont = []
    lblFontColor = []
    lblXPos = []
    lblYPos = []
    
    interfaceButtons = []
    
    leftImgJson = None
    rightImgJson = None
    leftImgPath = None
    rightImgPath = None
    leftImgX = 100
    rightImgX = 100
    sliceImgY = 0
    rightImgY = 0
    
    """*************************************************************************
                                Init Method 
    
    Inits current screen components
    *************************************************************************"""
    def __init__(self, interfaceJson):
        
        self.interfaceJson = interfaceJson
        
        self.lblJson.append(json.loads(json.dumps(self.interfaceJson['FirstLabel'])))
        self.lblJson.append(json.loads(json.dumps(self.interfaceJson['SecondLabel'])))
        self.lblJson.append(json.loads(json.dumps(self.interfaceJson['ThirdLabel'])))
        
        self.buttonsJson.append(json.loads(json.dumps(self.interfaceJson['FirstButtons'])))
        self.buttonsJson.append(json.loads(json.dumps(self.interfaceJson['SecondButtons'])))
        self.buttonsJson.append(json.loads(json.dumps(self.interfaceJson['ThirdButtons'])))
        
        self.leftImgJson = json.loads(json.dumps(self.interfaceJson['LeftBoltImg']))[0]
        self.rightImgJson = json.loads(json.dumps(self.interfaceJson['RightBoltImg']))[0]
        
        
        for lbl in self.lblJson:
            lblFontType = lbl['FontType']
            lblFontSize = int(lbl['FontSize'])
            lblFColor = lbl['lblFontColor']
            self.lblXPos.append(int(lbl['X']))
            self.lblYPos.append(int(lbl['Y']))
            
            font = None
            
            if lblFontType == "Regular":
                font = pygame.font.Font("Fonts/DejaVuSans-Regular.ttf",lblFontSize)
            elif lblFontType == "Bold":
                font = pygame.font.Font("Fonts/DejaVuSans-Bold.ttf",lblFontSize)
            elif lblFontType == "Italic":
                font = pygame.font.Font("Fonts/DejaVuSans-Italic.ttf",lblFontSize)
            elif lblFontType == "Light":
                font = pygame.font.Font("Fonts/DejaVuSans-Light.ttf",lblFontSize)
            
            self.lblFont.append(font)
            
            splitColor = lblFColor.split(",")
            fontColor = pygame.Color(int(splitColor[0]),int(splitColor[1]),int(splitColor[2]))
            self.lblFontColor.append(fontColor)
            
        for btns in self.buttonsJson:
            calButtons = []
            for btn in btns:
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
                    calButtons.append(newBtn)
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
                    calButtons.append(newBtn)
        
            self.interfaceButtons.append(calButtons)
            
        """
        Image Files Configuration
        """
        self.leftImgPath = self.leftImgJson['ImgPath']
        self.rightImgPath = self.rightImgJson['ImgPath']
        self.leftImgX = int(self.leftImgJson['X'])
        self.leftImgY = int(self.leftImgJson['Y'])
        self.rightImgX = int(self.rightImgJson['X'])
        self.rightImgY = int(self.rightImgJson['Y'])
            
        return
    
    """
    GetLeftButtonsList(self)
    
    returns the list with the jog buttons
    """
    def GetLeftButtonsList(self,calibrationState):
        
        return self.interfaceButtons[calibrationState]
    
    """
    GetlblFont
    """
    def GetlblFont(self,calibrationState):
        return self.lblFont[calibrationState]
    
    """
    GetlblFontColor
    """
    def GetlblFontColor(self,calibrationState):
        return self.lblFontColor[calibrationState]
    
    
    """
    GetlblXPos
    """
    def GetlblXPos(self,calibrationState):
        return self.lblXPos[calibrationState]
    
    """
    GetlblYPos
    """
    def GetlblYPos(self,calibrationState):
        return self.lblYPos[calibrationState]
    
    """*************************************************************************
                                IMAGES
    *************************************************************************"""
    
    """
    GetLeftImgPath
    """
    def GetLeftImgPath(self):
        return self.leftImgPath
    
    """
    GetRightImgPath
    """
    def GetRightImgPath(self):
        return self.rightImgPath
    
    """
    GetLeftImgX
    """
    def GetLeftImgX(self):
        return self.leftImgX
    
    """
    GetLeftImgY
    """
    def GetLeftImgY(self):
        return self.leftImgY
    
    """
    GetRightImgX
    """
    def GetRightImgX(self):
        return self.rightImgX
    
    """
    GetRightImgY
    """
    def GetRightImgY(self):
        return self.rightImgY