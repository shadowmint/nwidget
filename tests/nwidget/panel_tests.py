#!/usr/bin/env python

from datetime import timedelta
import src.bootstrap
import unittest
import nwidget
from nwidget.helpers import *
_ = src.bootstrap


class Tests(PygletTestBase):

  def setup(self):
    return nwidget.Panel(), nwidget.Assets()
  
  def shutdown(self):
    self.stop_pyglet()
  
  def test_can_parse_image(self):
    nwidget.Panel.clear_assets()

    from nwidget.widgets import PanelMap
    _, r = self.setup()
    a = Assert()
    i = PanelMap(r.resolve("data", "panel3.png"))

    a.equals(i.left, 3, "Failed to count left bound")
    a.equals(i.right, 2, "Failed to count right bound")
    a.equals(i.top, 3, "Failed to count top bound")
    a.equals(i.bottom, 5, "Failed to count bottom bound")

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
      # Notice we must enable blending to get alpha edges
      nwidget.Panel.clear_assets()
      self.enable_blending() 

      i1, a = self.setup()
      i1.bounds(50, 50, 200, 200)
      i1.texture = a.resolve("data", "panel3.png")
      
      i2, a = self.setup()
      i2.bounds(50, 220, 350, 340)
      i2.texture = a.resolve("data", "panel1.png")

      i3, a = self.setup()
      i3.bounds(220, 30, 300, 260)
      i3.texture = a.resolve("data", "panel1.png")

      i4, a = self.setup()
      i4.bounds(0, 0, 400, 400)
      i4.texture = a.resolve("data", "panel2.png")

      self.__widgets = [ i3, i2, i1, i4 ]
    self.run_pyglet(runner, draw, update)
    
if __name__ == "__main__":
  unittest.main()
