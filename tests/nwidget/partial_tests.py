#!/usr/bin/env python

from datetime import timedelta
import src.bootstrap
import unittest
import nwidget
from nwidget.helpers import *
_ = src.bootstrap


class Tests(PygletTestBase):

  def setup(self):
    return nwidget.Partial(), nwidget.Assets()
  
  def shutdown(self):
    self.stop_pyglet()
  
  def test_can_create_instance(self):
    def update():
      value = (self._elpased.microseconds % 1000000) / 1000000.0
      for a in self.actives:
        a.value = value
      if self._tested:
        if self._elpased > timedelta(seconds=10):
          self.shutdown()

    def draw():
      if self._tested:
        self._window.clear()
        for i in self.__widgets:
          i.draw()

    def runner():

      self.enable_blending()
      self.__widgets = []

      # Basic from left partial
      i, a = self.setup()
      i.bounds(50, 50, 200, 100)
      i.texture = a.resolve("data", "partial1.png")
      i.uv = (0, 0, 1, 0, 1, 0.5, 1, 0.5)
      i.texture_under = a.resolve("data", "partial1.png")
      i.uv_under = (0, 0.5, 1, 0.5, 1, 1, 1, 1)
      i.anchor = nwidget.align.LEFT
      i.value = 0.5
      self.__widgets.append(i)
      self.actives.append(i)

      # Panel based from right partial
      i, a = self.setup()
      i.bounds(50, 120, 200, 200)
      i.texture = a.resolve("data", "partial2.png")
      i.texture_under = a.resolve("data", "partial2_under.png")
      i.anchor = nwidget.align.RIGHT
      i.value = 0
      i.panel = True
      self.__widgets.append(i)
      self.actives.append(i)

      # Panel based from top partial
      i, a = self.setup()
      i.bounds(50, 210, 100, 390)
      i.texture = a.resolve("data", "partial2.png")
      i.texture_under = a.resolve("data", "partial2_under.png")
      i.anchor = nwidget.align.TOP
      i.value = 0
      i.panel = True
      self.__widgets.append(i)
      self.actives.append(i)

      # Panel based from bottom partial
      i, a = self.setup()
      i.bounds(110, 210, 160, 390)
      i.texture = a.resolve("data", "partial2.png")
      i.texture_under = a.resolve("data", "partial2_under.png")
      i.anchor = nwidget.align.BOTTOM
      i.value = 0
      i.panel = True
      self.__widgets.append(i)
      self.actives.append(i)

      # Image based from top partial
      i, a = self.setup()
      i.bounds(200, 210, 250, 390)
      i.texture = a.resolve("data", "partial1.png")
      i.anchor = nwidget.align.TOP
      i.value = 0
      self.__widgets.append(i)
      self.actives.append(i)

      # Image based from bottom partial
      i, a = self.setup()
      i.bounds(260, 210, 310, 390)
      i.texture = a.resolve("data", "partial1.png")
      i.anchor = nwidget.align.BOTTOM
      i.value = 0
      self.__widgets.append(i)
      self.actives.append(i)

      # Meaningful image from bottom
      i, a = self.setup()
      i.bounds(250, 10, 400, 170)
      i.texture = a.resolve("data", "partial3.jpg")
      i.texture_under = a.resolve("data", "partial3_under.jpg")
      i.anchor = nwidget.align.RIGHT
      i.value = 0.5
      self.__widgets.append(i)
      self.actives.append(i)

    self.actives = []
    self.run_pyglet(runner, draw, update)
    
if __name__ == "__main__":
  unittest.main()
