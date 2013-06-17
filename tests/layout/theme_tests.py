#!/usr/bin/env python

from datetime import timedelta
import src.bootstrap
import unittest
import time
import nwidget
from nwidget.helpers import *
_ = src.bootstrap


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
      self.layout = nwidget.Layout(self._window, theme, None, assets.resolve("ui/sample1.py"))

      # Model
      self.model = {"main_button_enabled": True, "updated": True, "main_text": "Try clicking me"}

      # events
      def click_event(code, widget):
        self.model = {"main_button_enabled": False, "main_text": "DISABLED", "updated": True}
      nwidget.listen("MAIN_BUTTON_CLICK", click_event)

      def swap_debug(code, widget):
        self.debug = not self.debug
        self.layout.show_edges(self.debug)
        self.layout.show_bounds(self.debug)
      self.show_debug = True
      nwidget.listen("DEBUG_CLICK", swap_debug)

      # Turn on debugging
      self.layout.watch()
      self.layout.show_edges(True)
      self.layout.show_bounds(True)

    self.run_pyglet(runner, draw, update)

if __name__ == "__main__":
  unittest.main()
