#!/usr/bin/env python

from datetime import timedelta
import src.bootstrap
import unittest
import nwidget
from nwidget.helpers import *
_ = src.bootstrap


class Tests(PygletTestBase):

  def setup(self):
    return nwidget.VList()
  
  def shutdown(self):
    self.stop_pyglet()
  
  def test_can_create_instance(self):
    self.__widgets = []

    def update():
      if self._tested:
        if self._elpased > timedelta(seconds=5):
          self.shutdown()

    def draw():
      if self._tested:
        self._window.clear()
        for i in self.__widgets:
          i.draw()

    def runner():

      a = nwidget.Assets()

      i = self.setup()
      i.bounds(10, 10, 60, 380)
      for _ in range(10):
        img = nwidget.Image(texture=a.resolve("data", "cat2.jpg"))
        i.add(img)
      self.__widgets.append(i)

      i = self.setup()
      i.bounds(100, 0, 200, 400)
      i.padding = 10
      for _ in range(10):
        img = nwidget.Image(texture=a.resolve("data", "cat2.jpg"))
        i.add(img)
      self.__widgets.append(i)

      # A few fixed size elements 
      i = self.setup()
      i.bounds(300, 50, 350, 400)
      i.padding = 5
      for x in range(10):
        img = nwidget.Image(texture=a.resolve("data", "cat2.jpg"))
        if x == 5:
          i.add(img, 100)
        elif x == 8:
          i.add(img, 30, 100)
        else:
          i.add(img)
      self.__widgets.append(i)

    self.run_pyglet(runner, draw, update)

if __name__ == "__main__":
  unittest.main()
