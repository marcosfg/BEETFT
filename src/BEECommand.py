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

import usb.core
import usb.util
import sys
import os
import time
import BEEConnect
import time

class Command():
    
    connected = None
    beeCon = None
    
    MESSAGE_SIZE = 512
    BLOCK_SIZE = 32

    """*************************************************************************
                                Init Method 
    
    Inits current screen components
    *************************************************************************"""
    def __init__(self, bee):
        
        self.beeCon = bee
        self.connected = self.beeCon.isConnected()
        
        return
    
    """*************************************************************************
                                connected Method 
    
    *************************************************************************"""
    def isConnected(self):
        return self.connected
    
    """*************************************************************************
                                Start Printer Method 
    
    *************************************************************************"""
    def startPrinter(self):
        
        #self.beeCon = BEEConnect.Connection()
        resp = self.beeCon.sendCmd("M625\n")
        print(resp)
        if('Bad M-code 625' in resp):   #printer in bootloader mode
            print("Printer running in Bootloader Mode")
            print("Changing to firmware")
            self.beeCon.sendCmd("M630\n")
            return "Bootloader"
        elif('ok Q' in resp):
            print("Printer running in firmware mode")
            return "Firmware"
        else:
            return ""
        
        return
    
    """*************************************************************************
                                getStatus Method 
    retuns string with printer status
    *************************************************************************"""
    def getStatus(self):
        
        resp = self.beeCon.sendCmd("M625\n")
        print(resp)
        
        sPos = resp.find('S:')
        
        try:
            status = int(resp[sPos+2])
        except:
            return "Unknown"
        
        if(status == 3):
            return "Ready"
        elif(status == 4):
            return "Moving"
        elif(status == 5):
            return "SD_Print"
        elif(status == 6):
            return "Transfering"
        elif(status == 7):
            return "Pause"
        elif(status == 9):
            return "SDown_Wait"
        
        return "Unknown"

    """*************************************************************************
                                beep Method 
    
    *************************************************************************"""
    def beep(self):
        
        self.beeCon.sendCmd("M300 P2000\n")
        
        return

    """*************************************************************************
                                home Method 
    
    *************************************************************************"""
    def home(self):
        
        self.beeCon.sendCmd("G28\n","3")
        
        return
    
    """*************************************************************************
                                homeXY Method 
    
    *************************************************************************"""
    def homeXY(self):
        
        self.beeCon.sendCmd("G28 X0 Y0\n","3")
        
        return
    
    """*************************************************************************
                                homeZ Method 
    
    *************************************************************************"""
    def homeZ(self):
        
        self.beeCon.sendCmd("G28 Z0\n","3")
        
        return
    
    """*************************************************************************
                                move Method 
    
    *************************************************************************"""
    def move(self,x=None,y=None,z=None,e=None):
        
        resp = self.beeCon.sendCmd("M121\n")
        print(resp)
        
        splits = resp.split(" ")
        xSplit = splits[2].split(":")
        ySplit = splits[3].split(":")
        zSplit = splits[4].split(":")
        eSplit = splits[5].split(":")
        
        currentX = float(xSplit[1])
        currentY = float(ySplit[1])
        currentZ = float(zSplit[1])
        currentE = float(eSplit[1])
        
        newX = currentX
        newY = currentY
        newZ = currentZ
        newE = currentE
        
        if x is not None:
            newX = newX + x
        if y is not None:
            newY = newY + y
        if z is not None:
            newZ = newZ + z
        if e is not None:
            newE = newE + e
        
        commandStr = "G1 X" + str(newX) + " Y" + str(newY) + " Z" + str(newZ) + " E" + str(newE) + "\n"
        
        self.beeCon.sendCmd(commandStr,"3")
        
        return
    
    """*************************************************************************
                                GoToFirstCalibrationPoint Method 
    
    *************************************************************************"""
    def GoToFirstCalibrationPoint(self):
        
        
        #go to home
        self.beeCon.sendCmd("G28\n","3")
        
        #set feedrate
        resp = self.beeCon.sendCmd("G1 F15000\n")
        print(resp)
        
        #set acceleration
        resp = self.beeCon.sendCmd("M206 X400\n")
        print(resp)
        
        #go to first point
        self.beeCon.sendCmd("G1 X0 Y67 Z2\n")
        
        #set acceleration
        resp = self.beeCon.sendCmd("M206 X1000\n","3")
        print(resp)
        
        return
    
    """*************************************************************************
                                GoToSecondCalibrationPoint Method 
    
    *************************************************************************"""
    def GoToSecondCalibrationPoint(self):
        
        #record calibration position
        resp = self.beeCon.sendCmd("M603\n")
        print(resp)
        resp = self.beeCon.sendCmd("M601\n")
        print(resp)
        
        #set feedrate
        resp = self.beeCon.sendCmd("G1 F5000\n")
        print(resp)
        #set acceleration
        resp = self.beeCon.sendCmd("M206 X400\n")
        print(resp)
        
        self.move(0,0,10,0)
        #go to SECOND point
        resp = self.beeCon.sendCmd("G1 X-31 Y-65\n","3")
        print(resp)
        self.move(0,0,-10,0)
        
        return
    
    """*************************************************************************
                                GoToThirdCalibrationPoint Method 
    
    *************************************************************************"""
    def GoToThirdCalibrationPoint(self):
        
        #set feedrate
        resp = self.beeCon.sendCmd("G1 F5000\n")
        print(resp)
        #set acceleration
        resp = self.beeCon.sendCmd("M206 X400\n")
        print(resp)
        
        self.move(0,0,10,0)
        #go to SECOND point
        resp = self.beeCon.sendCmd("G1 X35 Y-65\n","3")
        print(resp)
        self.move(0,0,-10,0)
        
        return
    
    """*************************************************************************
                                GetNozzleTemperature Method 
    
    *************************************************************************"""
    def GetNozzleTemperature(self):
        
        #get Temperature
        resp = self.beeCon.sendCmd("M105\n")
        #print(resp)
        
        try:
            splits = resp.split(" ")
            tPos = splits[0].find("T:")
            t = float(splits[0][tPos+2:])
            return t
        except:
            pass
        
        return 0

    """*************************************************************************
                                SetNozzleTemperature Method 
    
    *************************************************************************"""
    def SetNozzleTemperature(self, t):
        
        commandStr = "M104 S" + str(t) + "\n"
        
        #set Temperature
        resp = self.beeCon.sendCmd(commandStr)
        print(resp)
        
        return
    
    """*************************************************************************
                                Load Method 
    
    *************************************************************************"""
    def Load(self):
        
        resp = self.beeCon.sendCmd("G92 E\n")
        resp = self.beeCon.sendCmd("M300 P500\n")
        resp = self.beeCon.sendCmd("M300 S0 P500\n")
        resp = self.beeCon.sendCmd("M300 P500\n")
        resp = self.beeCon.sendCmd("M300 S0 P500\n")
        resp = self.beeCon.sendCmd("M300 P500\n")
        resp = self.beeCon.sendCmd("M300 S0 P500\n")
        resp = self.beeCon.sendCmd("G1 F300 E100\n")
        resp = self.beeCon.sendCmd("G92 E\n")
        return

    """*************************************************************************
                                Unload Method 
    
    *************************************************************************"""
    def Unload(self):
        
        resp = self.beeCon.sendCmd("G92 E\n")
        resp = self.beeCon.sendCmd("M300 P500\n")
        resp = self.beeCon.sendCmd("M300 S0 P500\n")
        resp = self.beeCon.sendCmd("M300 P500\n")
        resp = self.beeCon.sendCmd("M300 S0 P500\n")
        resp = self.beeCon.sendCmd("M300 P500\n")
        resp = self.beeCon.sendCmd("M300 S0 P500\n")
        resp = self.beeCon.sendCmd("G1 F300 E50\n")
        resp = self.beeCon.sendCmd("G92 E\n")
        resp = self.beeCon.sendCmd("G1 F1000 E-23\n","3")
        resp = self.beeCon.sendCmd("G1 F800 E2\n","3")
        resp = self.beeCon.sendCmd("G1 F2000 E-23\n","3")
        resp = self.beeCon.sendCmd("G1 F200 E-50\n","3")
        resp = self.beeCon.sendCmd("G92 E\n")
        
        return

    """*************************************************************************
                                GoToHeatPos Method 
    
    *************************************************************************"""
    def GoToHeatPos(self):
        
        #set feedrate
        resp = self.beeCon.sendCmd("G1 F15000\n")
        print(resp)
        
        #set acceleration
        resp = self.beeCon.sendCmd("M206 X400\n")
        print(resp)
        
        #go to first point
        self.beeCon.sendCmd("G1 X30 Y0 Z10\n")
        
        #set acceleration
        resp = self.beeCon.sendCmd("M206 X1000\n","3")
        print(resp)
        
        return

    """*************************************************************************
                                GoToRestPos Method 
    
    *************************************************************************"""
    def GoToRestPos(self):
        
        #set feedrate
        resp = self.beeCon.sendCmd("G1 F15000\n")
        print(resp)
        
        #set acceleration
        resp = self.beeCon.sendCmd("M206 X400\n")
        print(resp)
        
        #go to first point
        self.beeCon.sendCmd("G1 X-50 Y0 Z110\n")
        
        #set acceleration
        resp = self.beeCon.sendCmd("M206 X1000\n","3")
        print(resp)
        
        return
    
    """*************************************************************************
                                GetBeeCode Method 
    
    *************************************************************************"""
    def GetBeeCode(self):
        
        #Get BeeCode
        resp = self.beeCon.sendCmd("M400\n")
        print(resp)
        
        splits = resp.split(" ")
        
        code = ""
        
        for s in splits:
            cPos = s.find("bcode")
            if(cPos >= 0):
                code = s[cPos+6:]
        
        
        return code

    """*************************************************************************
                                SetBeeCode Method 
    
    *************************************************************************"""
    def SetBeeCode(self, code):
        
        commandStr = "M400 " + code + "\n"
        
        #Set BeeCode
        resp = self.beeCon.sendCmd(commandStr)
        
        return

    """*************************************************************************
                                initSD Method 
    
    *************************************************************************"""
    def initSD(self):
        #Init SD
        resp = self.beeCon.sendCmd("M21\n")
        
        tries = 10
        while(tries > 0):
            if("ok" in resp.lower()):
                break
            else:
                resp = self.beeCon.sendCmd("\n")
            tries -= 1
        
        return
    """*************************************************************************
                                CraeteFile Method 
    
    *************************************************************************"""
    def CraeteFile(self, fileName):
        #Init SD
        self.initSD()
        
        fn = fileName
        if(len(fileName) > 8):
            fn = fileName[:8]
        
        cmdStr = "M30 " + fn + "\n"
        
        resp = self.beeCon.sendCmd(cmdStr)

        tries = 10
        while(tries > 0):
            
            if("file created" in resp.lower()):
                print("   :"" SD file created")
                break
            elif("error" in resp.lower()):
                print("   : Error creating file")
                return False
            else:
                resp = self.beeCon.sendCmd("\n")
                #print(resp,"...")
            
            tries -= 1
        if(tries <= 0):
            return False
        
        return True

    """*************************************************************************
                                OpenFile Method 
    
    *************************************************************************"""
    def OpenFile(self, fileName):
        #Init SD
        self.initSD()
        
        cmdStr = "M23 " + fileName + "\n"
        
        #Open File
        resp = self.beeCon.sendCmd(cmdStr)
        
        tries = 10
        while(tries > 0):
            if("file opened" in resp.lower()):
                print("   :"" SD file opened")
                break
            else:
                resp = self.beeCon.sendCmd("\n")
            tries -= 1
        
        if(tries <= 0):
            return False
        
        return True
    
    """*************************************************************************
                                StartTransfer Method 
    
    *************************************************************************"""
    def StartTransfer(self, fSize, a):
        
        cmdStr = "M28 D" + str(fSize - 1) + " A" + str(a) + "\n"
        resp = self.beeCon.sendCmd(cmdStr)
        #print(cmdStr)
        tries = 10
        while(tries > 0):
            if("ok" in resp.lower()):
                print("   :",resp)
                break
            else:
                resp = self.beeCon.sendCmd("\n")
            tries -= 1
        
        if(tries <= 0):
            return False
        
        return True

    """*************************************************************************
                                SendBlock Method 
    
    *************************************************************************"""
    def SendBlock(self, d, a, block):
        
        
        
        return True