#!/usr/bin/env python

from datetime import timedelta
try:
  import bootstrap
except:
  pass
import unittest
import nwidget
from nwidget.helpers import *


class Tests(PygletTestBase):

  def setup(self):
    return nwidget.Block()
  
  def shutdown(self):
    self.stop_pyglet()
  
  def test_can_create_instance(self):
    def update():
      if self._tested:
        if self._elpased > timedelta(seconds=2):
          self.shutdown()
    def draw():
      if self._tested:
        self._window.clear()
        for i in self.__blocks:
          i.draw()
    def runner():
      self.enable_blending()
      
      i1 = self.setup()
      i1.bounds(50, 50, 100, 100)
      i1.solid = True
      i1.color = (255, 0, 255, 255)
      
      i2 = self.setup()
      i2.bounds(50, 150, 100, 200)
      i2.solid = False
      i2.color = (255, 255, 0, 255)
      
      self.__blocks = [ i1, i2 ]
    self.run_pyglet(runner, draw, update)
    
if __name__ == "__main__":
  unittest.main()
