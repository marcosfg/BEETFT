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
import platform

class FileFinder():
    
    absPath = None
    currentDir = None
    absDirPath = None
    
    """*************************************************************************
                                Init Method 
    
    
    *************************************************************************"""
    def __init__(self):
        
        self.currentDir = os.getcwd()
        
        dirSplit = self.currentDir.split("/")
        if dirSplit[len(dirSplit)-1] != "BEETFT":
            if dirSplit[len(dirSplit)-1] == "src":
                self.absDirPath = self.currentDir + "/"
            else:
                self.absDirPath = self.currentDir + "/BEETFT/"
        else:
            self.absDirPath = self.currentDir + "/"
        
        pSystem = platform.system()
        if pSystem == "Darwin":
            self.absDirPath = "/Users/marcosgomes/NetBeansProjects/BEETFT/src/"
            
        return
    
    """*************************************************************************
                                GetAbsolutePath Method 
    
    
    *************************************************************************"""
    def GetAbsPath(self, relPath):
        """
        path = ""
        if relPath.find("Fonts/") >= 0:
            
            strDir = os.path.dirname(os.path.abspath(relPath))
            fontPos = strDir.find("/Fonts")
            
            strDir = strDir[:fontPos]
            
            print(strDir)
            
            if strDir.find("BEETFT") < 0:
                strDir = strDir+ "/BEETFT/"
            
            path = strDir + "/" + relPath
            
        elif relPath.find("Images/") >= 0:
            strDir = os.path.dirname(os.path.abspath(relPath))
            fontPos = strDir.find("/Images")
            
            strDir = strDir[:fontPos]
            
            print(strDir)
            
            if strDir.find("BEETFT") < 0:
                strDir = strDir+ "/BEETFT/"
            
            path = strDir + "/" + relPath
        else:
            path = os.path.dirname(os.path.abspath(relPath)) + "/" + relPath
            
            if path.find("BEETFT") < 0:
                path = os.path.dirname(os.path.abspath(relPath)) + "/BEETFT/" + relPath
        
        print("Loading File: ",path)
        
        return path
        """
        path = self.absDirPath + relPath
        
        return path