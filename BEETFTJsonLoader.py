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


import json
import BEETFTDisplay
import BEETFT_Button
import PrinterInfoLoader
import JogLoader
import CalibrationLoader
import FilamentChangeLoader
import SettingsLoader
import FileBrowserLoader
import AboutLoader

class jsonLoader():
    
    """
    Json vars
    """
    jsonPath = "BEETFTConfig.json"
    displayJsonPath = "DisplayConfig.json"
    leftMenuJsonPath = "LeftMenuButtonsConfiguration.json"
    printerInfoJsonPath = "PrinterInfoConfiguration.json"
    jogJsonPath = "JogConfiguration.json"
    calibrationJsonPath = "CalibrationConfiguration.json"
    filamentChangeJsonPath = "FilamentChangeConfiguration.json"
    
    """
    Display Configuration class
    """
    displayData = None
    display = None
    displayObject = None
    
    """
    Left Menu Configuration
    """
    leftMenu = []
    leftMenuButtons = []
    defaultScreen = ""
    
    """
    Interface Configuration
    """
    interfaces = []
    printerInfoInterface = None
    jogInterface = None
    calibrationInterface = None
    filamentChangeInterface = None
    settingsInterface = None
    fileBrowserInterface = None
    aboutInterface = None
    
    """*************************************************************************
                                Init Method 
    
    Loads Json file
    *************************************************************************"""
    def __init__(self):
        
        """
        Load & Parse Json File
        """
        print("Loading Json configuration file")
        f = open(self.jsonPath,'r')                     #load json as text file
        jsonData = json.load(f)                         #parse the json file
        #self.display = jsonData.get('display')          #get the display list from json file
        #self.leftMenu = jsonData.get('leftMenu')        #get the leftPanel list from json file
        self.interfaces = jsonData.get('interfaces')      #get the interface list from json file
        f.close()                                       #close the file
        
        """
        Get Display Configuration
        """
        f = open(self.displayJsonPath,'r')                      #load json as text file
        displayData = json.load(f)                              #parse the json file
        self.display = displayData.get('display')               #get the display list from json file
        displayJson = json.loads(json.dumps(self.display[0]))
        self.defaultScreen = displayJson['DefaultScreen']
        self.displayObject = BEETFTDisplay.Display(
                displayJson['Name'],
                int(displayJson['Width']),
                int(displayJson['Height']),
                displayJson['bgColor'],
                int(displayJson['SplitLinePos']),
                displayJson['SplitLineColor'],
                int(displayJson['SplitLineThickness']))
        
        f.close()                                                   #close the file
        
        """
        Get Left Menu Buttons Configuration
        """
        f = open(self.leftMenuJsonPath,'r')                          #load json as text file
        menuData = json.load(f)                                     #parse the json file
        self.leftMenu = menuData.get('leftMenu')                    #get the leftPanel list from json file
        for btn in self.leftMenu:
            btnJson = json.loads(json.dumps(btn))
            title = btnJson['Title']
            pos = btnJson['Pos']
            splitPos = pos.split(",")
            x = int(splitPos[0])
            y = int(splitPos[1])
            
            size = btnJson['Size']
            splitSize = size.split("x")
            width = int(splitSize[0])
            height = int(splitSize[1])
            
            #btnType = btnJson['ButtonType']
            
            bgColor = btnJson['bgColor']
            splitBGColor = bgColor.split(",")
            bgR = int(splitBGColor[0])
            bgG = int(splitBGColor[1])
            bgB = int(splitBGColor[2])
            
            fColor = btnJson['fontColor']
            splitFColor = fColor.split(",")
            fR = int(splitFColor[0])
            fG = int(splitFColor[1])
            fB = int(splitFColor[2])
            
            fType = btnJson['fType']
            fSize = int(btnJson['fSize'])
            
            beeBtn = BEETFT_Button.Button(x,y,width,height,title,bgR,bgG,bgB,fR,fG,fB,fType,fSize)
            newBtn = beeBtn.GetTextButton()
            newBtn._propSetName(title)
            self.leftMenuButtons.append(newBtn)
        
        f.close()                                                   #close the file
            
        """
        Get Printer Info Interface Configuration
        """
        f = open(self.printerInfoJsonPath,'r')                          #load json as text file
        printerInfoData = json.load(f)                              #parse the json file
        printerInfo = printerInfoData['PrinterInfo']                #Get Printer Info
        printerInfoJson = json.loads(json.dumps(printerInfo[0]))    #Convert text to json
        self.printerInfoInterface = PrinterInfoLoader.PrinterInfoLoader(printerInfoJson)    #create interface
        f.close()                                                   #close the file
        
        """
        Get Jog Interface Configuration
        """
        f = open(self.jogJsonPath,'r')                          #load json as text file
        jogData = json.load(f)                                     #parse the json file
        jog = jogData['Jog']                #Get Jog configuration text
        jogJson = json.loads(json.dumps(jog[0]))    #Convert text to json
        self.jogInterface = JogLoader.JogLoader(jogJson)    #create interface
        f.close()                                            #close the file
        
        """
        Get Calibration Interface Configuration
        """
        f = open(self.calibrationJsonPath,'r')                          #load json as text file
        calibrationData = json.load(f)                                     #parse the json file
        calibration = calibrationData['Calibration']                #Get Calibration configuration text
        calibrationJson = json.loads(json.dumps(calibration[0]))    #Convert text to json
        self.calibrationInterface = CalibrationLoader.CalibrationLoader(calibrationJson)    #create interface
        f.close()                                            #close the file
        
        """
        Get Filament Change Interface Configuration
        """
        f = open(self.filamentChangeJsonPath,'r')                          #load json as text file
        filamentChangeData = json.load(f)                                     #parse the json file
        filamentChange = filamentChangeData['FilamentChange']                #Get Jog configuration text
        filamentChangeJson = json.loads(json.dumps(filamentChange[0]))    #Convert text to json
        self.filamentChangeInterface = FilamentChangeLoader.FilamentChangeLoader(filamentChangeJson)    #create interface
        f.close()                                            #close the file
        
        for interface in self.interfaces:
            interfaceJson = json.loads(json.dumps(interface))
            interfaceName = interfaceJson['InterfaceName']
            #if interfaceName == "PrinterInfo":
            #    self.printerInfoInterface = PrinterInfoLoader.PrinterInfoLoader(interfaceJson)
            #if interfaceName == "Jog":
            #    self.jogInterface = JogLoader.JogLoader(interfaceJson)
            #if interfaceName == "Calibration":
            #    self.calibrationInterface = CalibrationLoader.CalibrationLoader(interfaceJson)
            #if interfaceName == "FilamentChange":
            #    self.filamentChnageInterface = FilamentChangeLoader.FilamentChangeLoader(interfaceJson)
            if interfaceName == "Settings":
                self.settingsInterface = SettingsLoader.SettingsLoader(interfaceJson)
            elif interfaceName == "FileBrowser":
                self.fileBrowserInterface = FileBrowserLoader.FileBrowserLoader(interfaceJson)
            elif interfaceName == "About":
                self.aboutInterface = AboutLoader.AboutLoader(interfaceJson)
            
    
    """
    GetPrinterInfoInterface(self)
    
    Loads configuration for Printer Info Screen
    """
    def GetPrinterInfoInterface(self):
        
        return self.printerInfoInterface
    
    """
    GetJogInterface(self)
    
    Loads configuration or Jog Screen
    """
    def GetJogInterface(self):
        
        return self.jogInterface
    
    """
    GetCalibrationInterface(self)
    
    Loads configuration or Calibration Screen
    """
    def GetCalibrationInterface(self):
        
        return self.calibrationInterface
    
    """
    GetFilamentChangeInterface(self)
    
    Loads configuration or Filament Change Screen
    """
    def GetFilamentChangeInterface(self):
        
        return self.filamentChangeInterface
    
    """
    GetSettingsInterface(self)
    
    Loads configuration or Settings Screen
    """
    def GetSettingsInterface(self):
        
        return self.settingsInterface
    
    """
    GetFileBrowserInterface(self)
    
    Loads configuration or File Browser Screen
    """
    def GetFileBrowserInterface(self):
        
        return self.fileBrowserInterface
    
    """
    GetAboutInterface(self)
    
    Loads configuration or About Screen
    """
    def GetAboutInterface(self):
        
        return self.aboutInterface
    
    
    """
    GetLeftButtonsList(self)
    
    returns the list with the left menu buttons
    """
    def GetLeftButtonsList(self):
        
        return self.leftMenuButtons
    
    
    """
    GetDefaultScreen(self)
    
    returns the default screen
    """
    def GetDefaultScreen(self):
        
        return self.defaultScreen
