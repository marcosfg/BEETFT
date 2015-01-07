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

from time import time

import ColorCodesLoader
import FileFinder
import pygame
import BEECommand

class FilamentChangeScreen():
    
    comm = None
    
    exit = False
    interfaceState = 0
    
    lblTopText = None           #list for top label text
    lblTop = None               #Top label object
    lblTopFont = None           #Top label font
    lblTopFontColor = None      #top label color
    
    buttons = None              #list for interface buttons
    
    image = None                #image object for heating screen
    
    targetTemperature = 220     
    nozzleTemperature = 0
    pullInterval = 1         #pull interval for simulation mode
    nextPullTime = None
    
    firstNextReady = False      #true when target temperature is established
    
    pickColorRect = None        #Rect for selected color
    colorCodes = None
    colorNameList = None
    colorCodeList = None
    colorList = None
    listPosition = 0
    selectedColoridx = 0
    
    selectedColorFont = None
    selectedColorFontColor = None
    
    selectedColorCode = None
    selectedColorName = None
    
    """
    Progress Bar vars
    """
    progressBar = None
    pBarRect = None
    pBarFill = None
    
    """*************************************************************************
                                Init Method 
    
    Inits current screen components
    *************************************************************************"""
    def __init__(self, screen, interfaceLoader, comm):
        
        print("Loading Filament Change Screen Components")
        
        self.comm = comm
        
        self.exit = False
        self.firstNextReady = False
        
        self.screen = screen
        self.interfaceLoader = interfaceLoader
        
        self.interfaceState = 0         #reset interface state
        
        """
        Load lists and settings from interfaceLoader
        """
        self.lblTopFont = self.interfaceLoader.GetlblFont(self.interfaceState)
        self.lblTopFontColor = self.interfaceLoader.GetlblFontColor(self.interfaceState)
        self.lblTopText = self.interfaceLoader.GetlblText(self.interfaceState)
        self.buttons = self.interfaceLoader.GetButtonsList(self.interfaceState)
        
        self.progressBar = self.interfaceLoader.GetProgessBar()
        self.image = pygame.image.load(self.interfaceLoader.GetImagePath())
        self.selectedColorFont = self.interfaceLoader.GetSelectedLblFont()
        self.selectedColorFontColor = self.interfaceLoader.GetSelectedLblFontColor()
        
        """
        Load Colors
        """
        self.colorCodes = ColorCodesLoader.ColorCodes()
        self.colorNameList = self.colorCodes.GetColorNameList()
        self.colorCodeList = self.colorCodes.GetColorCodeList()
        self.colorList = self.colorCodes.GetColorList()
        
        #Get Nozzle Temeprature
        self.nozzleTemperature = self.comm.GetNozzleTemperature()
        print("Current Nozzle Temperature: ", self.nozzleTemperature)
        
        #Heat Nozzle
        self.comm.SetNozzleTemperature(self.targetTemperature)
        
        #Go to Heat Position
        self.comm.home()
        self.comm.GoToHeatPos()
        
        #Get current colot code
        self.selectedColorCode = self.comm.GetBeeCode()
        print("Current Color Code: ", self.selectedColorCode)
        self.selectedColorName = self.colorCodes.GetColorName(self.selectedColorCode)
        print("Current Color Name: ", self.selectedColorName)
        
        self.nextPullTime = time() + self.pullInterval
        

    """*************************************************************************
                                handle_events Method 
    
    Received the event vector and checks if it has any event from interface items
    *************************************************************************"""
    def handle_events(self,retVal):
        """handle all events."""
        for event in retVal:
            
            if event.type == pygame.MOUSEBUTTONDOWN:
            	self.GetSelectedIdx(event)
                
            for btn in self.buttons:
                if 'click' in btn.handleEvent(event):
                    btnName = btn._propGetName()
                    
                    if btnName == "Next":
                        if self.interfaceState == 0:
                            self.interfaceState = 1
                            self.comm.GoToRestPos()
                        elif self.interfaceState == 2:
                            self.interfaceState = 1
                            #Get selected list index
                            self.selectedColoridx = (2+self.listPosition) % len(self.colorList)
                            #Get selected color code
                            self.selectedColorCode = self.colorCodeList[self.selectedColoridx]
                            self.comm.SetBeeCode(self.selectedColorCode)
                            #Get selected color name
                            self.selectedColorName = self.colorCodes.GetColorName(self.selectedColorCode)
                            print("Selected Filament Code: ", self.selectedColorCode)
                    elif btnName == "OK":
                        if self.interfaceState == 1:
                            self.exit = True
                    elif btnName == "Pick Color":
                        self.interfaceState = self.interfaceState + 1
                    elif btnName == "Load":
                        print("Load Filament")
                        self.comm.Load()
                    elif btnName == "Unload":
                        print("Unload Filament")
                        self.comm.Unload()
                    elif btnName == "Up":
                        self.listPosition = self.listPosition - 1
                    elif btnName == "Down":
                        self.listPosition = self.listPosition + 1
                        
                    """
                    Load new buttons and labels from interfaceLoader
                    """
                    self.lblTopFont = None
                    self.lblTopFontColor = None
                    self.buttons = None
                    self.lblTopFont = self.interfaceLoader.GetlblFont(self.interfaceState)
                    self.lblTopFontColor = self.interfaceLoader.GetlblFontColor(self.interfaceState)
                    self.buttons = self.interfaceLoader.GetButtonsList(self.interfaceState)
                    self.lblTopText = self.interfaceLoader.GetlblText(self.interfaceState)
                    
        return
    

    """*************************************************************************
                                update Method 
    
    Updates screen components
    *************************************************************************"""
    def update(self):
        
        self.lblTop = self.lblTopFont.render(self.lblTopText, 1, self.lblTopFontColor)
        
        for btn in self.buttons:
            if self.interfaceState == 0:
                if btn._propGetName() == "Next":
                    btn.visible = self.firstNextReady
                else:
                    btn.visible = True
            else:
                btn.visible = True

        return

    """*************************************************************************
                                draw Method 
    
    Draws current screen
    *************************************************************************""" 
    def draw(self):
        
        self.screen.blit(self.lblTop, (self.interfaceLoader.GetlblTopXPos(self.interfaceState),
                                            self.interfaceLoader.GetlblTopYPos(self.interfaceState)))
        
        for btn in self.buttons:
            btn.draw(self.screen)
        
        if self.interfaceState == 0:
            # Draw Image
            x = self.interfaceLoader.GetImageX()
            y = self.interfaceLoader.GetImageY()
            self.screen.blit(self.image,(x,y))
            
            # Draw Progress Bar
            self.progressBar.DrawRect(self.screen)
            self.screen.blit(self.progressBar.GetSurface(float(self.nozzleTemperature/self.targetTemperature)),
                                self.progressBar.GetPos())
        elif self.interfaceState == 1:
            lblCurrentColorText = "Current Color: " + self.selectedColorName
            lbl = self.selectedColorFont.render(lblCurrentColorText, 1, self.selectedColorFontColor)
            self.screen.blit(lbl, (self.interfaceLoader.GetSelectedLblX(),self.interfaceLoader.GetSelectedLblY()))
            
        elif self.interfaceState == 2:
            
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
                    ff = FileFinder.FileFinder()
                    font = pygame.font.Font(ff.GetAbsPath("Fonts/DejaVuSans-Light.ttf"),fontSize)
                    colorLbl = font.render(self.colorNameList[idx], 1, pickerColor)
                    
                self.screen.blit(colorLbl, (x + height +5,y+lblOffset+((-2+i)*height)))
                
                if i>0 and i<5:
                    pygame.draw.line(self.screen, pickerColor, (x, y+((-2+i)*height)),
                                (x+width, y+((-2+i)*height)), int(0.05*height))
            
            
            self.pickColorRect = pygame.draw.rect(self.screen, pickerColor, (x,y,width,height), 3)
            
        
        
        return
    
    """*************************************************************************
                                GetCurrentScreenName Method 
    
    Frees every element from memmory
    *************************************************************************""" 
    def GetCurrentScreenName(self):
        
        return "Filament"
    
    """*************************************************************************
                                KillAll Method 
    
    Frees every element from memmory
    *************************************************************************""" 
    def KillAll(self):
        
        #CANCEL HEATING
        self.comm.SetNozzleTemperature(0)
        
        self.exit = None
        self.interfaceState = None
    
        self.lblTopText = None
        self.lblTop = None
        self.lblTopFont = None
        self.lblTopFontColor = None
    
        self.buttons = None
    
        self.image = None
    
        self.targetTemperature = None
        self.nozzleTemperature = None
        self.pullInterval = None
        self.nextPullTime = None
    
        self.firstNextReady = None
    
        self.pickColorRect = None
        self.colorCodes = None
        self.colorNameList = None
        self.colorCodeList = None
        self.colorList = None
        self.listPosition = None
        self.selectedColoridx = None
    
        self.selectedColorFont = None
        self.selectedColorFontColor = None
    
        self.progressBar = None
        self.pBarRect = None
        self.pBarFill = None
        
        return
    
    """*************************************************************************
                                ExitCallBack Method 
    
    Tells the main class to load the default interface
    *************************************************************************""" 
    def ExitCallBack(self):
        
        
        return self.exit
    
    """*************************************************************************
                                Pull Method 
    
    Pull variables
    *************************************************************************""" 
    def Pull(self):
        
        t = time()
        if t > self.nextPullTime:
            
            self.nozzleTemperature = self.comm.GetNozzleTemperature()
            
            if self.nozzleTemperature >= self.targetTemperature:
                self.nozzleTemperature = self.targetTemperature
                if(self.firstNextReady == False):
                    self.comm.beep()
                
                self.firstNextReady = True
            
            self.nextPullTime = time() + self.pullInterval
        
        
        return
    
    """*************************************************************************
                                GetSelectedIdx Method 
    
    Identifies which color the user chose by clicking the list
    *************************************************************************""" 
    def GetSelectedIdx(self, event):
        
        if self.interfaceState ==2:
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