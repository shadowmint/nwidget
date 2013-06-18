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
    return nwidget.ImageButton(), nwidget.Assets()
  
  def shutdown(self):
    self.stop_pyglet()
    nwidget.ImageButton.clear_assets()
  
  def test_can_run_flat_buttons(self):
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
      
      # Global setup
      self.__widgets = []
      self.enable_blending()
      
      # Common event callback
      def callback(code, button):
        button.disabled = True
        
      # Garish button to demo actions
      b1, a = self.setup()
      b1.texture = a.resolve("data", "image_button1.png")
      b1.texture_over = a.resolve("data", "image_button1.png")
      b1.texture_down = a.resolve("data", "image_button1.png")
      b1.texture_disabled = a.resolve("data", "image_button1.png")
      b1.uv = (0, 0.75, 1, 0.75, 1, 1, 0, 1)
      b1.uv_over = (0, 0.5, 1, 0.5, 1, 0.75, 0, 0.75)
      b1.uv_down = (0, 0.25, 1, 0.25, 1, 0.5, 0, 0.5)
      b1.uv_disabled = (0, 0, 1, 0, 1, 0.25, 0, 0.25)
      b1.bounds(10, 10, 138, 42)
      b1.on_click = "IBTN1"
      b1.register(self._window) # <--- Notice how you must attach the widget to the pyglet event system
      self.__widgets.append(b1)
      nwidget.listen("IBTN1", callback)
      
      # Square button test
      b2, a = self.setup()
      b2.from_square(a.resolve("data", "image_button2.png"))
      b2.on_click = "IBTN2"
      b2.bounds(100, 100, 164, 164)
      b2.register(self._window)
      self.__widgets.append(b2)
      nwidget.listen("IBTN2", callback)
      
      # Subtexture button tests
      b3, a = self.setup()
      b3.from_square(a.resolve("data", "image_button3.png"), (0.5, 0, 1, 0.5))
      b3.on_click = "IBTN3"
      b3.bounds(10, 300, 72, 364)
      b3.register(self._window)
      self.__widgets.append(b3)
      nwidget.listen("IBTN3", callback)
      
      b4, a = self.setup()
      b4.from_square(a.resolve("data", "image_button3.png"), (0.5, 0, 1, 0.5))
      b4.on_click = "IBTN4"
      b4.bounds(100, 300, 164, 364)
      b4.register(self._window)
      self.__widgets.append(b4)
      nwidget.listen("IBTN4", callback)
      b4.click()
      
      b5, a = self.setup()
      b5.from_row(a.resolve("data", "image_button3.png"), (0, 0.75, 1, 1))
      b5.on_click = "IBTN5"
      b5.bounds(200, 300, 264, 364)
      b5.register(self._window)
      self.__widgets.append(b5)
      nwidget.listen("IBTN5", callback)
      
      b6, a = self.setup()
      b6.from_column(a.resolve("data", "image_button3.png"), (0, 0, 0.25, 1))
      b6.on_click = "IBTN6"
      b6.bounds(300, 300, 364, 364)
      b6.register(self._window)
      self.__widgets.append(b6)
      nwidget.listen("IBTN6", callback)

    self.run_pyglet(runner, draw, update)
    
if __name__ == "__main__":
  unittest.main()
