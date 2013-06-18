#!/usr/bin/env python

from datetime import timedelta
try:
  import bootstrap
except:
  pass
import unittest
import time
import nwidget
from nwidget.helpers import *



class Tests(PygletTestBase):

  def setup(self):
    self.enable_blending()

  def shutdown(self):
    self.stop_pyglet()
  
  def test_can_create_instance(self):
    self._width = 600

    def update():
      if self._tested:
        if self._elpased > timedelta(seconds=5):
          self.shutdown()

    def draw():
      if self._tested:
        self._window.clear()
        self.layout.model = self.model
        self.layout.draw()

    def runner():

      # Load layout
      self.setup()
      assets = nwidget.Assets()
      theme_path = assets.resolve("..", "..", "assets", "theme", "light")
      theme = nwidget.theme.Light(theme_path, self._window)
      sassets = nwidget.Assets(assets.resolve("ui"))
      self.layout = nwidget.Layout(self._window, theme, sassets, assets.resolve("ui/sample2.py"))

      # Model
      self.model = {"main_button_enabled": True, "updated": True, "main_text": "Try clicking me", "turn_off": False}

      # events from child layout
      def click_event(code, widget):
        self.model["main_button_enabled"] = False
        self.model["main_text"] = "DISABLED"
        self.model["updated"] = True
      nwidget.listen("MAIN_BUTTON_CLICK", click_event)

      # events from parent layout
      def parent_event(code, widget):
        self.model["turn_off"] = True
        self.model["updated"] = True
      nwidget.listen("TURN_OFF_CHILD_DEBUG", parent_event)

      def parent_event2(code, widget):
        self.layout.show_edges(False)
        self.layout.show_bounds(False)
      nwidget.listen("TURN_OFF_OWN_DEBUG", parent_event2)

      # Turn on debugging by default
      self.layout.watch()
      self.layout.show_edges(True)
      self.layout.show_bounds(True)

    self.run_pyglet(runner, draw, update)

if __name__ == "__main__":
  unittest.main()
