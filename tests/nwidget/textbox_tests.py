#!/usr/bin/env python

from datetime import timedelta
import src.bootstrap
import unittest
import nwidget
from nwidget.helpers import *
_ = src.bootstrap


class Tests(PygletTestBase):

  def setup(self):
    return nwidget.Textbox(), nwidget.Assets()
  
  def shutdown(self):
    self.stop_pyglet()
  
  def test_can_create_instance(self):
    def update():
      if self._tested:
        if self._elpased > timedelta(seconds=8):
          self.shutdown()

    def draw():
      if self._tested:
        self._window.clear()
        for i in self.__widgets:
          i.draw()

    def runner():
      self.__widgets = []
      self.enable_blending()

      # Multiline label with edge wrapping
      i, a = self.setup()
      i.bounds(50, 110, 250, 210)
      i.text = "Hello World Thd sf s dfas df sdf dsf adf dsf dsf dsaf dsa fdsaf adsf adsf asdf asdf"
      i.font = a.resolve("data", "roboto.ttf")
      i.color = (255, 255, 0, 255)
      i.size = 10
      i.panel = a.resolve("data", "textbox_panel1.png")
      i.panel_focus = a.resolve("data", "textbox_panel2.png")
      i.register(self._window)
      i0 = i
      self.__widgets.append(i)
      
      # Single line label
      i, a = self.setup()
      i.bounds(10, 250, 390, 330)
      i.text = "Hello World"
      i.font = a.resolve("data", "roboto.ttf")
      i.color = (30, 30, 30, 255)
      i.multiline = False
      i.size = 12
      i.limit = 30
      i.register(self._window)
      i.panel = a.resolve("data", "textbox_panel1.png")
      i.panel_focus = a.resolve("data", "textbox_panel2.png")
      i.on_change = "TEXT_CHANGE"
      i.padding = 20
      i1 = i
      self.__widgets.append(i)

      def cb(code, widget):
        print("New text: %s" % widget.text)
      nwidget.listen("TEXT_CHANGE", cb)
        
    self.run_pyglet(runner, draw, update)
    
if __name__ == "__main__":
  unittest.main()
