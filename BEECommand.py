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
from time import time

class Command():
    
    connected = None
    beeConnect = None

    """*************************************************************************
                                Init Method 
    
    Inits current screen components
    *************************************************************************"""
    def __init__(self):
        
        self.beeConnect = BEEConnect.Connection()
        self.connected = self.beeConnect.isConnected()
        
        return
    
    """*************************************************************************
                                connected Method 
    
    *************************************************************************"""
    def isConnected(self):
        return self.connected
    
    """*************************************************************************
                                SendAndWait Method 
    
    *************************************************************************"""
    def SendAndWait(self,cmd):
        
        try:
            resp = self.beeConnect.dispatch(cmd)
            print(resp)

        except Exception:
            busy = True
            nextSend = time() + 1
            while busy:
                t = time()
                if t > nextSend:
                    try:

                        resp = self.beeConnect.dispatch("M625\n")
                        print(resp)
                        if resp.find("S:3") >= 0:
                            busy = False
                    except Exception:
                        pass
        
        return
    
    """*************************************************************************
                                Start Printer Method 
    
    *************************************************************************"""
    def startPrinter(self):
        
        self.beeConnect = BEEConnect.Connection()
        resp = self.beeConnect.dispatch("M625\n")
        print(resp)
        resp = self.beeConnect.dispatch("M630\n")
        print(resp)
        
        self.SendAndWait("G28\n")
        
        
        return
    
    """*************************************************************************
                                homeXY Method 
    
    *************************************************************************"""
    def homeXY(self):
        
        self.beeConnect = BEEConnect.Connection()
        
        self.SendAndWait("G28 X0 Y0\n")
        
        self.beeConnect.close()
        
        return
    
    """*************************************************************************
                                homeZ Method 
    
    *************************************************************************"""
    def homeZ(self):
        
        self.beeConnect = BEEConnect.Connection()
        
        self.SendAndWait("G28 Z0\n")
        
        self.beeConnect.close()
        
        return
    
    """*************************************************************************
                                move Method 
    
    *************************************************************************"""
    def move(self,x=None,y=None,z=None,e=None):
        
        self.beeConnect = BEEConnect.Connection()
        resp = self.beeConnect.dispatch("M121\n")
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
        
        self.SendAndWait(commandStr)
        
        self.beeConnect.close()
        
        return
    
    """*************************************************************************
                                GoToFirstCalibrationPoint Method 
    
    *************************************************************************"""
    def GoToFirstCalibrationPoint(self):
        
        self.beeConnect = BEEConnect.Connection()
        
        
        #go to home
        self.SendAndWait("G28\n")
        
        #set feedrate
        resp = self.beeConnect.dispatch("G1 F15000\n")
        print(resp)
        
        #set acceleration
        resp = self.beeConnect.dispatch("M206 X400\n")
        print(resp)
        
        #go to first point
        self.SendAndWait("G1 X0 Y67 Z2\n")
        
        #set acceleration
        resp = self.beeConnect.dispatch("M206 X1000\n")
        print(resp)
        
        
        self.beeConnect.close() 
        
        return
    
    """*************************************************************************
                                GoToSecondCalibrationPoint Method 
    
    *************************************************************************"""
    def GoToSecondCalibrationPoint(self):
        
        self.beeConnect = BEEConnect.Connection()
        
        #set feedrate
        resp = self.beeConnect.dispatch("G1 F5000\n")
        print(resp)
        #set acceleration
        resp = self.beeConnect.dispatch("M206 X400\n")
        print(resp)
        
        self.move(0,0,10,0)
        #go to SECOND point
        resp = self.beeConnect.dispatch("G1 X-31 Y-65\n")
        print(resp)
        self.move(0,0,-10,0)
        
        
        self.beeConnect.close() 
        
        return
    
    """*************************************************************************
                                GoToThirdCalibrationPoint Method 
    
    *************************************************************************"""
    def GoToThirdCalibrationPoint(self):
        
        self.beeConnect = BEEConnect.Connection()
        
        #set feedrate
        resp = self.beeConnect.dispatch("G1 F1000\n")
        print(resp)
        #set acceleration
        resp = self.beeConnect.dispatch("M206 X400\n")
        print(resp)
        
        self.move(0,0,10,0)
        #go to SECOND point
        resp = self.beeConnect.dispatch("G1 X35 Y65\n")
        print(resp)
        self.move(0,0,-10,0)
        
        self.beeConnect.close() 
        
        return