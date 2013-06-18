# Copyright 2013 Douglas Linder
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:
# 
#   http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
import os
import re
from collections import deque
from os.path import isdir, abspath, join, pardir

# Configure extra includes here
# eg. extras = [ abspath(join(os.getcwd(), pardir)) ]
extras = [ ]

class Bootstrap():
  """ Bootstrap for setting library paths
      
      Don't import this file into your project, actually copy it into
      your project directory and use it like this:

      import bootstrap
      
      What this does:

      - recurse upwards through the directory tree until finding a 'lib' folder.
      - add the lib folder the python path
      - decend into the lib folder and search for any sub folders named 'lib'
      - add them to the python path

      IE. Put your dependencies in lib/ like this:

      lib/nark/lib              <--- 'nark' library python files
      lib/blah/lib              <--- 'blah' library python files
      lib/blah/lib/blah/Blah.py <--- An actual python file.

      You can add alternative search locations by passing them into the
      extras array. These will also be searched for 'lib' folders the 
      same way.

      If you want to see things happen to try to figure out WTF is
      going on, turn __DEBUG to true.
  """

  __DEBUG = False
  """ Output debug messages? """
  
  __libPattern = ["lib$", "src$", "Lib$", "pyglet-.*$", "cocos2d-.*$"]
  """ Attach dir matching this to the python path """

  __zipPattern = ".*\.zip$"
  """ Attach zip files directly to the path """

  __targets = []
  """ List of targets found """

  __queue = deque()
  """ Queue of directories ot process """

  def __trace(self, msg):
    """ Print helpful debug messages """
    if (self.__DEBUG):
      print("[ bootstrap ] " + msg)

  def __seekRoot(self):
    """ Find the closest parent with a lib directory """
    found = False
    path = abspath(os.getcwd())
    self.__trace("Looking for library folders in '%s'" % path)
    while not found:
      for name in os.listdir(path):
        fullname = abspath(join(path, name))
        if isdir(fullname):
          for p in self.__libPattern:
            if not re.match(p, name) is None:
              found = True
              self.__targets.append(fullname)
              self.__queue.append(fullname)
              self.__trace("Found library folder at '%s'" % fullname)
              break
      if not found:
        new_path = abspath(join(path, pardir))
        self.__trace("No love. Seeking in parent '%s'" % new_path)
        if path == new_path:
          found = True # No where left to look
          self.__trace("No library path anywhere in the path.")
        else:
          path = new_path

  def __processPath(self, path):
    """ Seek matches in path and enque directories """
    if os.path.exists(path):
      self.__trace("Looking for child library folders in '%s'" % path)
      for name in os.listdir(path):
        fullname = abspath(join(path, name))
        if isdir(fullname):
          found = False
          for p in self.__libPattern:
            if not re.match(p, name) is None:
              self.__targets.append(fullname)
              self.__trace("Found a target at '%s'" % fullname)
              found = True
          if not found:
            self.__queue.append(fullname)

  def __addToPath(self):
    """ Add to python path """
    self.__trace("Finished looking for libraries")
    sys.path.extend(self.__targets)
    for path in self.__targets:
      self.__trace("Added target to path: %s" % path)
    for path in self.__targets:
      path = abspath(path)
      if os.path.exists(path):
        for name in os.listdir(path):
          fullname = abspath(join(path, name))
          if not isdir(fullname):
            if not re.match(self.__zipPattern, fullname) is None:
              sys.path.append(fullname)
              self.__trace("Added zip target to path: %s" % fullname)

  def load(self, extras):
    """ Load library dirs, including from extras """
    self.__queue.extend(extras)
    self.__targets.extend(extras)
    self.__seekRoot()
    while len(self.__queue) > 0:
      path = self.__queue.popleft()
      self.__processPath(path)
    self.__addToPath()

if not hasattr(Bootstrap, "__done"):
  bootstrap = Bootstrap()
  bootstrap.load(extras)
  Bootstrap.__done = True
