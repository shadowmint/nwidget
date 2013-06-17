# Copyright 2011 Douglas Linder
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from optparse import OptionParser
from subprocess import call
import os
import sys
import platform

class TestHelper:
  """ Helper class to find and run pyunit tests """

  __path = False

  __lib = False

  __tests = []

  __success = []

  __failed = []

  def __init__(self):
    pass

  def __findTests(self, path):
    """ Returns an array of files from target, as absolute paths. """
    if os.path.exists(path) and os.path.isdir(path):
      d = os.listdir(path)
      for name in d:
        if os.path.isdir(path + "/" + name):
          self.__findTests(path + "/" + name)
        elif name.endswith("tests.py"):
          self.__tests.append({ 'path' : os.path.abspath(path), 'test' : name })

  def __errorArgs(self):
    """ Prints an error message. """
    if not self.__path:
      print("Error: missing --path")
    if not self.__lib:
      print("Error: missing --lib")
    print("Invalid command. Try --help")
    exit(1)

  def __getArgs(self):
    """ Get command line arguments """
    parser = OptionParser()
    parser.add_option("-p", "--path", dest="path", help="test root", metavar="PATH")
    parser.add_option("-l", "--lib", dest="lib", help="library root", metavar="LIB")
    options = parser.parse_args()[0]
    if (not options.__dict__['path'] is None):
      self.__path = options.__dict__["path"]
    else:
      if os.getcwd().endswith("tests"):
        self.__path = os.path.join(os.getcwd())
      else:
        self.__path = os.path.join(os.getcwd(), "tests")
      print("Not --path specified, assumed: %s" % self.__path)
    if (not options.__dict__['lib'] is None):
      self.__lib = os.path.abspath(options.__dict__["lib"])
    else:
      if os.getcwd().endswith("tests"):
        self.__lib = os.path.join(os.getcwd(), os.pardir)
      else:
        self.__lib = os.getcwd() 
      print("Not --lib specified, assumed: %s" % self.__path)

  def __runTest(self, test):
    """ Run a single py unit test """
    success = False
    os.chdir(os.path.abspath(test['path']))
    if not platform.system() == "Windows":
      cmd = "PYTHONPATH=" + os.path.abspath(self.__lib) + " "
      cmd += "arch -i386 " + sys.executable + " " + os.path.abspath(test['test'])
    else:
      cmd = sys.executable + " " + os.path.abspath(test['test'])
    print(cmd)
    status = call(cmd, shell=True)
    if (status == 0):
      success = True
    return success

  def runTests(self):
    """ Find all the tests, run all the tests. """
    root = os.getcwd()
    self.__getArgs()
    self.__findTests(self.__path)
    if (len(self.__tests) > 0):
      for test in self.__tests:
        if self.__runTest(test):
          self.__success.append(test)
        else:
          self.__failed.append(test)
        os.chdir(root) # Reset to root

  def summary(self):
    """ Print a summary of events. """
    rtn = 0
    print("")
    for success in self.__success:
      print("success: " + success['path'] + "/" + success['test'])
    for fail in self.__failed:
      print(" FAILED: " + fail['path'] + "/" + fail['test'])
    total = len(self.__success) + len(self.__failed)
    print("\n" + str(len(self.__success)) + "/" + str(total) + " test sets passed")
    if len(self.__failed) > 0:
      rtn = 1
    return rtn

helper = TestHelper()
helper.runTests()
testsResult = helper.summary()
exit(testsResult)
