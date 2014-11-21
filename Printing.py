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
from time import time
import ColorCodesLoader

class PrintScreen():
    
    screen = None
    interfaceLoader = None
    printing = None
    exit = None
    
    lblFontColor = None
    lblXPos = None
    lblYPos = None
    lblText = None
    lblFont = None
    lbl = None
    
    timeLbl = None
    timeLblFontColor = None
    timeLblXPos = None
    timeLblYPos = None
    timeLblText = None
    timeLblFont = None
    
    colorLbl = None
    colorLblFontColor = None
    colorLblXPos = None
    colorLblYPos = None
    colorLblText = None
    colorLblFont = None
    
    buttons = None
    
    interfaceState = None
    
    image = None
    imageX = None
    imageY = None
    
    timeRemaining = None
    printPercent = None
    
    nextPullTime = None
    pullInterval = 1
    
    """
    Progress Bar vars
    """
    progressBar = None
    pBarRect = None
    pBarFill = None
    
    """
    Color Picker vars
    """
    pickColorRect = None        #Rect for selected color
    colorCodes = None
    colorNameList = None
    colorCodeList = None
    colorList = None
    listPosition = 0
    selectedColoridx = 0
    
    
    """*************************************************************************
                                Init Method 
    
    Inits current screen components
    *************************************************************************"""
    def __init__(self, screen, interfaceLoader, display):
        """
        .
        """
        print("loading Print Screen")
        
        self.screen = screen
        self.interfaceLoader = interfaceLoader
        self.printing = True
        self.exit = False
        self.interfaceState = 0
        self.printPercent = float(0)
        
        self.nextPullTime = time()
        self.Pull()
        
        self.BEEDisplay = display
        
        self.updateReady = False
        
        self.UpdateVars()
        
        """
        Load Colors
        """
        self.colorCodes = ColorCodesLoader.ColorCodes()
        self.colorNameList = self.colorCodes.GetColorNameList()
        self.colorCodeList = self.colorCodes.GetColorCodeList()
        self.colorList = self.colorCodes.GetColorList()
        
        
        self.start()
        
        return
    
    """*************************************************************************
                                start Method 
    
    Infinite Loop while printing state
    *************************************************************************"""
    def start(self):
        
        while (self.printing) and (not self.exit):
            # Handle events
            self.handle_events()
            
            # Update buttons visibility, text, graphs etc
            self.update()

            # Draw everything
            self.draw()
            
            #Pull Variable
            self.Pull()
            
        return
        
        return
    

    """*************************************************************************
                                handle_events Method 
    
    Received the event vector and checks if it has any event from interface items
    *************************************************************************"""
    def handle_events(self):
        
        retVal = pygame.event.get()
        """handle all events."""
        for event in retVal:
            if event.type == pygame.QUIT:
                self.exit = True
                
            if event.type == pygame.MOUSEBUTTONDOWN:
            	self.GetSelectedIdx(event)

            for btn in self.buttons:
                if 'click' in btn.handleEvent(event):
                    btnName = btn._propGetName()
                    
                    if btnName == "Cancel":
                        print("\n//TODO: SEND CANCEL PRINT\n")
                        self.exit = True
                    elif btnName == "Resume":
                        self.interfaceState = 0
                        print("\n//TODO: SEND RESUME PRINT\n")
                    elif btnName == "Pause":
                        self.interfaceState = 1
                        print("\n//TODO: SEND PAUSE PRINT\n")
                    elif btnName == "ShutDown":
                        self.interfaceState = 2
                        print("\n//TODO: SEND SHUTDOWN\n")
                    elif btnName == "Close":
                        print("\n//TODO: SEND CLOSE COMMAND\n")
                        self.exit = True
                    elif btnName == "Change Filament":
                        self.interfaceState = 3
                        print("\n//TODO: VERIFY ReadyToLoad?\n")
                    elif btnName == "Load":
                        print("\n//TODO: LOAD FILAMENT \n")
                    elif btnName == "Unload":
                        print("\n//TODO: UNLOAD FILAMENT \n")
                    elif btnName == "Color":
                        self.interfaceState = 4
                    elif btnName == "Up":
                        self.listPosition = self.listPosition - 1
                    elif btnName == "Down":
                        self.listPosition = self.listPosition + 1
                    elif btnName == "Next":
                        self.selectedColoridx = (2+self.listPosition) % len(self.colorList)
                        self.interfaceState = 3
                        print("\n//TODO: SEND COLOR CODE: ", self.colorCodeList[self.selectedColoridx],"\n")
                
                self.UpdateVars()
        
        return

    """*************************************************************************
                                update Method 
    
    Updates screen components
    *************************************************************************"""
    def update(self):
        
        #Update Top label
        self.lbl = self.lblFont.render(self.lblText, 1, self.lblFontColor)
        
        #Update Time Label
        if self.interfaceState == 0:
            str = self.timeLblText + self.timeRemaining
            self.timeLbl = self.timeLblFont.render(str, 1, self.timeLblFontColor)
        #Update Color Label
        elif self.interfaceState == 3:
            str = self.colorLblText + self.colorNameList[self.selectedColoridx]
            self.colorLbl = self.colorLblFont.render(str, 1, self.colorLblFontColor)
        
        
        for btn in self.buttons:
            if btn._propGetName() == "Update":
                btn.visible = self.updateReady
            else:
                btn.visible = True
        
        return

    """*************************************************************************
                                draw Method 
    
    Draws current screen
    *************************************************************************""" 
    def draw(self):        
        #clear whole screen
        self.screen.fill(self.BEEDisplay.GetbgColor())
        
        #Draw Top label
        self.screen.blit(self.lbl, (self.lblXPos,self.lblYPos))
        
        #Draw Time label
        if self.interfaceState == 0:
            self.screen.blit(self.timeLbl, (self.timeLblXPos,self.timeLblYPos))
            
            # Draw Progress Bar
            self.progressBar.DrawRect(self.screen)
            self.screen.blit(self.progressBar.GetSurface(self.printPercent),
                                self.progressBar.GetPos())
        #Draw Time label
        elif self.interfaceState == 3:
            self.screen.blit(self.colorLbl, (self.colorLblXPos,self.colorLblYPos))
            
        elif self.interfaceState == 4:
            x = self.interfaceLoader.GetPickerX()
            y = self.interfaceLoader.GetPickerY()
            width = self.interfaceLoader.GetPickerWidth()
            height = self.interfaceLoader.GetPickerHeight()
            pickerColor = self.interfaceLoader.GetPickerFontColor()
            fontSize = self.interfaceLoader.GetPickerFontSize()
            pickerFont = self.interfaceLoader.GetPickerFont()
            lblOffset = int((height-fontSize)/2)
            
            for i in range(0, 5):
                pos = i + self.listPosition
                
                idx = pos % len(self.colorList)   
                
                colorSurf = pygame.Surface((height*0.8,height*0.8))
                colorSurf.fill(self.colorList[idx])
                self.screen.blit(colorSurf, (x+(int(0.1*height)),y+((-2+i)*height)+(int(0.1*height))))
                
                colorLbl = None
                if i == 2:
                    colorLbl = pickerFont.render(self.colorNameList[idx], 1, pickerColor)
                else:
                    font = pygame.font.Font("Fonts/DejaVuSans-Light.ttf",fontSize)
                    colorLbl = font.render(self.colorNameList[idx], 1, pickerColor)
                    
                self.screen.blit(colorLbl, (x + height +5,y+lblOffset+((-2+i)*height)))
                
                if i>0 and i<5:
                    pygame.draw.line(self.screen, pickerColor, (x, y+((-2+i)*height)),
                                (x+width, y+((-2+i)*height)), int(0.05*height))
            
            
            self.pickColorRect = pygame.draw.rect(self.screen, pickerColor, (x,y,width,height), 3)
        
        
        #Draw Image
        if (self.interfaceState != 3) and (self.interfaceState != 4):
            self.screen.blit(self.image,(self.imageX,self.imageY))
        
        for btn in self.buttons:
            btn.draw(self.screen)
        
        
        
        # update screen
        pygame.display.update()
        
        return
    
    """*************************************************************************
                                GetCurrentScreenName Method 
    
    Frees every element from memmory
    *************************************************************************""" 
    def GetCurrentScreenName(self):
        
        return "Printing"
    
    """*************************************************************************
                                KillAll Method 
    
    Frees every element from memmory
    *************************************************************************""" 
    def KillAll(self):
        
        self.screen = None
        self.interfaceLoader = None
        self.printing = None
        self.exit = None
        self.lblFontColor = None
        self.lblXPos = None
        self.lblYPos = None
        self.lblText = None
        self.lblFont = None
        self.lbl = None
        self.timeLbl = None
        self.timeLblFontColor = None
        self.timeLblXPos = None
        self.timeLblYPos = None
        self.timeLblText = None
        self.timeLblFont = None
        self.colorLbl = None
        self.colorLblFontColor = None
        self.colorLblXPos = None
        self.colorLblYPos = None
        self.colorLblText = None
        self.colorLblFont = None
        self.buttons = None
        self.interfaceState = None
        self.image = None
        self.imageX = None
        self.imageY = None
        self.timeRemaining = None
        self.printPercent = None
        self.nextPullTime = None
        self.pullInterval = None
        self.progressBar = None
        self.pBarRect = None
        self.pBarFill = None
        self.pickColorRect = None
        self.colorCodes = None
        self.colorNameList = None
        self.colorCodeList = None
        self.colorList = None
        self.listPosition = None
        self.selectedColoridx = None
    
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
        
        t = time()
        if t > self.nextPullTime:
            self.nextPullTime = time() + self.pullInterval
            
            self.timeRemaining = "4:55:12"
            
            if self.interfaceState == 0:
                self.printPercent = float(self.printPercent + 0.05)
                if self.printPercent > 1:
                    self.printPercent = 1
                    self.printing = False
        
            
        return
    
    """*************************************************************************
                                Update Vars Method 
    
    Update variables
    *************************************************************************""" 
    def UpdateVars(self):
        
        self.lblFontColor = self.interfaceLoader.GetLblsFontColor(self.interfaceState)
        self.lblXPos = self.interfaceLoader.GetLblsXPos(self.interfaceState)
        self.lblYPos = self.interfaceLoader.GetLblsYPos(self.interfaceState)
        self.lblText = self.interfaceLoader.GetLblsText(self.interfaceState)
        self.lblFont = self.interfaceLoader.GetLblsFont(self.interfaceState)
        
        self.timeLblFontColor = self.interfaceLoader.GetTimeLblFontColor(self.interfaceState)
        self.timeLblXPos = self.interfaceLoader.GetTimeLblXPos(self.interfaceState)
        self.timeLblYPos = self.interfaceLoader.GetTimeLblYPos(self.interfaceState)
        self.timeLblText = self.interfaceLoader.GetTimeLblText(self.interfaceState)
        self.timeLblFont = self.interfaceLoader.GetTimeLblFont(self.interfaceState)
        
        self.colorLblFontColor = self.interfaceLoader.GetColorLblFontColor(self.interfaceState)
        self.colorLblXPos = self.interfaceLoader.GetColorLblXPos(self.interfaceState)
        self.colorLblYPos = self.interfaceLoader.GetColorLblYPos(self.interfaceState)
        self.colorLblText = self.interfaceLoader.GetColorLblText(self.interfaceState)
        self.colorLblFont = self.interfaceLoader.GetColorLblFont(self.interfaceState)
        
        self.buttons = self.interfaceLoader.GetButtonsList(self.interfaceState)
        
        if (self.interfaceState == 3) or (self.interfaceState == 4):
            self.image = None
            self.imageX = None
            self.imageY = None
        else:    
            self.image = pygame.image.load(self.interfaceLoader.GetImagePath(self.interfaceState))
            self.imageX = self.interfaceLoader.GetImageX(self.interfaceState)
            self.imageY = self.interfaceLoader.GetImageY(self.interfaceState)
        
        self.progressBar = self.interfaceLoader.GetProgessBar(self.interfaceState)
        
        return
    
    """*************************************************************************
                                GetSelectedIdx Method 
    
    Identifies which color the user chose by clicking the list
    *************************************************************************""" 
    def GetSelectedIdx(self, event):
        
        if self.interfaceState ==4:
            pos = pygame.mouse.get_pos()
            posX = pos[0]
            posY = pos[1]
            
            width = self.interfaceLoader.GetPickerWidth()
            height = self.interfaceLoader.GetPickerHeight()
            pickerXMin = self.interfaceLoader.GetPickerX()
            pickerXMax = pickerXMin + width
            pickerYMin = self.interfaceLoader.GetPickerY() - (2 * height)
            pickerYMax = pickerYMin + (5 * height)
            
            if (posX>pickerXMin) and (posX<pickerXMax) and (posY>pickerYMin) and (posY<pickerYMax):
                relY = posY - pickerYMin
                idxChange = -2 + int(relY/height)
                self.listPosition = self.listPosition + idxChange
        
        return 