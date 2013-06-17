#!/usr/bin/env python

from datetime import timedelta
import src.bootstrap
import unittest
import nwidget
from nwidget.helpers import *
_ = src.bootstrap

class Tests(PygletTestBase):

  def setup(self):
    return nwidget.Image(), nwidget.Assets()
  
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
        for i in self.__widgets:
          i.draw()
    def runner():
      i1, a = self.setup()
      i1.bounds(50, 50, 100, 100)
      i1.texture = a.resolve("data", "cat.jpg")
      
      i2, a = self.setup()
      i2.bounds(150, 150, 300, 400)
      i2.uv = (0, 0, 0, 0.5,  0.5, 0.5, 0.5, 0)
      i2.texture = a.resolve("data", "cat.jpg")
      
      self.__widgets = [ i1, i2 ]
    self.run_pyglet(runner, draw, update)
    
if __name__ == "__main__":
  unittest.main()
