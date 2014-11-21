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
import BEETFT_Button
import json

class FileBrowserLoader():
    
    interfaceJson = None
    topLblJson = []
    buttonsJson = []
    topLbltext = []
    lblsJson = []
    
    lblText = []
    lblFont = []
    lblFontColor = []
    lblXPos = []
    lblYPos = []
    lblIndexes = []
    
    lblTopFont = []
    lblTopFontColor = []
    lblTopXPos = []
    lblTopYPos = []
    
    interfaceButtons = []
    
    pickerX = None
    pickerY = None
    pickerWidth = None
    pickerHeight = None
    pickerFontSize = None
    pickerFont = None
    pickerStrlen = None
    pickerRowCount = None
    
    rpiDir = None
    usbDir = None
    
    slicingImgJson = None
    printImgJson = None
    slicingImgPath = None
    printImgPath = None
    slicingImgX = 100
    printImgX = 100
    sliceImgY = 0
    printImgY = 0
    
    """*************************************************************************
                                Init Method 
    
    Inits current screen components
    *************************************************************************"""
    def __init__(self, interfaceJson):
        
        self.interfaceJson = interfaceJson
        
        self.topLblJson.append(json.loads(json.dumps(self.interfaceJson['FirstTopLabel'])))
        self.topLblJson.append(json.loads(json.dumps(self.interfaceJson['SecondTopLabel'])))
        self.topLblJson.append(json.loads(json.dumps(self.interfaceJson['ThirdTopLabel'])))
        self.topLblJson.append(json.loads(json.dumps(self.interfaceJson['FourthTopLabel'])))
        
        self.buttonsJson.append(json.loads(json.dumps(self.interfaceJson['FirstButtons'])))
        self.buttonsJson.append(json.loads(json.dumps(self.interfaceJson['SecondButtons'])))
        self.buttonsJson.append(json.loads(json.dumps(self.interfaceJson['ThirdButtons'])))
        self.buttonsJson.append(json.loads(json.dumps(self.interfaceJson['FourthButtons'])))
        
        self.lblsJson.append(json.loads(json.dumps(self.interfaceJson['FirstLabels'])))
        self.lblIndexes.append(len(self.lblsJson[0]))
        self.lblsJson.append(json.loads(json.dumps(self.interfaceJson['SecondLabels'])))
        self.lblIndexes.append(len(self.lblsJson[1]))
        self.lblsJson.append(json.loads(json.dumps(self.interfaceJson['ThirdLabels'])))
        self.lblIndexes.append(len(self.lblsJson[2]))
        self.lblsJson.append(json.loads(json.dumps(self.interfaceJson['FourthLabels'])))
        self.lblIndexes.append(len(self.lblsJson[3]))
        
        self.slicingImgJson = json.loads(json.dumps(self.interfaceJson['SlicingImage']))
        self.printImgJson = json.loads(json.dumps(self.interfaceJson['PrintImage']))
        
        """
        Load Top Labels Configuration
        """
        for topLbl in self.topLblJson:
            topLblFontType = topLbl['FontType']
            topLblFontSize = int(topLbl['FontSize'])
            topLblFColor = topLbl['FontColor']
            self.lblTopXPos.append(int(topLbl['X']))
            self.lblTopYPos.append(int(topLbl['Y']))
            self.topLbltext.append(topLbl['Text'])
            self.lblTopFont.append(self.GetFont(topLblFontType,topLblFontSize))
            
            splitColor = topLblFColor.split(",")
            fontColor = pygame.Color(int(splitColor[0]),int(splitColor[1]),int(splitColor[2]))
            self.lblTopFontColor.append(fontColor)
        
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
        File Picker Configuration
        """
        filePickerJson = json.loads(json.dumps(self.interfaceJson['FilePicker']))
        self.pickerX = int(filePickerJson['X'])
        self.pickerY = int(filePickerJson['Y'])
        self.pickerWidth = int(filePickerJson['Width'])
        self.pickerHeight = int(filePickerJson['Height'])
        self.pickerFontSize = int(filePickerJson['FontSize'])
        self.pickerStrlen = int(filePickerJson['StringLen'])
        self.pickerRowCount = int(filePickerJson['RowCount'])
        pickerFontColorRGB = filePickerJson['FontColor']
        fontType = filePickerJson['FontType']
            
        font = self.GetFont(fontType,self.pickerFontSize)
        
        self.pickerFont = font
        
        splitColor = pickerFontColorRGB.split(",")
        self.pickerFontColor = pygame.Color(int(splitColor[0]),int(splitColor[1]),int(splitColor[2]))
        
        """
        File Picker Configuration
        """
        dirJson = json.loads(json.dumps(self.interfaceJson['FileFolders']))
        self.rpiDir = dirJson['RPI']
        self.usbDir = dirJson['USB']
        
        """
        Image Files Configuration
        """
        self.slicingImgPath = self.slicingImgJson['ImgPath']
        self.printImgPath = self.printImgJson['ImgPath']
        self.slicingImgX = int(self.slicingImgJson['X'])
        self.slicingImgY = int(self.slicingImgJson['Y'])
        self.printImgX = int(self.printImgJson['X'])
        self.printImgY = int(self.printImgJson['Y'])
        
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
    
    
    """*************************************************************************
                                BUTTONS
    *************************************************************************"""
    
    """
    GetButtonsList(self)
    
    returns the list with buttons
    """
    def GetButtonsList(self,BrowserState):
        
        return self.interfaceButtons[BrowserState]
    
    """*************************************************************************
                                TOP LABELS
    *************************************************************************"""
    """
    GetToplblText(self)
    
    returns the list with the label text
    """
    def GetToplblText(self,BrowserState):
        
        return self.topLbltext[BrowserState]
    
    """
    GetTopLblFont
    """
    def GetTopLblFont(self,BrowserState):
        return self.lblTopFont[BrowserState]
    
    """
    GetTopLblFontColor
    """
    def GetTopLblFontColor(self,BrowserState):
        return self.lblTopFontColor[BrowserState]
    
    
    """
    GetTopLblXPos
    """
    def GetTopLblXPos(self,BrowserState):
        return self.lblTopXPos[BrowserState]
    
    """
    GetTopLblYPos
    """
    def GetTopLblYPos(self,BrowserState):
        return self.lblTopYPos[BrowserState]
    
    
    """*************************************************************************
                                LABELS
    *************************************************************************"""
    
    """
    GetlblText(self)
    
    returns the list with the label text
    """
    def GetlblText(self,BrowserState):
        startIdx = 0
        for i in range(0,BrowserState):
            startIdx = startIdx + self.lblIndexes[i]
        endIdx = startIdx + self.lblIndexes[BrowserState]        
        return self.lblText[startIdx:endIdx]
    
    """
    GetlblFont
    """
    def GetlblFont(self,BrowserState):
        startIdx = 0
        for i in range(0,BrowserState):
            startIdx = startIdx + self.lblIndexes[i]
        endIdx = startIdx + self.lblIndexes[BrowserState]
        return self.lblFont[startIdx:endIdx]
    
    """
    GetlblFontColor
    """
    def GetlblFontColor(self,BrowserState):
        startIdx = 0
        for i in range(0,BrowserState):
            startIdx = startIdx + self.lblIndexes[i]
        endIdx = startIdx + self.lblIndexes[BrowserState]
        return self.lblFontColor[startIdx:endIdx]
    
    
    """
    GetlblTopXPos
    """
    def GetlblTopXPos(self,BrowserState):
        startIdx = 0
        for i in range(0,BrowserState):
            startIdx = startIdx + self.lblIndexes[i]
        endIdx = startIdx + self.lblIndexes[BrowserState]
        return self.lblXPos[startIdx:endIdx]
    
    """
    GetlblTopYPos
    """
    def GetlblTopYPos(self,BrowserState):
        startIdx = 0
        for i in range(0,BrowserState):
            startIdx = startIdx + self.lblIndexes[i]
        endIdx = startIdx + self.lblIndexes[BrowserState]
        return self.lblYPos[startIdx:endIdx]
    
    """*************************************************************************
                                FILE PICKER
    *************************************************************************"""
    
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
    GetPickerStrLen
    """
    def GetPickerStrLen(self):
        return self.pickerStrlen
    
    """
    GetPickerRowCount
    """
    def GetPickerRowCount(self):
        return self.pickerRowCount
    
    """
    GetRpiDir
    """
    def GetRpiDir(self):
        return self.rpiDir
    
    """
    GetUsbDir
    """
    def GetUsbDir(self):
        return self.usbDir
    
    """*************************************************************************
                                IMAGES
    *************************************************************************"""
    
    """
    GetSlicingImgPath
    """
    def GetSlicingImgPath(self):
        return self.slicingImgPath
    
    """
    GetPrintImgPath
    """
    def GetPrintImgPath(self):
        return self.printImgPath
    
    """
    GetSlicingImgX
    """
    def GetSlicingImgX(self):
        return self.slicingImgX
    
    """
    GetSlicingImgY
    """
    def GetSlicingImgY(self):
        return self.slicingImgY
    
    """
    GetPrintImgX
    """
    def GetPrintImgX(self):
        return self.printImgX
    
    """
    GetPrintImgY
    """
    def GetPrintImgY(self):
        return self.printImgY