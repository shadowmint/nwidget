# Copyright 2012 Douglas Linder
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
import pyglet
import unittest
from datetime import datetime

# Display debugging information during tests?
DEBUG = False

# The default length of a test to run for 'short' tests
DEFAULT_SHORT_TEST = 4

# The default length of a test to run for 'long' tests
DEFAULT_LONG_TEST = 10

# If we're debugging, make tests last forever thanks
if DEBUG:
  DEFAULT_LONG_TEST = 2048
  DEFAULT_SHORT_TEST = 2048

class Assert:
  """ Test helper """
  
  def true(self, value, message):
    if not value:
      self.__fail("%s (value was not True)" % (message))
  
  def false(self, value, message):
    if value:
      self.__fail("%s (value was True)" % (message))
      
  def equals(self, v1, v2, message):
    if not v1 == v2:
      self.__fail("%s (%s != %s)" % (message, str(v1), str(v2)))
      
  def null(self, value, message):
    if not value is None:
      self.__fail("%s (%s was not None)" % (message, str(value)))
      
  def notNull(self, value, message):
    if value is None:
      self.__fail("%s (value was None)" % (message, str(value)))
      
  def trace(self, message):
    if DEBUG:
      print(message)
      
  def __fail(self, message):
    try:
      assert False
    except Exception, e:
      print("%s: %s" % (message, str(e)))
    assert False


class PygletTestBase(unittest.TestCase):
  """ Common base for test base """

  def setUp(self):
    self._width = 400
    self._height = 400

  def run_pyglet(self, test, draw, loop):
    self._window = pyglet.window.Window(self._width, self._height)
    self.__loop = pyglet.app.EventLoop()
    self.__dead = False
    self.__test = test
    self._tested = False
    self.__started = datetime.now()
    self._elpased = datetime.now() - self.__started
    self.__app_loop = loop
    
    def event_loop(dt):
      self._elpased = datetime.now() - self.__started
      self.__app_loop()
      if self.__dead:
        self.__loop.exit()
      if not self._tested:
        self._tested = True
        self.__test()
        
    pyglet.clock.schedule_interval(event_loop, 0.001)
        
    self._window.push_handlers(on_draw=draw)
    self.__loop.run()
  
  def stop_pyglet(self):
    self.__dead = True      
    
  def enable_blending(self):
    """ Enable basic alpha blending to allow transparency """
    pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
    pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)
