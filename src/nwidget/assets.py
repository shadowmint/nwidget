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
import os.path

class Assets():
  """ Helper for resolving paths in a convenient manner """
  
  __base = ""
  """ The path which is the universal root for this assets object """
  
  def __init__(self, base=""):
    """ Base is the path path for the loader; for getcwd() if not provided """
    if base == "":
      base = os.getcwd()
    self.__base = base
    
  def resolve(self, *args):
    """ Appropriately resolves a path in the form blah, blah, blah. 
        
        Base is attached as the root to this set of path elements.
        
        Throws an error at this level if the requested file doesn't
        exist.
    """
    rtn = os.path.join(self.__base, *args)
    if not self.__exists(rtn):
      raise Exception("Bad path: %s (base: %s)" % (rtn, self.__base))
    return rtn
    
  def __exists(self, path):
    rtn = os.path.isdir(path) or (os.path.isfile(path) and os.access(path, os.R_OK))
    return rtn
