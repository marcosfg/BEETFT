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
import BEETFT_Button
import FileFinder
import pygame

class LeftMenuLoader():
    
    interfaceButtonsData = None
    carouselButtons = None
    
    carouselItems = None
    carouselX = None
    carouselY = None
    carouselWidth = None
    carouselHeight = None
    carouselButtonHeight = None
    
    buttonNames = None
    buttonTitles = None
    bgColor = None
    font = None
    fontType = None
    fontSize = None
    fontColor = None
    bgR = None
    bgG = None
    bgB = None
    fR = None
    fG = None
    Fb = None
    
    
    """*************************************************************************
                                Init Method 
    
    Inits current screen components
    *************************************************************************"""
    def __init__(self, jsonData):
        
        
        carouselJson = json.loads(json.dumps(jsonData['Carousel']))[0]
        carouselButtonsJson = carouselJson['Buttons']
        carouselConfigJson = carouselJson['Configuration']
        
        """
        Carousel Config
        """
        self.carouselItems = int(carouselConfigJson['CarouselItems'])
        self.carouselX = int(carouselConfigJson['X'])
        self.carouselY = int(carouselConfigJson['Y'])
        self.carouselWidth = int(carouselConfigJson['Width'])
        self.carouselHeight = int(carouselConfigJson['Height'])
        self.carouselButtonHeight = int(carouselConfigJson['ButtonHeight'])
        
        bgColor = carouselConfigJson['bgColor']
        splitColor = bgColor.split(",")
        self.bgR = int(splitColor[0])
        self.bgG = int(splitColor[1])
        self.bgB = int(splitColor[2])
        self.bgColor = pygame.Color(self.bgR,self.bgG,self.bgB)
        
        self.fontType = carouselConfigJson['FontType']
        self.fontSize = int(carouselConfigJson['FontSize'])
        self.font = self.GetFont(self.fontType,self.fontSize)
        
        fColor = carouselConfigJson['FontColor']
        splitColor = fColor.split(",")
        self.fR = int(splitColor[0])
        self.fG = int(splitColor[1])
        self.fB = int(splitColor[2])
        self.fontColor = pygame.Color(self.fR,self.fG,self.fB)
        
        self.carouselButtons = []
        for btn in carouselButtonsJson:
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
                self.carouselButtons.append(newBtn)
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
                self.carouselButtons.append(newBtn)
            
            
        leftButtons = jsonData['leftMenuButtons']
        self.buttonNames = []
        self.buttonTitles = []
        for btn in leftButtons:
            btnJson = json.loads(json.dumps(btn))
            title = btnJson['Title']
            btnName = btn['ButtonName']
            self.buttonNames.append(btnName)
            self.buttonTitles.append(title)
        
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
    GetCarouselButtons(self)
    
    
    """
    def GetCarouselButtons(self):
        
        return self.carouselButtons
    
    """
    GetCarouselItems(self)
    
    
    """
    def GetCarouselItems(self):
        
        return self.carouselItems
    
    """
    GetCarouselX(self)
    
    
    """
    def GetCarouselX(self):
        
        return self.carouselX
    
    """
    GetCarouselY(self)
    
    
    """
    def GetCarouselY(self):
        
        return self.carouselY
    
    """
    GetCarouselWidth(self)
    
    
    """
    def GetCarouselWidth(self):
        
        return self.carouselWidth
    
    """
    GetCarouselHeight(self)
    
    
    """
    def GetCarouselHeight(self):
        
        return self.carouselHeight
    
    """
    GetCarouselButtonHeight(self)
    
    
    """
    def GetCarouselButtonHeight(self):
        
        return self.carouselButtonHeight
    
    """
    GetCarouselButtonNames(self)
    
    
    """
    def GetCarouselButtonNames(self):
        
        return self.buttonNames
    
    """
    GetCarouselButtonTitles(self)
    
    
    """
    def GetCarouselButtonTitles(self):
        
        return self.buttonTitles
    
    """
    GetCarouselBgColor(self)
    
    
    """
    def GetCarouselBgColor(self):
        
        return self.bgColor
    
    """
    GetCarouselFontColor(self)
    
    
    """
    def GetCarouselFontColor(self):
        
        return self.fontColor
    
    """
    GetCarouselFont(self)
    
    
    """
    def GetCarouselFont(self):
        
        return self.font
    
    """
    GetCarouselFontType(self)
    
    
    """
    def GetCarouselFontType(self):
        
        return self.fontType
    
    """
    GetCarouselFontSize(self)
    
    
    """
    def GetCarouselFontSize(self):
        
        return self.fontSize
    
    """
    Individual Color Codes
    
    
    """
    def GetBgR(self):
        return self.bgR
    def GetBgG(self):
        return self.bgG
    def GetBgB(self):
        return self.bgB
    
    def GetFR(self):
        return self.fR
    def GetFG(self):
        return self.fG
    def GetFB(self):
        return self.fB