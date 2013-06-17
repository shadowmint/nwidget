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

from __future__ import absolute_import
from datetime import datetime
import hashlib
import imp
import os

class Factory():
  """ This class helps load and look after python modules manually.

      To load a module from a .py file, use:

      x = Factory()
      x.load(path)

      To access a module property, use:

      x.prop()

      If watch() is invoked, when ever prop() is called, the file is 
      checked to see if has been updated since last load, and reloaded
      if so.
  """

  def __init__(self):
    self.__path = None
    self.__hash = None
    self.__watch = False

  def watch(self, watching):
    """ Enable watching """
    self.__watch = watching

  def load(self, path):
    """ Load the module 

        Notice exceptions are throw upwards, while missing/bad file
        is a return code of False. 
    """
    self.__path = path
    if self.__hash is None:
      m = hashlib.md5()
      m.update(self.__path)
      self.__hash = m.hexdigest()
    try:
      self.__timestamp = os.path.getmtime(self.__path)
      with open(self.__path, 'r') as content_file:
        content = content_file.read()
    except OSError:
      return False 
    except IOError:
      return False 
    self.__module = imp.new_module(self.__hash)
    exec content in self.__module.__dict__
    return True

  def __check(self):
    """ Check for updates to file since last update """
    if self.__watch:
      timestamp = os.path.getmtime(self.__path)
      if timestamp != self.__timestamp:
        self.load(self.__path)

  def prop(self, name):
    """ Return a property from the loaded module """
    self.__check()
    return self.__module.__dict__[name]
