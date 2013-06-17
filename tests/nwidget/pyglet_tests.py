#!/usr/bin/env python

from datetime import timedelta
import src.bootstrap
import unittest
import time
import nwidget
from nwidget.helpers import *
_ = src.bootstrap

class TestType():
  def __init__(self):
    pass
  
class Tests(PygletTestBase):

  def setup(self):
    return Assert(), TestType()
  
  def shutdown(self):
    self.stop_pyglet()
  
  def test_can_create_instance(self):
    def update():
      if self._tested:
        if self._elpased > timedelta(seconds=2):
          self.shutdown()
    def draw():
      if self._tested:
        self._window.clear()
    def runner():
      a, i = self.setup()
      a.notNull(i, "Failed to create test instance")
    self.run_pyglet(runner, draw, update)

if __name__ == "__main__":
  unittest.main()
