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
    return nwidget.Stack()
  
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
      self.enable_blending()

      a = nwidget.Assets()
      s1 = nwidget.Image(texture=a.resolve("data", "cat2.jpg"))
      s2 = nwidget.Image(texture=a.resolve("data", "panel2.png"))

      i = self.setup()
      i.add(s1)
      i.add(s2)
      i.bounds(50, 50, 200, 200)

      self.__widgets = [i]
    self.run_pyglet(runner, draw, update)
    
if __name__ == "__main__":
  unittest.main()
