# Import Pmw from this directory tree.
import os
import sys
import pathlib
print(os.getcwd())
from pythonframework.FrameworkCore.CommonHelper.Constants import Constants
from pythonframework.FrameworkCore.ReadExcelData.ReadExcel import ReadExcel
from pythonframework.FrameworkCore.SeleniumConfiguration.SeleniumConfiguration import SeleniumConfiguration
from pythonframework.FrameworkCore.TestResultReport.TestResultReport import TestResult
from pythonframework.FrameworkCore.FrameworkLibrary.FrameworkInitializer import FrameworkInitializer
from pythonframework.FrameworkCore.SeleniumConfiguration.SeleniumConfiguration import BackgroudWorker_aruList
from pythonframework.FrameworkCore.SeleniumConfiguration.SeleniumConfiguration import AppiumConfiguration
from pythonframework.FrameworkCore.CommonHelper.CommonEnum import CommonEnums, TestApplicationType
from pythonframework.FrameworkCore.TestResultReport.ColorPrint import ColorPrint
from pythonframework.FrameworkCore.SeleniumConfiguration.Constants import *


sys.path[:0] = ['../../../']
sys.path[:0] = ['../../']


class SecureSelenium:

  def __init__(self, AutomationFolderPath):
    self.AutomationFolderPath = AutomationFolderPath
    self.TestAutomationFolderNames = None
    self.SeleniumConfiguration = SeleniumConfiguration()
    self.BackgroundWorker_aruList = BackgroudWorker_aruList()
    self.AppiumConfiguration = AppiumConfiguration()
    self.FrameworkInitializer = None
    self.Folder_Existence = 0
    self.UserInfo = None


  def ValidateAutomationFolderStucture(self, strRootFolderpath):
    if pathlib.Path(strRootFolderpath).exists():
      self.SeleniumConfiguration.AutomationFolderPath = strRootFolderpath
      self.Folder_Existence = 1
    else:
      ColorPrint.PrintRed("root automation folder doesn't exists.")
      return False
    if self.Folder_Existence == 1:
      if pathlib.Path(strRootFolderpath + "\ControlFile").exists():

        self.SeleniumConfiguration.ControlFileFolderPath = strRootFolderpath + "\ControlFile"
      else:
        ColorPrint.PrintRed("ControlFile folder doesn't exists.")
        self.Folder_Existence = 0
        return False
    if self.Folder_Existence == 1:
      if pathlib.Path(strRootFolderpath + '\DataBase').exists():
        self.SeleniumConfiguration.TestDataFolderPath = strRootFolderpath + "\DataBase"
      else:
        ColorPrint.PrintRed("DataBase folder doesn't exists.")
        self.Folder_Existence = 0
        return False
    if self.Folder_Existence == 1:
      if pathlib.Path(strRootFolderpath + '\Keyword Sheets').exists():
        self.SeleniumConfiguration.Keyword_sheet_path = strRootFolderpath + "\Keyword Sheets"
      else:
        ColorPrint.PrintRed("Keyword sheets folder doesn't exists.")
        self.Folder_Existence = 0
        return False
    if self.Folder_Existence == 1:
      if pathlib.Path(strRootFolderpath + "\ObjectRepository").exists():
        self.SeleniumConfiguration.ObjectRepositryPath = strRootFolderpath + "\ObjectRepository"
      else:
        self.Folder_Existence = 0
        ColorPrint.PrintRed("ObjectRepository folder doesn't exists.")
        return False
    if self.Folder_Existence == 1:
      if pathlib.Path(strRootFolderpath + "\SeleniumLibraries").exists():
        self.SeleniumConfiguration.SeleniumLibraryFolderPath = strRootFolderpath + "\SeleniumLibraries"
      else:
        self.Folder_Existence = 0
        ColorPrint.PrintRed("SeleniumLibraries folder doesn't exists.")
        return False
    if self.Folder_Existence == 1:
      if pathlib.Path(strRootFolderpath + "\AutoRunConfigfile").exists():
        self.SeleniumConfiguration.SeleniumAutoRunConfigFolderPath = strRootFolderpath + "\AutoRunConfigfile"
      else:
        self.Folder_Existence = 0
        ColorPrint.PrintRed("AutoRunConfigfile folder doesn't exists.")
        return False
    if self.Folder_Existence == 1:
      if pathlib.Path("..\\..\\Resultlog").exists():
        self.SeleniumConfiguration.ResultFolderPath = "..\\..\\Resultlog"
        return True
      else:
        try:
          pathlib.Path("..\\..\\Resultlog").mkdir()
          ColorPrint.PrintRed("ResultLog folder doesn't exists and Created.")
          self.SeleniumConfiguration.ResultFolderPath = " ..\\..\\Resultlog"
          return True
        except Exception:
          return False
    if self.Folder_Existence == 1:
      return True



  def RunTest(self):
    self.SeleniumConfiguration.ObjectRepositryFilePath = self.SeleniumConfiguration.ObjectRepositryPath + "/" + self.SeleniumConfiguration.ORname
    self.TestResult = TestResult(self.SeleniumConfiguration, self.AppiumConfiguration)
    self.TestResult.CreateResult()
    controlfiles = pathlib.Path(self.SeleniumConfiguration.ControlFileFolderPath).glob('*.xlsx')
    self.FrameworkInitializer = FrameworkInitializer(self.TestResult, self.SeleniumConfiguration,
                                                     self.AppiumConfiguration)
    for cotrolfile in controlfiles:
      if cotrolfile.is_file() and '~$' not in cotrolfile.name:
        controlfilename = cotrolfile.name
        if controlfilename == 'KeywordControlFile.xlsx' :
          from pythonframework.FrameworkCore.FrameworkLibrary.ExecuteControlFile import ExecuteControlFile
          self.objExecuteControlFile = ExecuteControlFile()
          self.objExecuteControlFile.ControlFileExecution()
        else:
          self.SeleniumConfiguration.ControlFileName = controlfilename
          self.TestResult.WriteControlFileNameInResultInResultReport(controlfilename,"Control file Execution Started:")
          ColorPrint.PrintGreen(controlfilename + " Control file Execution Started:")
          self.FrameworkInitializer.ExecuteControlFile(cotrolfile.absolute())
          self.TestResult.WriteControlFileNameInResultInResultReport(controlfilename,"Control file Execution Ended:")
          ColorPrint.PrintGreen(controlfilename + " Control file Execution Ended:")



  def AgisnValuefromRow_SeleniumWeb(self, objreadexcel,datatable, rownum):
    self.UserInfo =""
    self.SeleniumConfiguration.IsAppium = False
    self.SeleniumConfiguration.IsLocalServer = True
    ControlFilepath = objreadexcel.GetDatafromTestDataTable(datatable, rownum, ConfigFile.ControlFilePath)
    if ControlFilepath != "":
      self.SeleniumConfiguration.ControlFileFolderPath = self.SeleniumConfiguration.ControlFileFolderPath + ControlFilepath
    else:
      self.UserInfo = self.UserInfo + "Control file path can not be blank!"
    orName = objreadexcel.GetDatafromTestDataTable(datatable, rownum, ConfigFile.ObjectRepositoryPath)
    if orName!="":
      self.SeleniumConfiguration.ORname = orName
      self.SeleniumConfiguration.ORname = orName
    else:
      self.UserInfo=self.UserInfo + "OR name can not be blank!"
    BrowserName = objreadexcel.GetDatafromTestDataTable(datatable, rownum, ConfigFile.BrowserName)
    self.SeleniumConfiguration.FrameworkType =  objreadexcel.GetDatafromTestDataTable(datatable, rownum, ConfigFile.FrameworkType)
    if BrowserName != "":
      self.SeleniumConfiguration.BrowserName = BrowserName
    else:
      self.UserInfo = self.UserInfo + "Browser name can not be null!"
    if self.UserInfo!="":
      ColorPrint.PrintRed(self.UserInfo)
      return False
    else:
      return True



  def AgisnValuefromRow_android(self, objreadexcel,datatable, rownum):
    self.UserInfo =""
    self.SeleniumConfiguration.IsAppium = True
    self.SeleniumConfiguration.MobileOS = 1
    self.AppiumConfiguration.PlateformName="Android"
    self.SeleniumConfiguration.IsLocalServer = False

    DeviceName = objreadexcel.GetDatafromTestDataTable(datatable, rownum, ConfigFile.DeviceName)

    if DeviceName!="":
      self.AppiumConfiguration.UseDeviceName = DeviceName

    else:
      self.UserInfo=self.UserInfo + "DeviceName can not be blank!"
    ControlFilepath = objreadexcel.GetDatafromTestDataTable(datatable, rownum, ConfigFile.ControlFilePath)
    self.SeleniumConfiguration.FrameworkType = objreadexcel.GetDatafromTestDataTable(datatable, rownum,
                                                                                     ConfigFile.FrameworkType)

    if ControlFilepath != "":
      self.SeleniumConfiguration.ControlFileFolderPath = self.SeleniumConfiguration.ControlFileFolderPath+ControlFilepath
    else:
      self.UserInfo = self.UserInfo + "Control file path can not be blank!"
    orName = objreadexcel.GetDatafromTestDataTable(datatable, rownum, ConfigFile.ObjectRepositoryPath)
    if orName != "":
      self.SeleniumConfiguration.ORname = orName
    else:
      self.UserInfo = self.UserInfo + "OR name can not be blank!"

    AppType = objreadexcel.GetDatafromTestDataTable(datatable, rownum, ConfigFile.MobileApplicationType)
    if AppType != "Web":
      App = objreadexcel.GetDatafromTestDataTable(datatable, rownum, ConfigFile.ApplicationFilePath)
      if App!="":
        self.AppiumConfiguration.ApplicationPath = App
      else:
        self.UserInfo = self.UserInfo + "Please enter the App name as per service provider."
    CommandTimeOut = objreadexcel.GetDatafromTestDataTable(datatable, rownum, ConfigFile.CommandTimeout)
    if CommandTimeOut != "":
      self.AppiumConfiguration.newCommandTimeout = CommandTimeOut
    else:
      self.UserInfo = self.UserInfo + "CommandTimeOut can not be blank!"
    AutomationName = objreadexcel.GetDatafromTestDataTable(datatable, rownum, ConfigFile.AutomationName)
    if AutomationName != "":
      self.AppiumConfiguration.AutomationName = AutomationName
    else:
      self.UserInfo = self.UserInfo + "AutomationName can not be blank!"
    BrowserName = objreadexcel.GetDatafromTestDataTable(datatable, rownum, ConfigFile.BrowserName)
    if BrowserName != "":
      self.AppiumConfiguration.AutomationName = BrowserName
    else:
      self.UserInfo = self.UserInfo + "Browser Name can not be blank!"
    AppType = objreadexcel.GetDatafromTestDataTable(datatable, rownum, ConfigFile.ApplicationType)
    if AppType != "":
      if AppType==MobileApplicationType.Web:
        self.AppiumConfiguration.Script_Apptype=CommonEnums.Android_Web
      elif AppType==MobileApplicationType.Native:
        self.AppiumConfiguration.Script_Apptype = CommonEnums.Android_Native
      elif AppType == MobileApplicationType.Hybrid:
        self.AppiumConfiguration.Script_Apptype = CommonEnums.Android_Hybrid
    else:
      self.UserInfo = self.UserInfo + "App Type can not be blank!"
    DevicePlateformVersion = objreadexcel.GetDatafromTestDataTable(datatable, rownum, ConfigFile.DevicePlatfromVersion)

    if DevicePlateformVersion != "":
      self.AppiumConfiguration.DevicePlateformVersion = DevicePlateformVersion
      self.AppiumConfiguration.PlatformVersion=DevicePlateformVersion
    else:
      self.UserInfo = self.UserInfo + "Device Plateform Version can not be blank!"
    Autowebview = objreadexcel.GetDatafromTestDataTable(datatable, rownum, ConfigFile.AutoWebView)
    if Autowebview == "true":
      self.AppiumConfiguration.Autowebview = True
    else:
      self.AppiumConfiguration.Autowebview = False
    IgnoreUnimportantView = objreadexcel.GetDatafromTestDataTable(datatable, rownum, ConfigFile.IgnorUnimportantView)
    if Autowebview == "true":
      self.AppiumConfiguration.IgnoreUnimportantView = True
    else:
      self.AppiumConfiguration.IgnoreUnimportantView = False
    if self.UserInfo!="":
      ColorPrint.PrintRed(self.UserInfo)
      return False
    else:
      return True



  def AgisnValuefromRow_IOS(self, objreadexcel, datatable, rownum):
    self.UserInfo = ""
    self.SeleniumConfiguration.IsAppium = True
    self.SeleniumConfiguration.MobileOS = 2
    self.AppiumConfiguration.PlateformName = "IOS"
    self.SeleniumConfiguration.IsLocalServer = False
    self.SeleniumConfiguration.FrameworkType = objreadexcel.GetDatafromTestDataTable(datatable, rownum,
                                                                                     ConfigFile.FrameworkType)

    ControlFilepath = objreadexcel.GetDatafromTestDataTable(datatable, rownum, ConfigFile.ControlFilePath)
    if ControlFilepath != "":
      self.SeleniumConfiguration.ControlFileFolderPath = self.SeleniumConfiguration.ControlFileFolderPath + ControlFilepath
    else:
      self.UserInfo = self.UserInfo + "Control file path can not be blank!"
    DeviceName = objreadexcel.GetDatafromTestDataTable(datatable, rownum, ConfigFile.DeviceName)
    if DeviceName != "":
      self.AppiumConfiguration.UseDeviceName = DeviceName
    else:
      self.UserInfo = self.UserInfo + "DeviceName can not be blank!"
    orName = objreadexcel.GetDatafromTestDataTable(datatable, rownum, ConfigFile.ObjectRepositoryPath)
    if orName != "":
      self.SeleniumConfiguration.ORname = orName
    else:
      self.UserInfo = self.UserInfo + "OR name can not be blank!"

    AppType = objreadexcel.GetDatafromTestDataTable(datatable, rownum, ConfigFile.MobileApplicationType)
    if AppType != "Web":
      App = objreadexcel.GetDatafromTestDataTable(datatable, rownum, ConfigFile.ApplicationFilePath)
      if App != "":
        self.AppiumConfiguration.ApplicationPath = App
      else:
        self.UserInfo = self.UserInfo + "Please enter the App name as per service provider."
    CommandTimeOut = objreadexcel.GetDatafromTestDataTable(datatable, rownum, ConfigFile.CommandTimeout)
    if CommandTimeOut != "":
      self.AppiumConfiguration.newCommandTimeout = CommandTimeOut
    else:
      self.UserInfo = self.UserInfo + "CommandTimeOut can not be blank!"
    AutomationName = objreadexcel.GetDatafromTestDataTable(datatable, rownum, ConfigFile.AutomationName)
    if AutomationName != "":
      self.AppiumConfiguration.AutomationName = AutomationName
    else:
      self.UserInfo = self.UserInfo + "AutomationName can not be blank!"
    BrowserName = objreadexcel.GetDatafromTestDataTable(datatable, rownum, ConfigFile.BrowserName)
    if BrowserName != "":
      self.AppiumConfiguration.AutomationName = BrowserName
    else:
      self.UserInfo = self.UserInfo + "Browser Name can not be blank!"
    AppType = objreadexcel.GetDatafromTestDataTable(datatable, rownum, ConfigFile.MobileApplicationType)
    if AppType != "":
      if AppType == MobileApplicationType.Web:
        self.AppiumConfiguration.Script_Apptype = CommonEnums.Android_Web
      elif AppType == MobileApplicationType.Native:
        self.AppiumConfiguration.Script_Apptype = CommonEnums.Android_Native
      elif AppType == MobileApplicationType.Hybrid:
        self.AppiumConfiguration.Script_Apptype = CommonEnums.Android_Hybrid
    else:
      self.UserInfo = self.UserInfo + "App Type can not be blank!"
    DevicePlateformVersion = objreadexcel.GetDatafromTestDataTable(datatable, rownum, ConfigFile.DevicePlatfromVersion)
    if DevicePlateformVersion != "":
      self.AppiumConfiguration.DevicePlateformVersion = DevicePlateformVersion
    else:
      self.UserInfo = self.UserInfo + "Device Plateform Version can not be blank!"
    Autowebview = objreadexcel.GetDatafromTestDataTable(datatable, rownum, ConfigFile.AutoWebView)
    if Autowebview == "true":
      self.AppiumConfiguration.Autowebview = True
    else:
      self.AppiumConfiguration.Autowebview = False
    IgnoreUnimportantView = objreadexcel.GetDatafromTestDataTable(datatable, rownum, ConfigFile.IgnorUnimportantView)
    if Autowebview == "true":
      self.AppiumConfiguration.IgnoreUnimportantView = True
    else:
      self.AppiumConfiguration.IgnoreUnimportantView = False
    if self.UserInfo != "":
      ColorPrint.PrintRed(self.UserInfo)
      return False
    else:
      return True



  def AgisnValuefromRow_WebService(self, objreadexcel,datatable, rownum):
    self.UserInfo =""
    ControlFilepath = objreadexcel.GetDatafromTestDataTable(datatable, rownum, ConfigFile.ControlFilePath)
    if ControlFilepath != "":
      self.SeleniumConfiguration.ControlFileFolderPath = self.SeleniumConfiguration.ControlFileFolderPath + ControlFilepath
    else:
      self.UserInfo = self.UserInfo + "Control file path can not be blank!"
    if self.UserInfo!="":
      ColorPrint.PrintRed(self.UserInfo)
      return False
    else:
      return True
  def RunwebserviceTest(self):
    try:
      self.TestResult = TestResult(self.SeleniumConfiguration, self.AppiumConfiguration)
      self.TestResult.CreateResult()
      controlfiles = pathlib.Path(self.SeleniumConfiguration.ControlFileFolderPath).glob('*.xlsx')
      self.FrameworkInitializer = FrameworkInitializer(self.TestResult, self.SeleniumConfiguration,
                                                       self.AppiumConfiguration)
      for cotrolfile in controlfiles:
        if cotrolfile.is_file() and '~$' not in cotrolfile.name:
          controlfilename = cotrolfile.name
          self.TestResult.WriteControlFileNameInResultInResultReport(controlfilename, "Control file Execution Started:")
          ColorPrint.PrintGreen(controlfilename + " Control file Execution Started:")
          self.FrameworkInitializer.ExecuteControlFileForWebApi(cotrolfile)
          self.TestResult.WriteControlFileNameInResultInResultReport(controlfilename, "Control file Execution Ended:")
          ColorPrint.PrintGreen(controlfilename + " Control file Execution Ended:")
    except Exception as e:
      errortext = str(e.args)
      ColorPrint.PrintRed("error in RunwebserviceTest as:-" + errortext+"Fail")



  def RunMainTest(self):
    print("[Info]: Version:" + self.SeleniumConfiguration.ProjectVersion)
    if self.ValidateAutomationFolderStucture(self.AutomationFolderPath):
      configfiles = pathlib.Path(self.SeleniumConfiguration.SeleniumAutoRunConfigFolderPath).glob('*.xlsx')
      for config in configfiles:
        if config.is_file() and '~$' not in config.name:
          objexcel = ReadExcel()
          DTconfiglFile = objexcel.GetExcelData(TestDataFilePath=config)
          if DTconfiglFile is not None:
            IntAction = 0

            for i in range(len(DTconfiglFile.index)):
              Action = objexcel.GetDatafromTestDataTable(DTconfiglFile, i, ConfigFile.Action)
              IntAction = int(Action)
              if IntAction == 1:
                self.SeleniumConfiguration.ControlFileFolderPath = self.AutomationFolderPath + "\ControlFile"
                self.SeleniumConfiguration.AutomationApproach = ""
                self.SeleniumConfiguration.ORFormat = ""
                AppilcationType = objexcel.GetDatafromTestDataTable(DTconfiglFile, i, Constants.TestApplicationType)
                if TestApplicationType.WebApp.name == AppilcationType:
                  """ColorPrint.PrintGreen("[Info]: Test type " + TestApplicationType.WebApp.name + " started, iteration number:-" + str(
                    i+1) + " config file name is " + config.name)"""
                  if(self.AgisnValuefromRow_SeleniumWeb(objexcel, DTconfiglFile, i)):
                    self.RunTest()
                  else:
                    ColorPrint.PrintRed("invalid data in config filr , test interation "+str(i+1)+ "information list "+self.UserInfo)
                  """ColorPrint.PrintGreen(
                  "Test type " + TestApplicationType.WebApp.name + " ended, iteration number:-" + str(
                    i + 1) + " config file name is " + config.name)"""

                elif TestApplicationType.MobileApp_Android.name == AppilcationType:
                  ColorPrint.PrintGreen("Test type " + TestApplicationType.MobileApp_Android.name + " started, iteration number:-" + str(
                    i+1) + " config file name is " + config.name)
                  if(self.AgisnValuefromRow_android(objexcel, DTconfiglFile, i)):
                    self.RunTest()
                  else:
                    ColorPrint.PrintRed("invalid data in config file , test interation "+str(i+1)+ "information list "+self.UserInfo)
                  ColorPrint.PrintGreen("Test type " + TestApplicationType.MobileApp_Android.name + " ended, iteration number:-" + str(
                    i + 1) + " config file name is " + config.name)

                elif TestApplicationType.MobileApp_IOS.name == AppilcationType:
                  ColorPrint.PrintGreen("Test type " + TestApplicationType.MobileApp_IOS.name + " started, iteration number:-" + str(
                    i+1) + " config file name is " + config.name)
                  if (self.AgisnValuefromRow_IOS(objexcel, DTconfiglFile, i)):
                    self.RunTest()
                  else:
                    ColorPrint.PrintRed("invalid data in config filr , test interation " + str(
                      i + 1) + "information list " + self.UserInfo)
                  ColorPrint.PrintGreen(
                    "Test type " + TestApplicationType.MobileApp_IOS.name + " ended, iteration number:-" + str(
                      i + 1) + " config file name is " + config.name)

                elif TestApplicationType.WebService.name == AppilcationType:
                  ColorPrint.PrintGreen("Test type " + TestApplicationType.WebService.name + " started, iteration number:-" + str(
                    i+1) + " config file name is " + config.name)
                  self.SeleniumConfiguration.WebServiceType = 1
                  if (self.AgisnValuefromRow_WebService(objexcel, DTconfiglFile, i)):
                    self.RunwebserviceTest()
                  else:
                    ColorPrint.PrintRed("invalid data in config filr , test interation " + str(
                      i + 1) + "information list " + self.UserInfo)
                  ColorPrint.PrintGreen("Test type " + TestApplicationType.WebService.name + " ended, iteration number:-" + str(
                    i+1) + " config file name is " + config.name)

                elif TestApplicationType.WebSocket.name == AppilcationType:
                  self.SeleniumConfiguration.WebServiceType = 2
                  ColorPrint.PrintGreen("Test type " + TestApplicationType.WebSocket.name + " started, iteration number:-" + str(
                    i+1) + " config file name is " + config.name)
                else:
                  ColorPrint.PrintRed(
                    "Please define/check the valid test type in config file , given test type is " + AppilcationType + " config file name is " + config.name)
    else:
      ColorPrint.PrintRed("Folder structure is not valid")
