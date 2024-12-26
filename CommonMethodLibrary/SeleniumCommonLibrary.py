from pythonframework.FrameworkCore.SeleniumConfiguration.SeleniumConfiguration import TestResult, State
from pythonframework.FrameworkCore.CoreLibrary.SeleniumCoreLibrary import SeleniumCoreLibrary


class SeleniumCommonLibrary:


  def __init__(self, FrameworkInitializer):
    self.Driver = FrameworkInitializer.Driver
    self.AppiumDriver = FrameworkInitializer.AppiumDriver
    self.AppiumAndroidDriver = FrameworkInitializer.AppiumAndroidDriver
    self.AppiumIosDriver = FrameworkInitializer.AppiumIosDriver
    self.AppiumServer = None
    self.ObjTestResult = FrameworkInitializer.ObjTestResult
    self.FrameworkInitializer = FrameworkInitializer
    self.ObjSeleniumConfiguration = FrameworkInitializer.ObjSeleniumConfiguration
    self.ObjectRepository = FrameworkInitializer.ObjectRepository
    self.FrameworkCommonLibrary = FrameworkInitializer.ObjFrameworkCommon


  def SetValueInEditBox(self, strEnteredTestValue, ParentTestObjectName, ChildTestObjectName, EditBoxLength=0,
                        state=State.Enable):

    result = TestResult.Fail
    try:
      locatortype, locatorvalue, index = self.FrameworkCommonLibrary.GetElementInfoFromOldOR(ParentTestObjectName,
                                                                                             ChildTestObjectName)
      ObjSeleniumCoreLib = SeleniumCoreLibrary(self.FrameworkInitializer)
      ObjSeleniumCoreLib.SetValueInInputBox(
                                            LocatorType=locatortype,
                                            LocatorValue=locatorvalue,
                                            Index=int(index),
                                            strEnteredTestValue=strEnteredTestValue,
                                            state=state,
                                            EditBoxLength =EditBoxLength
                                          )


    except Exception as e:
      result = TestResult.Fail
      errors = str(e.args)
      e.__cause__ = None
      self.FrameworkCommonLibrary.ObjTestResult.WriteResultInResultReport(
        "error in  SetValueInEditBox " + errors, "fail")
      return result


  def SelectValueInListBox(self, strListItemValue, ParentTestObjectName, ChildTestObjectName,
                           state=State.Enable):
    try:
      locatortype, locatorvalue, index = self.FrameworkCommonLibrary.GetElementInfoFromOldOR(ParentTestObjectName, ChildTestObjectName)
      ObjSeleniumCoreLib = SeleniumCoreLibrary(self.FrameworkInitializer)
      ObjSeleniumCoreLib.SelectValueInListBox(
                                              LocatorType = locatortype,
                                              LocatorValue = locatorvalue,
                                              Index = int(index),
                                              strListItemValue = strListItemValue,
                                              state = state
                                            )

    except Exception as e:
      result = TestResult.Fail
      errors = str(e.args)
      e.__cause__ = None
      self.FrameworkCommonLibrary.ObjTestResult.WriteResultInResultReport(
        "error in  SelectValueInListBox " + errors, "fail")
      return result


  def Click(self, ParentTestObjectName, ChildTestObjectName):

    try:
      locatortype, locatorvalue, index = self.FrameworkCommonLibrary.GetElementInfoFromOldOR(ParentTestObjectName,
                                                                                             ChildTestObjectName)
      ObjSeleniumCoreLib = SeleniumCoreLibrary(self.FrameworkInitializer)
      ObjSeleniumCoreLib.Click(
                                LocatorType=locatortype,
                                LocatorValue=locatorvalue,
                                Index=int(index)
                              )

    except Exception as e:
      errors = str(e.args)
      e.__cause__ = None
      self.FrameworkCommonLibrary.ObjTestResult.WriteResultInResultReport(
        "Error in  Click " + errors, "Fail")
      return False


  def GetTextMessage(self, ParentTestObjectName, ChildTestObjectName):
    TextMessage = ""
    try:
      locatortype, locatorvalue, index = self.FrameworkCommonLibrary.GetElementInfoFromOldOR(ParentTestObjectName,
                                                                                             ChildTestObjectName)
      ObjSeleniumCoreLib = SeleniumCoreLibrary(self.FrameworkInitializer)
      TextMessage = ObjSeleniumCoreLib.GetTextMessage(
                                                        LocatorType=locatortype,
                                                        LocatorValue=locatorvalue,
                                                        Index=int(index)
                                                      )
      return TextMessage

    except Exception as e:
      errors = str(e.args)
      e.__cause__ = None
      self.FrameworkCommonLibrary.ObjTestResult.WriteResultInResultReport(
        "error in  Click " + errors, "Fail")
      return TextMessage



  def OpenApplication(self, strURL):
    try:

      if strURL is not None:

        ObjSeleniumCoreLib = SeleniumCoreLibrary(self.FrameworkInitializer)
        ObjSeleniumCoreLib.OpenApplication(strURL)
      else:
        self.FrameworkCommonLibrary.ObjTestResult.WriteResultInResultReport(
          "Fail to navigate URL-" + str(strURL) + " URL should not be null", "Fail")

    except:
      return False


  def AcceptAlertMessages(self):
    try:
      if self.IsAlertPresent():
        ObjSeleniumCoreLib = SeleniumCoreLibrary(self.FrameworkInitializer)
        ObjSeleniumCoreLib.AcceptAlertMessages()
    except Exception as e:
      errors = str(e.args)
      e.__cause__ = None
      self.FrameworkCommonLibrary.ObjTestResult.WriteResultInResultReport(
        "error in  AcceptAlertMessages " + errors, "fail")
      return False


  def IsAlertPresent(self):
    try:
      ObjSeleniumCoreLib = SeleniumCoreLibrary(self.FrameworkInitializer)
      result = ObjSeleniumCoreLib.IsAlertPresent()
      return result
    except Exception as e:
      errors = str(e.args)
      e.__cause__ = None
      self.FrameworkCommonLibrary.ObjTestResult.WriteResultInResultReport(
        "error in  IsAlertPresent " + errors, "fail")
      return False


  def ScreenCapture(self, strTextMessage):
    try:
      if self.ObjSeleniumConfiguration.IsAppium is not True:
        ObjSeleniumCoreLib = SeleniumCoreLibrary(self.FrameworkInitializer)
        result = ObjSeleniumCoreLib.ScreenCapture(strTextMessage)
        return result
    except Exception as e:
      e.__cause__ = None
      self.ObjTestResult.WriteResultInResultReport("Error in ScreenCapture " + str(e.args),"Fail")
      return False


  def HideKeyboard(self):
      try:
        keyboard = self.FrameworkInitializer.AppiumDriver.keyboard
        if keyboard is not None:
          self.FrameworkInitializer.AppiumDriver.hide_keyboard()
      except Exception as exc:
        exc.__cause__ = None


  def SetDateInCalender(self, ParentTestObjectName, ChildTestObjectName ,dateText):
    try:
      locatortype, locatorvalue, index = self.FrameworkCommonLibrary.GetElementInfoFromOldOR(ParentTestObjectName,
                                                                                             ChildTestObjectName)
      ObjSeleniumCoreLib = SeleniumCoreLibrary(self.FrameworkInitializer)
      ObjSeleniumCoreLib.SetDateInCalender(
                                            LocatorType=locatortype,
                                            LocatorValue=locatorvalue,
                                            Index=int(index),
                                            dateText=dateText
                                          )


    except Exception as e:
      errors = str(e.args)
      e.__cause__ = None
      self.FrameworkCommonLibrary.ObjTestResult.WriteResultInResultReport(
        "Error in  SetDateInCalender " + errors, "Fail")
      return


