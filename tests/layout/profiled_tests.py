#!/usr/bin/env python

from datetime import timedelta
import src.bootstrap
import unittest
import time
import nwidget
import cProfile
import io
import pstats
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
        if self._elpased > timedelta(seconds=10):
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
      self.layout = nwidget.Layout(self._window, theme, assets, assets.resolve("ui/sample1.py"))

      # Model
      self.model = {"main_button_enabled": True, "updated": True, "main_text": "Try clicking me"}

      # events
      def click_event(code, widget):
        print("EVENT!")
        self.model = {"main_button_enabled": False, "main_text": "DISABLED", "updated": True}
      nwidget.listen("MAIN_BUTTON_CLICK", click_event)

      # Turn on debugging
      self.layout.watch()
      self.layout.show_edges(True)
      self.layout.show_bounds(True)

    # Run profiler manually
    p = cProfile.Profile()
    print("Starting profiler")
    p.enable()

    # Run test
    self.run_pyglet(runner, draw, update)

    # Print results
    p.disable()
    print("Stopped profiler")

    p.dump_stats("profile_output.txt")
    print("Profile output saved to: \"profile_output.txt\"")

    fp = open("profile.txt", "w")
    ps = pstats.Stats("profile_output.txt", stream=fp)
    ps.sort_stats("time")
    ps.print_stats()
    fp.close()

if __name__ == "__main__":
  unittest.main()
