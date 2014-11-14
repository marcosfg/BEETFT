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

import PrintingLoader

class jsonLoader():
    
    """
    Json vars
    """
    #jsonPath = "BEETFTConfig.json"
    displayJsonPath = "/home/pi/BEETFT/DisplayConfig.json"
    leftMenuJsonPath = "/home/pi/BEETFT/LeftMenuButtonsConfiguration.json"
    printerInfoJsonPath = "/home/pi/BEETFT/PrinterInfoConfiguration.json"
    jogJsonPath = "/home/pi/BEETFT/JogConfiguration.json"
    calibrationJsonPath = "/home/pi/BEETFT/CalibrationConfiguration.json"
    filamentChangeJsonPath = "/home/pi/BEETFT/FilamentChangeConfiguration.json"
    settingsJsonPath = "/home/pi/BEETFT/SettingsConfiguration.json"
    fileBrowserJsonPath = "/home/pi/BEETFT/FileBrowserConfiguration.json"
    aboutJsonPath = "/home/pi/BEETFT/AboutConfiguration.json"
    
    printingJsonPath = "/home/pi/BEETFT/PrintingConfiguration.json"
    
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
    printerInfoInterface = None
    jogInterface = None
    calibrationInterface = None
    filamentChangeInterface = None
    settingsInterface = None
    fileBrowserInterface = None
    aboutInterface = None
    
    printingInterface = None
    
    """*************************************************************************
                                Init Method 
    
    Loads Json file
    *************************************************************************"""
    def __init__(self):
        
        
        
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
            btnName = btn['ButtonName']
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
            
            beeBtn = BEETFT_Button.Button(x,y,width,height,title,bgR,bgG,bgB,fR,fG,fB,fType,fSize,None,None,None,btnName)
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
        filamentChange = filamentChangeData['FilamentChange']                #Get Filament Chnage configuration text
        filamentChangeJson = json.loads(json.dumps(filamentChange[0]))    #Convert text to json
        self.filamentChangeInterface = FilamentChangeLoader.FilamentChangeLoader(filamentChangeJson)    #create interface
        f.close()                                            #close the file
        
        """
        Get Settings Interface Configuration
        """
        f = open(self.settingsJsonPath,'r')                            #load json as text file
        settingsData = json.load(f)                                    #parse the json file
        settings = settingsData['Settings']                                  #Get Settings configuration text
        settingsJson = json.loads(json.dumps(settings[0]))                #Convert text to json
        self.settingsInterface = SettingsLoader.SettingsLoader(settingsJson)    #create interface
        f.close()                                                   #close the file
        
        """
        Get File Browser Interface Configuration
        """
        f = open(self.fileBrowserJsonPath,'r')                          #load json as text file
        fileBrowserData = json.load(f)                                     #parse the json file
        fileBrowser = fileBrowserData['FileBrowser']                #Get File Browser configuration text
        fileBrowserJson = json.loads(json.dumps(fileBrowser[0]))    #Convert text to json
        self.fileBrowserInterface = FileBrowserLoader.FileBrowserLoader(fileBrowserJson)    #create interface
        f.close()                                            #close the file
        
        """
        Get About Interface Configuration
        """
        f = open(self.aboutJsonPath,'r')                            #load json as text file
        aboutData = json.load(f)                                    #parse the json file
        about = aboutData['About']                                  #Get About configuration text
        aboutJson = json.loads(json.dumps(about[0]))                #Convert text to json
        self.aboutInterface = AboutLoader.AboutLoader(aboutJson)    #create interface
        f.close()                                                   #close the file
        
        """
        Get About Interface Configuration
        """
        f = open(self.printingJsonPath,'r')                            #load json as text file
        printingData = json.load(f)                                    #parse the json file
        printing = printingData['Printing']                                  #Get About configuration text
        printingJson = json.loads(json.dumps(printing[0]))                #Convert text to json
        self.printingInterface = PrintingLoader.PrintingLoader(printingJson)    #create interface
        f.close()                                                   #close the file
        
        return
    
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
    GetPrintingInterface(self)
    
    Loads configuration or About Screen
    """
    def GetPrintingInterface(self):
        
        return self.printingInterface
    
    
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
