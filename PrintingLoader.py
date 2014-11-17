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
import ProgressBar
import FileFinder

class PrintingLoader():
    
    interfaceJson = None
    
    interfacelabels = None
    lblsJson = None
    lblFontColor = None
    lblXPos = None
    lblYPos = None
    lblText = None
    lblFont = None 
    lblIndexes = None
    
    timeLblFontColor = None
    timeLblXPos = None
    timeLblYPos = None
    timeLblText = None
    timeLblFont = None
    
    colorLblFontColor = None
    colorLblXPos = None
    colorLblYPos = None
    colorLblText = None
    colorLblFont = None 
    
    buttonsJson = None
    interfaceButtons = None
    
    images = None
    imagesJson = None
    imagePath = None
    imageX = None
    imageY = None
    
    #Progress Bar
    progressBar = None
    
    #Color Picker
    pickerX = 0
    pickerY = 0
    pickerWidth = 0
    pickerHeight = 0
    pickerFontSize = 0
    pickerFontColorRGB = "0,0,0"
    pickerFontColor = None
    pickerFont = None
    
    """*************************************************************************
                                Init Method 
    
    Inits current screen components
    *************************************************************************"""
    def __init__(self, interfaceJson):
        
        self.interfaceJson = interfaceJson
        
        self.buttonsJson = []
        
        self.lblsJson = []
        self.lblFontColor = []
        self.lblXPos = []
        self.lblYPos = []
        self.lblText = []
        self.lblFont = []
        self.lblIndexes = []
        
        self.images = []
        self.imagesJson = []
        self.imagePath = []
        self.imageX = []
        self.imageY = []
        
        self.lblsJson.append(json.loads(json.dumps(self.interfaceJson['FirstTopLabel'])))
        self.lblIndexes.append(len(self.lblsJson[0]))
        self.lblsJson.append(json.loads(json.dumps(self.interfaceJson['SecondTopLabel'])))
        self.lblIndexes.append(len(self.lblsJson[1]))
        self.lblsJson.append(json.loads(json.dumps(self.interfaceJson['ThirdTopLabel'])))
        self.lblIndexes.append(len(self.lblsJson[2]))
        self.lblsJson.append(json.loads(json.dumps(self.interfaceJson['FourthTopLabel'])))
        self.lblIndexes.append(len(self.lblsJson[3]))
        self.lblsJson.append(json.loads(json.dumps(self.interfaceJson['FifthTopLabel'])))
        self.lblIndexes.append(len(self.lblsJson[4]))
        
        self.buttonsJson.append(json.loads(json.dumps(self.interfaceJson['FirstButtons'])))
        self.buttonsJson.append(json.loads(json.dumps(self.interfaceJson['SecondButtons'])))
        self.buttonsJson.append(json.loads(json.dumps(self.interfaceJson['ThirdButtons'])))
        self.buttonsJson.append(json.loads(json.dumps(self.interfaceJson['FourthButtons'])))
        self.buttonsJson.append(json.loads(json.dumps(self.interfaceJson['FifthButtons'])))
        
        self.imagesJson.append(json.loads(json.dumps(self.interfaceJson['FirstImage'])))
        self.imagesJson.append(json.loads(json.dumps(self.interfaceJson['SecondImage'])))
        self.imagesJson.append(json.loads(json.dumps(self.interfaceJson['ThirdImage'])))
        #self.imagesJson.append(json.loads(json.dumps(self.interfaceJson['FourthImage'])))
        
        """
        Time Label Configuration
        """
        timeLblJson = json.loads(json.dumps(self.interfaceJson['TimeLabel']))
        
        self.timeLblXPos = int(timeLblJson['X'])
        self.timeLblYPos = int(timeLblJson['Y'])
        self.timeLblText = timeLblJson['Text']
        
        self.timeLblFont = self.GetFont(timeLblJson['FontType'],int(timeLblJson['FontSize']))
        
        timeFontColor = timeLblJson['FontColor']
        splitColor = timeFontColor.split(",")
        self.timeLblFontColor = pygame.Color(int(splitColor[0]),int(splitColor[1]),int(splitColor[2]))
        
        """
        Color Label Configuration
        """
        colorLblJson = json.loads(json.dumps(self.interfaceJson['ColorLabel']))
        
        self.colorLblXPos = int(colorLblJson['X'])
        self.colorLblYPos = int(colorLblJson['Y'])
        self.colorLblText = colorLblJson['Text']
        
        self.colorLblFont = self.GetFont(colorLblJson['FontType'],int(colorLblJson['FontSize']))
        
        colorFontColor = colorLblJson['FontColor']
        splitColor = colorFontColor.split(",")
        self.colorLblFontColor = pygame.Color(int(splitColor[0]),int(splitColor[1]),int(splitColor[2]))
        
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
        Load Buttons Configuration
        """
        self.interfaceButtons = []
        for btns in self.buttonsJson:
            filButtons = []
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
                                                fType,fSize,None,None,None,btnName)
                                                
                    newBtn = jogBtn.GetTextButton()
                    newBtn._propSetName(btnTitle)
                    filButtons.append(newBtn)
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
                    filButtons.append(newBtn)
        
            self.interfaceButtons.append(filButtons)
            
        """
        Load Heating Image Configuration
        """
        for img in self.imagesJson:
            imgJson = json.loads(json.dumps(img))
            for img in imgJson:
                self.imagePath.append(img['ImgPath'])
                self.imageX.append(int(img['X']))
                self.imageY.append(int(img['Y']))
                
        
        """
        Load Progress Bar Configuration
        """
        pBarJson = json.loads(json.dumps(self.interfaceJson['ProgressBar']))
        pBarX = int(pBarJson['X'])
        pBarY = int(pBarJson['Y'])
        pBarWidth = int(pBarJson['Width'])
        pBarHeight = int(pBarJson['Height'])
        pBarThickness = int(pBarJson['Thickness'])
        pBarLineColorRGB = pBarJson['LineColor']
        pBarFillColorRGB = pBarJson['bgColor']
        
        splitColor = pBarLineColorRGB.split(",")
        pBarLineColor = pygame.Color(int(splitColor[0]),int(splitColor[1]),int(splitColor[2]))
        
        splitColor = pBarFillColorRGB.split(",")
        pBarFillColor = pygame.Color(int(splitColor[0]),int(splitColor[1]),int(splitColor[2]))
        
        self.progressBar = ProgressBar.ProgressBar(pBarX,pBarY,pBarWidth,pBarHeight,pBarLineColor,pBarFillColor,pBarThickness)
        
        """
        Color Picker Configuration
        """
        colorPickerJson = json.loads(json.dumps(self.interfaceJson['ColorPicker']))
        self.pickerX = int(colorPickerJson['X'])
        self.pickerY = int(colorPickerJson['Y'])
        self.pickerWidth = int(colorPickerJson['Width'])
        self.pickerHeight = int(colorPickerJson['Height'])
        self.pickerFontSize = int(colorPickerJson['FontSize'])
        pickerFontColorRGB = colorPickerJson['FontColor']
        fontType = colorPickerJson['FontType']
            
        font = self.GetFont(fontType,self.pickerFontSize)
        
        self.pickerFont = font
        
        splitColor = pickerFontColorRGB.split(",")
        self.pickerFontColor = pygame.Color(int(splitColor[0]),int(splitColor[1]),int(splitColor[2]))
                
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
    GetButtonsList(self)
    
    returns the list with buttons
    """
    def GetButtonsList(self,interfaceState):
        
        return self.interfaceButtons[interfaceState]
    
    """
    GetLblsText
    """
    def GetLblsText(self,interfaceState):
        return self.lblText[interfaceState]
    
    """
    GetLblsFont
    """
    def GetLblsFont(self,interfaceState):
        return self.lblFont[interfaceState]
    
    """
    GetLblsFontColor
    """
    def GetLblsFontColor(self,interfaceState):
        return self.lblFontColor[interfaceState]
    
    """
    GetLblsXPos
    """
    def GetLblsXPos(self,interfaceState):
        return self.lblXPos[interfaceState]
    
    """
    GetLblsYPos
    """
    def GetLblsYPos(self,interfaceState):
        return self.lblYPos[interfaceState]
    
    """
    GetTimeLblText
    """
    def GetTimeLblText(self,interfaceState):
        if interfaceState == 0:
            return self.timeLblText
    
    """
    GetTimeLblFont
    """
    def GetTimeLblFont(self,interfaceState):
        if interfaceState == 0:
            return self.timeLblFont
    
    """
    GetTimeLblFontColor
    """
    def GetTimeLblFontColor(self,interfaceState):
        if interfaceState == 0:
            return self.timeLblFontColor
    
    """
    GetTimeLblXPos
    """
    def GetTimeLblXPos(self,interfaceState):
        if interfaceState == 0:
            return self.timeLblXPos
    
    """
    GetTimeLblYPos
    """
    def GetTimeLblYPos(self,interfaceState):
        if interfaceState == 0:
            return self.timeLblYPos
    
    """
    GetColorLblText
    """
    def GetColorLblText(self,interfaceState):
        if interfaceState == 3:
            return self.colorLblText
    
    """
    GetColorLblFont
    """
    def GetColorLblFont(self,interfaceState):
        if interfaceState == 3:
            return self.colorLblFont
    
    """
    GetColorLblFontColor
    """
    def GetColorLblFontColor(self,interfaceState):
        if interfaceState == 3:
            return self.colorLblFontColor
    
    """
    GetColorLblXPos
    """
    def GetColorLblXPos(self,interfaceState):
        if interfaceState == 3:
            return self.colorLblXPos
    
    """
    GetColorLblYPos
    """
    def GetColorLblYPos(self,interfaceState):
        if interfaceState == 3:
            return self.colorLblYPos
    
    """
    GetImagePath
    """
    def GetImagePath(self,interfaceState):
        if interfaceState >= len(self.imagePath):
            return []
        return self.imagePath[interfaceState]
    
    """
    GetImageX
    """
    def GetImageX(self,interfaceState):
        if interfaceState >= len(self.imagePath):
            return []
        return self.imageX[interfaceState]
    
    """
    GetImageY
    """
    def GetImageY(self,interfaceState):
        if interfaceState >= len(self.imagePath):
            return []
        return self.imageY[interfaceState]
    
    """
    GetProgessBar
    """
    def GetProgessBar(self,interfaceState):
        if interfaceState == 0:
            return self.progressBar 
        else:
            return
    
    """
    GetPickerX
    """
    def GetPickerX(self):
        return self.pickerX
    
    """
    GetPickerY
    """
    def GetPickerY(self):
        return self.pickerY
    
    """
    GetPickerWidth
    """
    def GetPickerWidth(self):
        return self.pickerWidth
    
    """
    GetPickerHeight
    """
    def GetPickerHeight(self):
        return self.pickerHeight
    
    """
    GetPickerFontSize
    """
    def GetPickerFontSize(self):
        return self.pickerFontSize
    
    """
    GetPickerFontColor
    """
    def GetPickerFontColor(self):
        return self.pickerFontColor
    
    """
    GetPickerFont
    """
    def GetPickerFont(self):
        return self.pickerFont
        
        