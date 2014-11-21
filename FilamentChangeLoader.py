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

class FilamentChangeLoader():
    
    interfaceJson = None
    topLblJson = []
    buttonsJson = []
    lbltext = []
    
    lblTopFont = []
    lblTopFontColor = []
    lblTopXPos = []
    lblTopYPos = []
    
    interfaceButtons = []
    
    imagePath = None
    imageX = 100
    imageY = 0
    
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
        
        self.topLblJson.append(json.loads(json.dumps(self.interfaceJson['FirstTopLabel'])))
        self.topLblJson.append(json.loads(json.dumps(self.interfaceJson['SecondTopLabel'])))
        self.topLblJson.append(json.loads(json.dumps(self.interfaceJson['ThirdTopLabel'])))
        
        self.buttonsJson.append(json.loads(json.dumps(self.interfaceJson['FirstButtons'])))
        self.buttonsJson.append(json.loads(json.dumps(self.interfaceJson['SecondButtons'])))
        self.buttonsJson.append(json.loads(json.dumps(self.interfaceJson['ThirdButtons'])))
        
        """
        Load Top Labels Configuration
        """
        for lbl in self.topLblJson:
            lblFontType = lbl['FontType']
            lblFontSize = int(lbl['FontSize'])
            lblFColor = lbl['lblFontColor']
            self.lblTopXPos.append(int(lbl['X']))
            self.lblTopYPos.append(int(lbl['Y']))
            self.lbltext.append(lbl['Text'])
            
            font = self.GetFont(lblFontType,lblFontSize)
            
            self.lblTopFont.append(font)
            
            splitColor = lblFColor.split(",")
            fontColor = pygame.Color(int(splitColor[0]),int(splitColor[1]),int(splitColor[2]))
            self.lblTopFontColor.append(fontColor)
        
        """
        Load Buttons Configuration
        """
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
                                                fType,fSize, None, None, None, btnName)
                    newBtn = jogBtn.GetTextButton()
                    newBtn._propSetName(btnTitle)
                    filButtons.append(newBtn)
                elif btnType == "Img":
                    btnTitle = btn['Title']
                    normalPath = btn['NormalPath']
                    downPath = btn['DownPath']
                    highlightedPath = btn['HighlightedPath']
                    btnName = btn['ButtonName']
                
                    jogBtn = BEETFT_Button.Button(btnX,btnY,btnWidth,btnHeight,btnTitle,
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
        imageJson = json.loads(json.dumps(self.interfaceJson['FirstImage']))
        self.imagePath = imageJson['ImgPath']
        self.imageX = int(imageJson['X'])
        self.imageY = int(imageJson['Y'])
        
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
        
        
        
        """
        Selected Color Label Configuration
        """
        colorLblJson = json.loads(json.dumps(self.interfaceJson['SelectedColorLbl']))
        lblFontType = colorLblJson['FontType']
        lblFontSize = int(colorLblJson['FontSize'])
        lblFColor = colorLblJson['FontColor']
        self.selectedLblX = int(colorLblJson['X'])
        self.selectedLblY = int(colorLblJson['Y'])
            
        splitColor = lblFColor.split(",")
        self.selectedLblFontColor = pygame.Color(int(splitColor[0]),int(splitColor[1]),int(splitColor[2]))
        self.selectedLblFont = self.GetFont(lblFontType,lblFontSize)
            
        return
    
    """
    GetFont
    """
    def GetFont(self,fontType,fontSize):
        font = None
        if fontType == "Regular":
            font = pygame.font.Font("Fonts/DejaVuSans-Regular.ttf",fontSize)
        elif fontType == "Bold":
            font = pygame.font.Font("Fonts/DejaVuSans-Bold.ttf",fontSize)
        elif fontType == "Italic":
            font = pygame.font.Font("Fonts/DejaVuSans-Italic.ttf",fontSize)
        elif fontType == "Light":
            font = pygame.font.Font("Fonts/DejaVuSans-Light.ttf",fontSize)
            
        return font
    
    """
    GetButtonsList(self)
    
    returns the list with buttons
    """
    def GetButtonsList(self,calibrationState):
        
        return self.interfaceButtons[calibrationState]
    
    """
    GetlblText(self)
    
    returns the list with the label text
    """
    def GetlblText(self,calibrationState):
        
        return self.lbltext[calibrationState]
    
    """
    GetlblFont
    """
    def GetlblFont(self,calibrationState):
        return self.lblTopFont[calibrationState]
    
    """
    GetlblFontColor
    """
    def GetlblFontColor(self,calibrationState):
        return self.lblTopFontColor[calibrationState]
    
    
    """
    GetlblTopXPos
    """
    def GetlblTopXPos(self,calibrationState):
        return self.lblTopXPos[calibrationState]
    
    """
    GetlblTopYPos
    """
    def GetlblTopYPos(self,calibrationState):
        return self.lblTopYPos[calibrationState]
    
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
    
    """
    GetProgessBar
    """
    def GetProgessBar(self):
        return self.progressBar
    
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
    
    """
    GetSelectedLblFont
    """
    def GetSelectedLblFont(self):
        return self.selectedLblFont
    
    """
    GetSelectedLblFontColor
    """
    def GetSelectedLblFontColor(self):
        return self.selectedLblFontColor
    
    """
    GetSelectedLblX
    """
    def GetSelectedLblX(self):
        return self.selectedLblX
    
    """
    GetSelectedLblY
    """
    def GetSelectedLblY(self):
        return self.selectedLblY