#!/usr/bin/env python
try:
  import bootstrap
except:
  pass
import unittest
import nwidget
from nwidget.helpers import *



class FakeWindow():
  def get_size(self):
    return 100, 100
  def set_handler(self, key, callback):
    pass


class Tests(PygletTestBase):

  def setup(self):
    return Assert(), nwidget.Layout
  
  def test_can_create_instance(self):
    t, i = self.setup()
    t.notNull(i, "Failed to create Layout instance")
    
  def test_can_load_layout(self):
    t, i = self.setup()

    # Fake window
    self._window = FakeWindow()

    # Load a theme to pass to the layout
    assets = nwidget.Assets()
    theme = nwidget.theme.Light(assets.resolve("..", "..", "assets", "theme", "light"), self._window)
    i(self._window, theme, None, assets.resolve("ui", "sample1.py"))

if __name__ == "__main__":
  unittest.main()
