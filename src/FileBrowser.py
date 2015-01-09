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
from time import time
import math
import FileFinder
import pygame

class FileBrowserScreen():
    
    exit = False
    interfaceState = 0
    
    lblTopText = None           #list for top label text
    lblTop = None               #Top label object
    lblTopFont = None           #Top label font
    lblTopFontColor = None      #top label color
    
    lblText = None           #list for label text
    lbl = None               #label object
    lblFont = None           #label font
    lblFontColor = None      #label color
    
    buttons = None              #list for interface buttons
    
    selectedRoot = "RPI"
    selctedRootRect = None
    
    cancelTransfer = False
    initTransfer = False
    blocksTransfered = 0
    nBlocks = 0
    
    startPrint = False
    
    """
    File Picker
    """
    fileList = None
    pickFileRect = None        #Rect for selected color
    listPosition = 0
    selectedFileIdx = 0
    pickerStrLen = 20
    
    selectedFileName = None
    
    """
    Slicer
    """
    ready2Print = False
    selectedRes = "ResLow"
    selectedFill = "FillLow"
    pullInterval = 1         #pull interval for simulation mode
    nextPullTime = None
    
    """
    Images
    """
    slicingImgPath = None
    transfImgPath = None
    heatImgPath = None
    
    slicingImgX = 0
    slicingImgY = 0
    
    transfImgX = 0
    transfImgY = 0
    
    heatImgX = 0
    heatImgY = 0
    
    """
    Heating vars
    """
    targetTemperature = 220     
    nozzleTemperature = 0
    
    """
    Progress Bar vars
    """
    progressBar = None
    pBarRect = None
    pBarFill = None
    
    """
    BEEConnect vars
    """
    #conn = None
    beeCon = None
    beeCmd = None
    
    """*************************************************************************
                                Init Method 
    
    Inits current screen components
    *************************************************************************"""
    def __init__(self, screen, interfaceLoader, cmd):
        """
        .
        """
        print("Loading File Browser Screen Components")
        
        self.beeCmd = cmd
        self.beeCon = self.beeCmd.beeCon
        
        self.exit = False
        self.firstNextReady = False
        self.ready2Print = False
        
        self.screen = screen
        self.interfaceLoader = interfaceLoader
        
        self.interfaceState = 0         #reset interface state
        
        self.cancelTransfer = False
        self.initTransfer = False
        
        """
        Load lists and settings from interfaceLoader
        """
        self.lblTopFont = self.interfaceLoader.GetTopLblFont(self.interfaceState)
        self.lblTopFontColor = self.interfaceLoader.GetTopLblFontColor(self.interfaceState)
        self.lblTopText = self.interfaceLoader.GetToplblText(self.interfaceState)
        
        self.lblFont = self.interfaceLoader.GetlblFont(self.interfaceState)
        self.lblFontColor = self.interfaceLoader.GetlblFontColor(self.interfaceState)
        self.lblText = self.interfaceLoader.GetlblText(self.interfaceState)
        
        self.buttons = self.interfaceLoader.GetButtonsList(self.interfaceState)
        
        #PROGRESS BAR
        self.progressBar = self.interfaceLoader.GetProgessBar()
        
        #FILE LIST
        self.LoadFileList(self.interfaceLoader.GetRpiDir())
        self.pickerStrLen = self.interfaceLoader.GetPickerStrLen()
        
        self.slicingImg = pygame.image.load(self.interfaceLoader.GetSlicingImgPath())
        self.transfImg = pygame.image.load(self.interfaceLoader.GetTransfImgPath())
        self.heatImg = pygame.image.load(self.interfaceLoader.GetHeatImgPath())
        
        self.slicingImgX = self.interfaceLoader.GetSlicingImgX()
        self.slicingImgY = self.interfaceLoader.GetSlicingImgY()
        
        self.transfImgX = self.interfaceLoader.GetTransfImgX()
        self.transfImgY = self.interfaceLoader.GetTransfImgY()
        
        self.heatImgX = self.interfaceLoader.GetHeatImgX()
        self.heatImgY = self.interfaceLoader.GetHeatImgY()
        
        self.nextPullTime = time() + self.pullInterval
    
        return

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
                    
                    if btnName == "Up":
                        self.listPosition = self.listPosition - 1
                    elif btnName == "Down":
                        self.listPosition = self.listPosition + 1
                    elif btnName == "RPI":
                        self.listPosition = 0
                        self.LoadFileList(self.interfaceLoader.GetRpiDir())
                        self.selectedRoot = btnName
                    elif btnName == "USB":
                        self.LoadFileList(self.interfaceLoader.GetUsbDir())
                        self.selectedRoot = btnName
                    elif btnName == "Next":
                        self.selectedFileIdx = (2+self.listPosition) % len(self.fileList)
                        self.selectedFileName = self.fileList[self.selectedFileIdx]
                        if self.selectedFileName.endswith(".stl"):
                            self.interfaceState = self.interfaceState + 1
                        elif self.selectedFileName.endswith(".gcode"):
                            self.interfaceState = self.interfaceState + 3
                            self.initTransfer = True
                            #self.transferFile(self.selectedFileName)
                        
                        print("Selected: ",self.selectedFileName)
                    elif btnName == "ResLow":
                        self.selectedRes = btnName
                        print('Click')
                    elif btnName == "ResMed":
                        self.selectedRes = btnName
                    elif btnName == "ResHigh":
                        self.selectedRes = btnName
                    elif btnName == "FillLow":
                        self.selectedFill = btnName
                    elif btnName == "FillMed":
                        self.selectedFill = btnName
                    elif btnName == "FillHigh":
                        self.selectedFill = btnName
                    elif btnName == "Slice":
                        print("Start Slicing with ", self.selectedRes, " and ", self.selectedFill)
                        self.interfaceState = self.interfaceState + 1
                        self.nextPullTime = time() + self.pullInterval
                        self.ready2Print = False
                        
                    elif btnName == "Cancel":
                        self.cancelTransfer = True
                        self.interfaceState = 0
                        #self.exit = True
                    elif btnName == "Print":
                        self.interfaceState = 3
                        
                    """
                    Load new buttons and labels from interfaceLoader
                    """
                    self.lblTopFont = None
                    self.lblTopFontColor = None
                    self.lblTopText = None
                    
                    self.lblFont = None
                    self.lblFontColor = None
                    self.lblText = None
                    
                    self.buttons = None
                    
                    self.lblTopFont = self.interfaceLoader.GetTopLblFont(self.interfaceState)
                    self.lblTopFontColor = self.interfaceLoader.GetTopLblFontColor(self.interfaceState)
                    self.lblTopText = self.interfaceLoader.GetToplblText(self.interfaceState)
                    
                    self.lblFont = self.interfaceLoader.GetlblFont(self.interfaceState)
                    self.lblFontColor = self.interfaceLoader.GetlblFontColor(self.interfaceState)
                    self.lblText = self.interfaceLoader.GetlblText(self.interfaceState)
                    
                    self.buttons = self.interfaceLoader.GetButtonsList(self.interfaceState)
                    
            event = None
        
        return

    """*************************************************************************
                                update Method 
    
    Updates screen components
    *************************************************************************"""
    def update(self):
        
        self.lblTop = self.lblTopFont.render(self.lblTopText, 1, self.lblTopFontColor)
        
        self.lbl = []
        for i in range(0,len(self.lblText)):
            self.lbl.append(self.lblFont[i].render(self.lblText[i], 1, self.lblFontColor[i]))
        
        for btn in self.buttons:
            if self.interfaceState == 2:
                if btn._propGetName() == "Print":
                    btn.visible = self.ready2Print
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
        
        self.screen.blit(self.lblTop, (self.interfaceLoader.GetTopLblXPos(self.interfaceState),
                                            self.interfaceLoader.GetTopLblYPos(self.interfaceState)))
                                            
        for i in range(0,len(self.lblText)):
            self.screen.blit(self.lbl[i], (self.interfaceLoader.GetlblTopXPos(self.interfaceState)[i],
                                            self.interfaceLoader.GetlblTopYPos(self.interfaceState)[i]))
            
        for btn in self.buttons:
            btn.draw(self.screen)
            btnName = btn._propGetName()
            if (btnName == self.selectedRoot) or (btnName == self.selectedRes) or (btnName == self.selectedFill):
                pygame.draw.rect(self.screen, btn._propGetFgColor(), btn._propGetRect(), 3)
                
        
        if self.interfaceState == 0:
            
            x = self.interfaceLoader.GetPickerX()
            y = self.interfaceLoader.GetPickerY()
            width = self.interfaceLoader.GetPickerWidth()
            height = self.interfaceLoader.GetPickerHeight()
            pickerColor = self.interfaceLoader.GetPickerFontColor()
            fontSize = self.interfaceLoader.GetPickerFontSize()
            pickerFont = self.interfaceLoader.GetPickerFont()
            lblOffset = int((height-fontSize)/2)
            
            listRange = len(self.fileList)
            if listRange >= self.interfaceLoader.GetPickerRowCount():
                listRange = self.interfaceLoader.GetPickerRowCount()
            
            for i in range(0, listRange):
                pos = i + self.listPosition

                idx = pos % len(self.fileList)
                
                fileName = self.fileList[idx]
                if len(fileName) > self.pickerStrLen:
                    fileName = fileName[:self.pickerStrLen-3] + "..."
                lblStr = fileName

                fileLbl = None
                yPos = 0
                if ((i == int(listRange/3) + 1) and (listRange >= self.interfaceLoader.GetPickerRowCount())):
                    fileLbl = pickerFont.render(lblStr, 1, pickerColor)
                elif ((i == int(listRange/3)+1) and (listRange < self.interfaceLoader.GetPickerRowCount())):
                    fileLbl = pickerFont.render(lblStr, 1, pickerColor)
                else:
                    font = pygame.font.Font("Fonts/DejaVuSans-Light.ttf",fontSize)
                    fileLbl = font.render(lblStr, 1, pickerColor)
                    
                if listRange >= self.interfaceLoader.GetPickerRowCount():
                    yPos = y+lblOffset+((-2+i)*height)
                else:
                    yPos = y+lblOffset+((-2+i)*height)
                    
                self.screen.blit(fileLbl, (x + int(0.1*height),yPos))

                if (i>0 and i<listRange) and listRange > 2:
                    pygame.draw.line(self.screen, pickerColor, (x, y+((-2+i)*height)),
                                (x+width, y+((-2+i)*height)), int(0.05*height))


            self.pickFileRect = pygame.draw.rect(self.screen, pickerColor, (x,y,width,height), 3)
            
        elif self.interfaceState == 2:
            # Draw Image
            self.screen.blit(self.slicingImg,(self.slicingImgX,self.slicingImgY))
        #TRANSFERING
        elif self.interfaceState == 3:
            # Draw Image
            self.screen.blit(self.transfImg,(self.transfImgX,self.transfImgY))
            # Draw Progress Bar
            self.progressBar.DrawRect(self.screen)
            fill = 0
            try:
                fill = float(self.blocksTransfered/self.nBlocks)
            except:
                pass
            self.screen.blit(self.progressBar.GetSurface(fill),
                                self.progressBar.GetPos())
        #HEATING
        elif self.interfaceState == 4:
            # Draw Image
            self.screen.blit(self.heatImg,(self.heatImgX,self.heatImgY))
            # Draw Progress Bar
            self.progressBar.DrawRect(self.screen)
            self.screen.blit(self.progressBar.GetSurface(float(self.nozzleTemperature/self.targetTemperature)),
                                self.progressBar.GetPos())
        
        return
    
    """*************************************************************************
                                GetCurrentScreenName Method 
    
    Frees every element from memmory
    *************************************************************************""" 
    def GetCurrentScreenName(self):
        
        return "Browser"
    
    """*************************************************************************
                                KillAll Method 
    
    Frees every element from memmory
    *************************************************************************""" 
    def KillAll(self):
        
        self.exit = None
        self.interfaceState = None
        self.lblTopText = None
        self.lblTop = None
        self.lblTopFont = None
        self.lblTopFontColor = None
        self.lblText = None
        self.lbl = None
        self.lblFont = None
        self.lblFontColor = None
        self.buttons = None
        self.selectedRoot = None
        self.selctedRootRect = None
        self.fileList = None
        self.pickFileRect = None
        self.listPosition = None
        self.selectedFileIdx = None
        self.pickerStrLen = None
        self.selectedFileName = None
        self.ready2Print = None
        self.selectedRes = None
        self.selectedFill = None
        self.pullInterval = None
        self.nextPullTime = None
        self.slicingImgPath = None
        self.transfImgPath = None
        self.heatImgPath = None
        self.slicingImgX = None
        self.slicingImgY = None
        self.transfImgX = None
        self.transfImgY = None
        self.heatImgX = None
        self.heatImgY = None
        
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
            #self.ready2Print = True
            
            if(self.interfaceState == 4):
                self.nozzleTemperature = self.beeCmd.GetNozzleTemperature()
                if(self.nozzleTemperature >= self.targetTemperature):
                    self.nozzleTemperature = self.targetTemperature
                    if(self.startPrint == True):
                        self.startPrint = False
                        self.beeCmd.home()
                        self.beeCmd.startSDPrint();
                    
            
            self.nextPullTime = time() + self.pullInterval
            
        if(self.interfaceState == 3):
            if(self.initTransfer == True):
                self.blocksTransfered = 0
                self.nBlocks = 0
                self.transferFile(self.selectedFileName)
                
        """
        t = time()
        if t > self.nextPullTime:
            
            self.nozzleTemperature = self.beeCmd.GetNozzleTemperature()
            
            if self.nozzleTemperature >= self.targetTemperature:
                self.nozzleTemperature = self.targetTemperature
                if(self.firstNextReady == False):
                    self.beeCmd.beep()
                
                self.firstNextReady = True
            
            self.nextPullTime = time() + self.pullInterval
        """
            
        return
    
    """*************************************************************************
                                GetSelectedIdx Method 
    
    Identifies which color the user chose by clicking the list
    *************************************************************************""" 
    def GetSelectedIdx(self, event):
        
        #self.LoadFileList("/Users/marcosgomes/Downloads/",".stl")
        
        
        if self.interfaceState ==0:
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
    
    """*************************************************************************
                                LoadFileList Method 
    
    Loads the file list in the directory with the selected fileType
    *************************************************************************""" 
    def LoadFileList(self, directory):
        
        self.fileList = []
        
        ff = FileFinder.FileFinder()
        
        for file in os.listdir(ff.GetAbsPath(directory)):
            if file.endswith(".stl") or file.endswith(".gcode"):                
                self.fileList.append(file)
                #print(file)
                
        return
    
    """*************************************************************************
                                transferFile Method 
    
    Transfers Gcode file to R2C2
    *************************************************************************""" 
    def transferFile(self, filename):
        
        self.initTransfer = False
        self.startPrint = False
        
        #check if file exists
        if(os.path.isfile(filename) == False):
            print("File does not exist")
            return
        
        #Load File
        print("   :","Loading File")
        f = open(filename, 'rb')
        fSize = os.path.getsize(filename)
        print("   :","File Size: ", fSize, "bytes")
        
        blockBytes = self.beeCmd.MESSAGE_SIZE * self.beeCmd.BLOCK_SIZE
        self.nBlocks = math.ceil(fSize/blockBytes)
        print("   :","Number of Blocks: ", self.nBlocks)
        
        
        
        #TODO SEND M31 WITH ESTIMATED TIME
        
        fnSplit = filename.split(".")
        sdFN = fnSplit[0]
        
        #CREATE SD FILE
        resp = self.beeCmd.CraeteFile(sdFN)
        if(not resp):
            return
        
        #Start transfer
        self.blocksTransfered = 0
        totalBytes = 0
        
        startTime = time()
        
        #Load local file
        with open(filename, 'rb') as f:

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
                    
                retVal = pygame.event.get()
                self.handle_events(retVal)
                self.Pull()
                self.draw()
                self.update()
                self.blocksTransfered += 1
                print("   :","Transfered ", str(self.blocksTransfered), "/", str(self.nBlocks), " blocks ", totalBytes, "/", fSize, " bytes")
            
        print("   :","Transfer completed")
        
        elapsedTime = time()- startTime
        avgSpeed = fSize//elapsedTime
        print("Elapsed time: ",elapsedTime)
        print("Average Transfer Speed: ", avgSpeed)
        
        #OPEN SD FILE
        resp = self.beeCmd.OpenFile(sdFN)
        if(not resp):
            return
        
        print("Heating")
        #Heat Nozzle
        self.beeCmd.SetNozzleTemperature(self.targetTemperature)
        self.startPrint = True
        
        print("Start printing")
        
        self.interfaceState = 4
        
        return
