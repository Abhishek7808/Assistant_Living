from pythonframework.FrameworkCore.SeleniumConfiguration.SeleniumConfiguration import TestResult, State
from pythonframework.FrameworkCore.SeleniumConfiguration.SeleniumConfiguration import UserMessageList
from pythonframework.FrameworkCore.CoreLibrary.AppiumCoreLibrary import AppiumCoreLibrary


class Appium_Android:

  def __init__(self, FrameworkInitializer):
    self.ObjUserList = UserMessageList()
    self.FrameworkInitializer=FrameworkInitializer
    self.FrameworkCommonLibrary = FrameworkInitializer.ObjFrameworkCommon
    self.ObjSeleniumConfiguration = FrameworkInitializer.ObjSeleniumConfiguration
    self.AppiumAndroidDriver = FrameworkInitializer.AppiumAndroidDriver
    self.ObjTestResult = FrameworkInitializer.ObjTestResult
    self.elements = None


  def Click(self, ParentTestObjectName, ChildTestObjectName, Byscrooling=False):
    try:
      locatortype, locatorvalue, index = self.FrameworkCommonLibrary.GetElementInfoFromOldOR(ParentTestObjectName,
                                                                                             ChildTestObjectName)
      ObjAppiumCoreLib = AppiumCoreLibrary(self.FrameworkInitializer)

      result = ObjAppiumCoreLib.Click(
                                          LocatorType=locatortype,
                                          LocatorValue=locatorvalue,
                                          Index=int(index)
                                        )
      return  result

    except:
      return False


  def screenshot_android(self, filename, comment):

    try:
      ObjAppiumCoreLib = AppiumCoreLibrary(self.FrameworkInitializer)
      ObjAppiumCoreLib.screenshot_android(filename,comment)

    except Exception as e:
      print(str(e))


  def SetValueInEditBox(self, strEnteredTestValue, ParentTestObjectName, ChildTestObjectName, Byscrooling=False,
                        IsMaxlengthCheck=True,
                        state=State.Enable):

    result = TestResult.Fail
    EnteredTestValueLength = None
    try:
      locatortype, locatorvalue, index = self.FrameworkCommonLibrary.GetElementInfoFromOldOR(ParentTestObjectName,
                                                                                             ChildTestObjectName)

      ObjAppiumCoreLib = AppiumCoreLibrary(self.FrameworkInitializer)
      ObjAppiumCoreLib.SetValueInEditBox(
                                          LocatorType=locatortype,
                                          LocatorValue=locatorvalue,
                                          Index=int(index),
                                          strEnteredTestValue=strEnteredTestValue,
                                          Byscrooling=Byscrooling,
                                          state=state
                                        )


    except Exception as e:
      errortext = str(e)
      e.__cause__ = None
      return result



  def HideKeyboard(self):

    ObjAppiumCoreLib = AppiumCoreLibrary(self.FrameworkInitializer)
    ObjAppiumCoreLib.HideKeyboard()


  def WaitForElementTillPresent_Appium(self, ParentTestObjectName, ChildTestObjectName, TimesInSec):
    try:
      locatortype, locatorvalue, index = self.FrameworkCommonLibrary.GetElementInfoFromOldOR(ParentTestObjectName,
                                                                                             ChildTestObjectName)
      ObjAppiumCoreLib = AppiumCoreLibrary(self.FrameworkInitializer)
      result = ObjAppiumCoreLib.WaitForElementTillPresent_Appium(
                                                        LocatorType=locatortype,
                                                        LocatorValue=locatorvalue,
                                                        TimesInSec=int(TimesInSec)
                                                      )

      return result

    except Exception as e:
      e.__cause__ = None



  def VerifyElememnt(self, ParentTestObjectName, ChildTestObjectName):
    try:
      locatortype, locatorvalue, index = self.FrameworkCommonLibrary.GetElementInfoFromOldOR(ParentTestObjectName,
                                                                                             ChildTestObjectName)
      ObjAppiumCoreLib = AppiumCoreLibrary(self.FrameworkInitializer)
      result = ObjAppiumCoreLib.VerifyElememnt(
                                                LocatorType=locatortype,
                                                LocatorValue=locatorvalue,
                                                Index=int(index)
                                              )

      return result


    except Exception as e:
      self.FrameworkCommonLibrary.ObjTestResult.WriteResultInResultReport(ParentTestObjectName +
                                                                          "/" + ChildTestObjectName + " element Cannot verified on page getting error ",
                                                                          "Fail")
      e.__cause__ = None



  def VerifyText(self, ParentTestObjectName, ChildTestObjectName, text):
    try:
      locatortype, locatorvalue, index = self.FrameworkCommonLibrary.GetElementInfoFromOldOR(ParentTestObjectName,
                                                                                             ChildTestObjectName)
      ObjAppiumCoreLib = AppiumCoreLibrary(self.FrameworkInitializer)
      result = ObjAppiumCoreLib.VerifyText(
                                            LocatorType=locatortype,
                                            LocatorValue=locatorvalue,
                                            Index=int(index),
                                            text=text
                                          )

      return result

    except Exception as e:
      self.FrameworkCommonLibrary.ObjTestResult.WriteResultInResultReport(ParentTestObjectName +
                                                                          "/" + ChildTestObjectName + " " + " text Cannot verified on page getting error ",
                                                                          "Fail")
      e.__cause__ = None



  def ScreenCapture(self):
    try:
      ObjAppiumCoreLib = AppiumCoreLibrary(self.FrameworkInitializer)
      ObjAppiumCoreLib.ScreenCapture()

    except :
      pass



