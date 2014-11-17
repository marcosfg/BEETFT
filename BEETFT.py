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
import json
from pprint import pprint
from subprocess import call
import BEETFTJsonLoader
import WaitForConnection
import pygame

import BEETFTDisplay
#Screen interfaces imports
import PrinterInfo
import Jog
import Calibration
import FilamentChange
import Settings
import FileBrowser
import About
import Printing

os.environ["SDL_FBDEV"] = "/dev/fb1"
os.environ["SDL_MOUSEDEV"] = "/dev/input/touchscreen"
os.environ["SDL_MOUSEDRV"] = "TSLIB"

"""
Main Class Interfaces
"""
class BEETFT_Main():
    
    """
    State vars
    """
    BEEConnected = False
    BEEState = "Diconnected"            #["Diconnected","StandBy","Printing"]
    
    """
    vars
    @var done: anything can set to True to force quit
    """
    done = False
    jsonLoader = None
    BEEDisplay = None
    leftMenuButtons = None
    
    """
    Interfaces
    """
    currentScreenName = None
    currentScreen = None
    printerInfoScreenLoader = None
    jogScreenLoader = None
    calibrationScreenLoader = None
    filamentScreenLoader = None
    settingsScreenLoader = None
    browserScreenLoader = None
    aboutScreenLoader = None
    
    printingScreenLoader = None

    """*************************************************************************
                                Init Method 
    
    Calls the JSON loader and setups the GUI
    *************************************************************************"""
    def __init__(self):
        
        #Make sure the infinite loop wokrs
        self.done = False
        
        self.BEEState = "Disconnected"
        """
        JSON Loading
        """
        self.jsonLoader = BEETFTJsonLoader.jsonLoader()
        
        print("Using display: ",self.jsonLoader.displayObject.displayType)
        print("Display Resolution: ", 
                self.jsonLoader.displayObject.displayWidth, 
                "x", self.jsonLoader.displayObject.displayHeight)
        
        self.BEEDisplay = self.jsonLoader.displayObject
        self.leftMenuButtons = self.jsonLoader.GetLeftButtonsList()
        
        """
        Screen Loaders
        """
        self.printerInfoScreenLoader = self.jsonLoader.GetPrinterInfoInterface()
        self.jogLoader = self.jsonLoader.GetJogInterface()
        self.calibrationLoader = self.jsonLoader.GetCalibrationInterface()
        self.filamentChangeLoader = self.jsonLoader.GetFilamentChangeInterface()
        self.settingsLoader = self.jsonLoader.GetSettingsInterface()
        self.fileBrowserLoader = self.jsonLoader.GetFileBrowserInterface()
        self.aboutLoader = self.jsonLoader.GetAboutInterface()
        
        self.printingScreenLoader = self.jsonLoader.GetPrintingInterface()
        
        """
        Init pygame
        """
        print("Drawing Interfaces")
        # init pygame and set up screen
        pygame.init()
        self.screen = self.BEEDisplay.GetBEEScreen()
        self.screen.fill(self.BEEDisplay.GetbgColor())
        
        """
        Wait For Connection
        """
        waitScreen = WaitForConnection.WaitScreen(self.screen)
        #If the user closes the windows without a connection
        if not waitScreen.connected:
            self.done = True
            
        waitScreen.KillAll()
        waitScreen = None
        
        self.GetBEEStatus() 
        
        """
        Print interface screen
        """
        if self.BEEState == "Printing":
            self.currentScreen = Printing.PrintScreen(self.screen,self.printingScreenLoader,self.BEEDisplay)
            
            self.currentScreen.KillAll()
            self.currentScreen = None
        
        """
        Init Interfaces Screens
        """
        self.currentScreenName = self.jsonLoader.GetDefaultScreen()
        
        if self.currentScreenName == "PrinterInfo":
            self.currentScreen = PrinterInfo.PrinterInfoScreen(self.screen,self.printerInfoScreenLoader)
        elif self.currentScreenName == "Jog":
            self.currentScreen = Jog.JogScreen(self.screen,self.jogLoader)
        elif self.currentScreenName == "Calibration":
            self.currentScreen = Calibration.CalibrationScreen(self.screen,self.calibrationLoader)
        elif self.currentScreenName == "FilamentChange":
            self.currentScreen = FilamentChange.FilamentChangeScreen(self.screen,self.filamentChangeLoader)
        elif self.currentScreenName == "Settings":
            self.currentScreen = Settings.SettingsScreen(self.screen,self.settingsLoader)
        elif self.currentScreenName == "FileBrowser":
            self.currentScreen = FileBrowser.FileBrowserScreen(self.screen,self.fileBrowserLoader)
        elif self.currentScreenName == "About":
            self.currentScreen = About.AboutScreen(self.screen,self.aboutLoader)
        
    """*************************************************************************
                                Start Method 
    
    Infinit loop, calls methos to draw, update and handle events
    *************************************************************************"""
    def start(self):
        print("\nStarting BEETFT")
        
        while not self.done:
            # Handle events
            self.handle_events()
            
            # Update buttons visibility, text, graphs etc
            self.update()

            # Draw everything
            self.draw()
            
            #Pull variables
            self.currentScreen.Pull()
            
            # Check for interface CallBack
            if self.currentScreen.ExitCallBack():
                self.currentScreen.KillAll()
                self.currentScreen = None
                self = BEETFT_Main()
            
        pygame.quit()
        
        
        
    """*************************************************************************
                                handle_events Method 
    
    Retrieves the event vector and sends it to the individual interface methods
    *************************************************************************"""
    def handle_events(self):

        retVal = pygame.event.get()
        """handle all events."""
        for event in retVal:
            if event.type == pygame.QUIT:
                print("quit")
                self.done = True
                
            self.currentScreen.handle_events(retVal)
            
            setScreen = None
            for btn in self.leftMenuButtons:
                if 'click' in btn.handleEvent(event):
                    if btn._propGetName() == "Printer Info":
                        setScreen = "PrinterInfo"
                    elif btn._propGetName() == "Jog":
                        setScreen = "Jog"
                    elif btn._propGetName() == "Calibration":
                        setScreen = "Calibration"
                    elif btn._propGetName() == "Filament":
                        setScreen = "FilamentChange"
                    elif btn._propGetName() == "Settings":
                        setScreen = "Settings"
                    elif btn._propGetName() == "Browser":
                        setScreen = "FileBrowser"
                    elif btn._propGetName() == "About":
                        setScreen = "About"
                    
            
            if (not (setScreen is None)) and (not setScreen==self.currentScreen.GetCurrentScreenName()):
                self.currentScreen.KillAll()
                self.currentScreen = None
                
                if setScreen == "PrinterInfo":
                    self.currentScreen = PrinterInfo.PrinterInfoScreen(self.screen,self.printerInfoScreenLoader)
                elif setScreen == "Jog":
                    self.currentScreen = Jog.JogScreen(self.screen,self.jogLoader)
                elif setScreen == "Calibration":
                    self.currentScreen = Calibration.CalibrationScreen(self.screen,self.calibrationLoader)
                elif setScreen == "FilamentChange":
                    self.currentScreen = FilamentChange.FilamentChangeScreen(self.screen,self.filamentChangeLoader)
                elif setScreen == "Settings":
                    self.currentScreen = Settings.SettingsScreen(self.screen,self.settingsLoader)
                elif setScreen == "FileBrowser":
                    self.currentScreen = FileBrowser.FileBrowserScreen(self.screen,self.fileBrowserLoader)
                elif setScreen == "About":
                    self.currentScreen = About.AboutScreen(self.screen,self.aboutLoader)
                    
                self.currentScreenName = self.currentScreen.GetCurrentScreenName()
        
        
        
    """*************************************************************************
                                update Method 
    
    Calls all the individual update methods
    *************************************************************************"""
    def update(self):
        #set left buttons visible
        for btn in self.jsonLoader.leftMenuButtons:
            btn.visible = True
        
        self.currentScreen.update()
            
        
        return
            
    """*************************************************************************
                                draw Method 
    
    Draws current screen and calls all the individual draw methods
    *************************************************************************"""   
    def draw(self):
        #clear whole screen
        self.screen.fill(self.BEEDisplay.GetbgColor())
        
        #draw split line
        self.BEEDisplay.DrawLine(self.screen)
        
        for btn in self.leftMenuButtons:
            btn.draw(self.screen)
            if btn._propGetName() == self.currentScreen.GetCurrentScreenName():
                pygame.draw.rect(self.screen, btn._propGetFgColor(), btn._propGetRect(), 3)
        
        #draw screen elements
        self.currentScreen.draw()
        
        # update screen
        pygame.display.update()
        
        return
    
    """*************************************************************************
                                GetBEEStatus Method 
    
    Gets the printer status
    *************************************************************************"""  
    def GetBEEStatus(self):
        
        self.BEEState = "Printing"
        
        return

if __name__ == '__main__':
    opp = BEETFT_Main()
    opp.start()