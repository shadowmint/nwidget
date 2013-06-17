#!/usr/bin/env python

from datetime import timedelta
import src.bootstrap
import unittest
import nwidget
from nwidget.helpers import *
_ = src.bootstrap

class Tests(PygletTestBase):

  def setup(self):
    return nwidget.Label(), nwidget.Assets()
  
  def shutdown(self):
    self.stop_pyglet()
  
  def test_can_create_instance(self):
    def update():
      if self._tested:
        if self._elpased > timedelta(seconds=DEFAULT_SHORT_TEST):
          self.shutdown()
        else:
          self.__widgets[0].text = "bsdfmnmmmmbsdfsdf" + str(self._elpased)
    def draw():
      if self._tested:
        self._window.clear()
        for i in self.__widgets:
          i.draw()
    def runner():
      
      # Label that changes over time
      i1, a = self.setup()
      i1.bounds(50, 50, 270, 100)
      i1.text = "Hello World"
      i1.font = a.resolve("data", "lekton.ttf")
      i1.color = (255, 0, 0, 255)
      i1.size = 12
      
      # Multiline label with edge wrapping
      i2, a = self.setup()
      i2.bounds(50, 110, 250, 210)
      i2.text = "Hello World Thd sf s dfas df sdf dsf adf dsf dsf dsaf dsa fdsaf adsf adsf asdf asdf"
      i2.font = a.resolve("data", "roboto.ttf")
      i2.color = (255, 255, 0, 255)
      i2.size = 10
      
      # Label centered
      i3, a = self.setup()
      i3.bounds(50, 220, 350, 260)
      i3.text = "This text is bottom-centered"
      i3.font = a.resolve("data", "roboto.ttf")
      i3.color = (255, 255, 255, 255)
      i3.align = nwidget.align.CENTER
      i3.valign = nwidget.align.BOTTOM
      
      # Label right align
      i4, a = self.setup()
      i4.bounds(50, 260, 350, 300)
      i4.text = "This text is top-right aligned"
      i4.color = (255, 255, 255, 255)
      i4.align = nwidget.align.RIGHT
      i4.valign = nwidget.align.TOP
      
      # Label with font-size
      i5, a = self.setup()
      i5.bounds(50, 300, 350, 340)
      i5.text = "This text is 20pt high"
      i5.color = (255, 255, 255, 255)
      i5.font = a.resolve("data", "orotund.ttf")
      i5.size = 20
      
      self.__widgets = [ i1, i2, i3, i4, i5 ]
      
      # Display bounds for labels
      set = []
      for w in self.__widgets:
        b = nwidget.Block()
        b.bounds(w.xmin, w.ymin, w.xmax, w.ymax)
        b.color = (0, 0, 255, 255)
        set.append(b)
      for b in set:
        self.__widgets.append(b)  
        
    self.run_pyglet(runner, draw, update)
    
if __name__ == "__main__":
  unittest.main()
