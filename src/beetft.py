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
import About
import BEETFTJsonLoader
import Calibration
import FilamentChange
import FileBrowser
import Jog
import PrinterInfo
import Printing
import Settings
import WaitForConnection
import pygame
import BEETFT_Button
import BEECommand
import BEEConnect
import math
import time

os.environ["SDL_FBDEV"] = "/dev/fb1"
os.environ["SDL_MOUSEDEV"] = "/dev/input/touchscreen"
os.environ["SDL_MOUSEDRV"] = "TSLIB"

"""
Main Class Interfaces
"""
class BEETFT_Main():
    
    """
    BEEConnect vars
    """
    #conn = None
    beeCon = None
    beeCmd = None
    
    """
    State vars
    """
    BEEConnected = False
    BEEState = "Diconnected"            #["Diconnected","StandBy","Printing"]
    
    blocksTransfered = 0
    nBlocks = 0
    cancelTransfer = False
    
    """
    vars
    @var done: anything can set to True to force quit
    """
    restart = False
    done = False
    jsonLoader = None
    BEEDisplay = None
    
    """
    Left Menu
    """
    leftMenuButtons = None
    interfaceButtons = None
    
    leftMenuLoader = None
    carouselButtons = None
    visibleButtons = None
    currentIdx = None
    carouselItems = None
    carouselX = None
    carouselY = None
    carouselWidth = None
    carouselHeight = None
    carouselButtonHeight = None
    buttonNames = None
    buttonTitles = None
    carouselBgR = None
    carouselBgG = None
    carouselBgB = None
    carouselFR = None
    carouselFG = None
    carouselFB = None
    carouselFontType = None
    carouselFontSize = None
        
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
        self.restart = True
        self.cancelTransfer = False
        
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
        
        """
        Left Menu Loader
        """
        self.leftMenuLoader = self.jsonLoader.GetLeftMenuLoader()
        
        self.carouselButtons = self.leftMenuLoader.GetCarouselButtons()
        
        self.currentIdx = 0
        self.carouselItems = self.leftMenuLoader.GetCarouselItems()
        self.carouselX = self.leftMenuLoader.GetCarouselX()
        self.carouselY = self.leftMenuLoader.GetCarouselY()
        self.carouselWidth = self.leftMenuLoader.GetCarouselWidth()
        self.carouselHeight = self.leftMenuLoader.GetCarouselHeight()
        self.carouselButtonHeight = self.leftMenuLoader.GetCarouselButtonHeight()
        
        self.buttonNames = self.leftMenuLoader.GetCarouselButtonNames()
        self.buttonTitles = self.leftMenuLoader.GetCarouselButtonTitles()
        
        self.carouselBgR = self.leftMenuLoader.GetBgR()
        self.carouselBgG = self.leftMenuLoader.GetBgG()
        self.carouselBgB = self.leftMenuLoader.GetBgB()
        self.carouselFR = self.leftMenuLoader.GetFR()
        self.carouselFG = self.leftMenuLoader.GetFG()
        self.carouselFB = self.leftMenuLoader.GetFB()
        
        self.carouselFontType = self.leftMenuLoader.GetCarouselFontType()
        self.carouselFontSize = self.leftMenuLoader.GetCarouselFontSize()
        
        #self.interfaceButtons = self.jsonLoader.GetLeftButtonsList()
        self.UpdateLeftButtons()
        
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
        #pygame.mouse.set_visible(False)
        
        
        
        self.screen = self.BEEDisplay.GetBEEScreen()
        self.screen.fill(self.BEEDisplay.GetbgColor())
        
        """
        Wait For Connection
        """
        waitScreen = WaitForConnection.WaitScreen(self.screen)
        #If the user closes the windows without a connection
        if not waitScreen.connected:
            self.done = True
            
        self.beeCon = waitScreen.beeCon
        self.beeCmd = BEECommand.Command(self.beeCon)
        
        waitScreen.KillAll()
        waitScreen = None
        
        self.GetBEEStatus()
        
        
        """
        Print interface screen
        """
        if(self.BEEState == "SD_Print"):
            #init print screen in Printing state
            self.LoadCurrentScreen("Print", 0)
        elif( self.BEEState == "Ready"):
            """
            Init Interfaces Screens
            """
            self.beeCmd.home()
            self.currentScreenName = self.jsonLoader.GetDefaultScreen()
            self.LoadCurrentScreen(self.currentScreenName)
        
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
            pullRes = self.currentScreen.Pull()
            
            #check for gobal actions
            if(pullRes is not None):
                print(pullRes)
                if(pullRes == "Transfer"):
                    #init print screen in Transfer state
                    self.BEEState = "Transfer"
                    self.cancelTransfer = False
                    fileName = self.currentScreen.selectedFileName
                    self.LoadCurrentScreen("Print", 5)
                    self.transferFile(fileName)
                
            
            # Check for interface CallBack
            if self.currentScreen.ExitCallBack():
                self.currentScreen.KillAll()
                self.currentScreen = None
                self.beeCmd.homeZ()
                self.beeCmd = None
                self.beeCon.close()
                self.beeCon = None
                self.done = True
                self.restart = True
                #pygame.quit()
                #self = BEETFT_Main()
            
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
                self.restart = False
                self.done = True
                
            for btn in self.carouselButtons:
                if 'click' in btn.handleEvent(event):
                    btnName = btn._propGetName()
                    if btnName == "MenuUp":
                        self.currentIdx = self.currentIdx - 1
                    elif btnName == "MenuDown":
                        self.currentIdx = self.currentIdx + 1
                    self.UpdateLeftButtons()
            
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
                self.LoadCurrentScreen(setScreen)
                
            
        respEvent = self.currentScreen.handle_events(retVal)
        
        if(self.BEEState == "Transfer" and respEvent == "Cancel"):
            self.cancelTransfer = True
                
        return
        
        
        
    """*************************************************************************
                                update Method 
    
    Calls all the individual update methods
    *************************************************************************"""
    def update(self):
        if(self.BEEState == "SD_Print" or self.BEEState == "Transfer"):
            pass
        else:
            #set left buttons visible
            for btn in self.jsonLoader.leftMenuButtons:
                btn.visible = True

            #set carouselbuttons visible
            for btn in self.carouselButtons:
                btn.visible = True
                pass

        self.currentScreen.update()
            
        
        return
            
    """*************************************************************************
                                draw Method 
    
    Draws current screen and calls all the individual draw methods
    *************************************************************************"""   
    def draw(self):
        
        #clear whole screen
        self.screen.fill(self.BEEDisplay.GetbgColor())
        
        if(self.BEEState == "SD_Print" or self.BEEState == "Transfer"):
            pass
        else:
            #draw split line
            self.BEEDisplay.DrawLine(self.screen)

            for btn in self.carouselButtons:
                btn.draw(self.screen)

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
                                UpdateLeftButtons Method 
    
    Updates Left Menu buttons to show
    *************************************************************************"""  
    def UpdateLeftButtons(self):
        
        self.leftMenuButtons = []
        for i in range(0,self.carouselItems):
            
            pos = i + self.currentIdx
            idx = pos % len(self.buttonNames)
                
            x = self.carouselX
            y = self.carouselY + i*self.carouselHeight
            width = self.carouselWidth
            height = self.carouselButtonHeight
            
            beeBtn = BEETFT_Button.Button(x,y,width,height,
                                            self.buttonNames[idx],
                                            self.carouselBgR,self.carouselBgR,self.carouselBgR,
                                            self.carouselFR,self.carouselFG,self.carouselFB,
                                            self.carouselFontType,self.carouselFontSize,
                                            None,None,None,self.buttonTitles[idx])
            
            self.leftMenuButtons.append(beeBtn.GetTextButton())
        
        return
    
    """*************************************************************************
                                GetBEEStatus Method 
    
    Gets the printer status
    *************************************************************************"""  
    def GetBEEStatus(self):
        
        self.BEEState = self.beeCmd.getStatus()
        
        print("Printer Status: ",self.BEEState)
        
        return
    
    """*************************************************************************
                                LoadCurrentScreen Method 
    
    Updates slected screen
    *************************************************************************"""  
    def LoadCurrentScreen(self, setScreen, state = 0):
        
        if(self.currentScreen is not None):
            print("New Screen")
            self.currentScreen.KillAll()
            self.currentScreen = None
            
        if(setScreen == "Print"):
            self.currentScreen = Printing.PrintScreen(self.screen,self.printingScreenLoader,self.beeCmd, state)
        else:
            if setScreen == "PrinterInfo":
                self.currentScreen = PrinterInfo.PrinterInfoScreen(self.screen,self.printerInfoScreenLoader,self.beeCmd)
            elif setScreen == "Jog":
                self.currentScreen = Jog.JogScreen(self.screen,self.jogLoader,self.beeCmd)
            elif setScreen == "Calibration":
                self.currentScreen = Calibration.CalibrationScreen(self.screen,self.calibrationLoader,self.beeCmd)
            elif setScreen == "FilamentChange":
                self.currentScreen = FilamentChange.FilamentChangeScreen(self.screen,self.filamentChangeLoader,self.beeCmd)
            elif setScreen == "Settings":
                self.currentScreen = Settings.SettingsScreen(self.screen,self.settingsLoader,self.beeCmd)
            elif setScreen == "FileBrowser":
                self.currentScreen = FileBrowser.FileBrowserScreen(self.screen,self.fileBrowserLoader,self.beeCmd)
            elif setScreen == "About":
                self.currentScreen = About.AboutScreen(self.screen,self.aboutLoader,self.beeCmd)

            self.currentScreenName = self.currentScreen.GetCurrentScreenName()

        return
    
    """*************************************************************************
                                transferFile Method 
    
    Transfers gcode file to R2C2
    *************************************************************************"""  
    def transferFile(self, fileName):
        
        #check if file exists
        if(os.path.isfile(fileName) == False):
            print("File does not exist")
            return
        
        #Load File
        print("   :","Loading File")
        f = open(fileName, 'rb')
        fSize = os.path.getsize(fileName)
        print("   :","File Size: ", fSize, "bytes")
        
        blockBytes = self.beeCmd.MESSAGE_SIZE * self.beeCmd.BLOCK_SIZE
        self.nBlocks = math.ceil(fSize/blockBytes)
        print("   :","Number of Blocks: ", self.nBlocks)
        
        
        
        #TODO SEND M31 WITH ESTIMATED TIME
        
        fnSplit = fileName.split(".")
        sdFN = fnSplit[0]
        
        #CREATE SD FILE
        resp = self.beeCmd.CraeteFile(sdFN)
        if(not resp):
            return
        
        #Start transfer
        self.blocksTransfered = 0
        totalBytes = 0
        
        startTime = time.time()
        
        #Load local file
        with open(fileName, 'rb') as f:

            while(self.blocksTransfered < self.nBlocks and self.cancelTransfer == False):

                startPos = totalBytes
                endPos = totalBytes + blockBytes
                
                bytes2write = endPos - startPos
                
                if(self.blocksTransfered == self.nBlocks -1):
                    self.beeCmd.StartTransfer(fSize,startPos)
                    bytes2write = fSize - startPos
                else:
                    self.beeCmd.StartTransfer(endPos,startPos)
                    
                msg2write = math.ceil(bytes2write/self.beeCmd.MESSAGE_SIZE)

                for i in range(0,msg2write):
                    msg = f.read(self.beeCmd.MESSAGE_SIZE)
                    #print(msg)
                    resp = self.beeCon.sendCmd(msg,"tog")

                    #print(resp)
                    totalBytes += self.beeCmd.MESSAGE_SIZE
                
                self.blocksTransfered += 1
                
                self.currentScreen.Pull([self.blocksTransfered,self.nBlocks])
                self.handle_events()
                self.update()
                self.draw()
                
                
                print("   :","Transfered ", str(self.blocksTransfered), "/", str(self.nBlocks), " blocks ", totalBytes, "/", fSize, " bytes")
            
        print("   :","Transfer completed")
        
        elapsedTime = time.time()- startTime
        avgSpeed = fSize//elapsedTime
        print("Elapsed time: ",elapsedTime)
        print("Average Transfer Speed: ", avgSpeed)
        
        #OPEN SD FILE
        resp = self.beeCmd.OpenFile(sdFN)
        if(not resp):
            return
        
        #init print screen in Heat state
        self.LoadCurrentScreen("Print", 6)
        
        return

def restart_program():
    python = sys.executable
    os.execl(python, python, * sys.argv)

if __name__ == '__main__':
    app = BEETFT_Main()
    app.start()
    if(app.restart == True):
        app = None
        restart_program()