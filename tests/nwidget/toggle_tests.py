#!/usr/bin/env python

from datetime import timedelta
import src.bootstrap
import unittest
import nwidget
from nwidget.helpers import *
_ = src.bootstrap


class Tests(PygletTestBase):

  def setup(self):
    return nwidget.Toggle(), nwidget.Assets()
  
  def shutdown(self):
    self.stop_pyglet()
  
  def test_can_create_instance(self):
    self.enable_blending()
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
      i, a = self.setup()
      i.bounds(50, 50, 100, 100)
      i.add(nwidget.Image(texture=a.resolve("data", "cat.jpg")), "CAT")
      i.add(nwidget.Image(texture=a.resolve("data", "cat2.jpg")), "CAT2")
      i.add(nwidget.Image(texture=a.resolve("data", "panel1.png")), "CAT3")
      i.register(self._window)
      i.on_change = "CHANGED"
      self.__widgets.append(i)

      i, a = self.setup()
      i.bounds(200, 200, 300, 300)
      i.add(nwidget.Image(texture=a.resolve("data", "cat.jpg")), "CAT")
      i.add(nwidget.Image(texture=a.resolve("data", "cat2.jpg")), "CAT2")
      i.add(nwidget.Image(texture=a.resolve("data", "panel1.png")), "CAT3")
      i.disabled_widget = nwidget.Image(texture=a.resolve("data", "button_disabled.png"))
      i.register(self._window)
      item = i
      self.__widgets.append(i)

      # Events
      def cb(_, widget):
        print("New state is: %s -> %s" % (widget.index, widget.state))
        if widget.state == "CAT3":
          item.disabled = True
          print("Disabled")
        elif item.disabled:
          item.disabled = False
      nwidget.listen("CHANGED", cb)

      i, a = self.setup()
      i.bounds(10, 200, 100, 290)
      i.add(nwidget.Image(texture=a.resolve("data", "cat.jpg")), "CAT")
      i.add(nwidget.Image(texture=a.resolve("data", "cat2.jpg")), "CAT2")
      i.add(nwidget.Image(texture=a.resolve("data", "panel1.png")), "CAT3")
      i.register(self._window)
      i.index = 2
      self.__widgets.append(i)

    self.run_pyglet(runner, draw, update)
    
if __name__ == "__main__":
  unittest.main()
