#!/usr/bin/env python

from datetime import timedelta
import src.bootstrap
import unittest
import nwidget
from nwidget.helpers import *
_ = src.bootstrap


class Tests(PygletTestBase):

  def setup(self):
    return nwidget.TextArea(), nwidget.Assets()
  
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
      i.register(self._window)
      i0 = i
      self.__widgets.append(i)
      
      # Single line label
      i, a = self.setup()
      i.bounds(10, 250, 390, 300)
      i.text = "Hello World"
      i.font = a.resolve("data", "roboto.ttf")
      i.color = (30, 30, 30, 255)
      i.multiline = False
      i.size = 12
      i.limit = 30
      i.register(self._window)
      i.on_change = "TEXT_CHANGE"
      i1 = i
      self.__widgets.append(i)

      def cb(code, widget):
        print("New text: %s" % widget.text)
      nwidget.listen("TEXT_CHANGE", cb)
      
      # Buttons to control focus
      b = nwidget.Button(text="Focus")
      b.bounds(50, 80, 150, 100)
      b.on_click = "B1"
      b.register(self._window)
      def cb(code, button):
        i0.focus()
        i1.focus(False)
      nwidget.listen("B1", cb)
      self.__widgets.append(b)
      
      b = nwidget.Button(text="Focus")
      b.bounds(10, 310, 110, 340)
      b.on_click = "B2"
      b.register(self._window)
      def cb2(code, button):
        i1.focus()
        i0.focus(False)
      nwidget.listen("B2", cb2)
      self.__widgets.append(b)
      
      # Display bounds for labels
      set = []
      for w in self.__widgets:
        if isinstance(w, nwidget.TextArea):
          b = nwidget.Block(solid=True)
          b.bounds(w.xmin, w.ymin, w.xmax, w.ymax)
          b.color = (150, 150, 150, 255)
          set.append(b)
      for b in set:
        self.__widgets.insert(0, b)  
        
    self.run_pyglet(runner, draw, update)
    
if __name__ == "__main__":
  unittest.main()
