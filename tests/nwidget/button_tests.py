#!/usr/bin/env python

from datetime import timedelta
import src.bootstrap
import unittest
import nwidget
from nwidget.helpers import *
_ = src.bootstrap

class Tests(PygletTestBase):

  def setup(self):
    return nwidget.Button(), nwidget.Assets()
  
  def shutdown(self):
    self.stop_pyglet()
    nwidget.Button.clear_assets()
  
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
    
      # Garish button to demo actions
      b1, a = self.setup()
      b1.frame = (255, 0, 0, 255)             
      b1.frame_over = (0, 255, 0, 255)        
      b1.frame_down = (0, 0, 255, 255)        
      b1.frame_disabled = (10, 10, 10, 255) 
      b1.font_color = (100, 0, 0, 255)
      b1.font_over = (0, 100, 0, 255)
      b1.font_down = (0, 0, 100, 255)
      b1.font_disabled = (90, 90, 90, 255)
      b1.text = "Hello World Button"                             
      b1.font = a.resolve("data", "roboto.ttf")
      b1.font_size = 12                        
      b1.on_click = "GARISH_BUTTON"                         
      b1.bounds(10, 10, 390, 50)
      b1.magic = 0
      b1.register(self._window)  # <--- Notice how you must attach the widget to the pyglet event system
      self.__widgets.append(b1)

      # Callback test on b1
      def callback(code, button):
        button.magic += 1
        button.text = "Clicked %d times" % button.magic
      nwidget.listen("GARISH_BUTTON", callback)

      # Trigger a few fake clicks
      nwidget.events.trigger("GARISH_BUTTON", b1)
      nwidget.events.trigger("GARISH_BUTTON", b1)
      nwidget.events.trigger("GARISH_BUTTON", b1)
      nwidget.events.trigger("GARISH_BUTTON", b1)
      
      # Garish button to demo disabled
      b2, a = self.setup()
      b2.frame = (255, 0, 0, 255)             
      b2.frame_over = (0, 255, 0, 255)        
      b2.frame_down = (0, 0, 255, 255)        
      b2.frame_disabled = (100, 100, 100, 255) 
      b2.font_color = (100, 0, 0, 255)
      b2.font_over = (0, 100, 0, 255)
      b2.font_down = (0, 0, 100, 255)
      b2.font_disabled = (0, 0, 0, 255)
      b2.text = "Disabled button"
      b2.font = a.resolve("data", "roboto.ttf")
      b2.font_size = 10                        
      b2.on_click = "GARISH_BUTTON_2"                         
      b2.bounds(50, 50, 200, 80)
      b2.disabled = True
      b2.register(self._window)
      self.__widgets.insert(0, b2)

      # Normalish button
      b3, a = self.setup()
      b3.frame = (205, 205, 205, 255)             
      b3.frame_over = (205, 205, 215, 255)        
      b3.frame_down = (90, 90, 90, 255)        
      b3.font_color = (100, 100, 100, 255)
      b3.font_over = (100, 100, 100, 255)
      b3.font_down = (150, 150, 150, 255)
      b3.text = "Extra wide button content here"
      b3.font = a.resolve("data", "roboto.ttf")
      b3.font_size = 12                        
      b3.on_click = "BUTTON_3"                         
      b3.bounds(10, 100, 300, 140)
      b3.register(self._window)
      self.__widgets.append(b3)

      for i in range(5):
        b4, a = self.setup()
        b4.texture = a.resolve("data", "button.png")
        b4.texture_over = a.resolve("data", "button_over.png")
        b4.texture_down = a.resolve("data", "button_down.png")
        b4.texture_disabled = a.resolve("data", "button_disabled.png")
        b4.font_color = (100, 0, 0, 255)
        b4.font_over = (0, 100, 0, 255)
        b4.font_down = (0, 0, 100, 255)
        b4.font_disabled = (90, 90, 90, 255)
        b4.text = "Hello World Button " + str(i)                             
        b4.font = a.resolve("data", "roboto.ttf")
        b4.font_size = 12                        
        b4.on_click = "B4"
        b4.bounds(10, 200 + i * 40, 390, 200 + i * 40 + 30)
        b4.register(self._window)
        self.__widgets.append(b4)

    self.run_pyglet(runner, draw, update)
    
if __name__ == "__main__":
  unittest.main()
