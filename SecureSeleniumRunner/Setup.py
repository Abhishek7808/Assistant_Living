"""
# Version = 1.0.0.0
# -------------------------------------------------------------------------------
# Name: Setup.py
# Purpose: To Initiate the clone process.
# Author: Vivek Purohit (44454)
# -------------------------------------------------------------------------------
"""
import sys
import os
sys.path[:0] = ['../../../']
from configparser import ConfigParser
from git import rmtree
from pythonframework.FrameworkCore.CommonHelper.Helper import Helper

class setup:
    """
    Purpose: To Initiate the clone process.
    """
    def __init__(self):
        self.obj_helper = Helper

    def clone_setup(self):
        """
        Clone the required framework pkg to the root folder, and installs the same
        :return:
        """

        config = ConfigParser()
        config.read('frameworksettings.ini')
        relative_path = config.get('DEFAULT', 'project_hirarchy')
        path=relative_path + str('Deliverables')

        isExist=os.path.exists(path)
        if isExist is True:
            try:
                rmtree(path)
            except Exception as e:
                print(str(e))

        self.obj_helper.git_clone(self,directory = path)


obj = setup()
obj.clone_setup()









