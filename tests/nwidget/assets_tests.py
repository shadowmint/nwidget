#!/usr/bin/env python

import src.bootstrap
import unittest
import os.path
from nwidget.assets import Assets
from nwidget.helpers import *
_ = src.bootstrap


class Tests(unittest.TestCase):

  def setup(self, base=""):
    if base == "":
      instance = Assets()
    else:
      instance = Assets(base)
    return Assert(), instance
  
  def test_can_create_instance(self):
    a, i = self.setup()
    a.notNull(i, "Failed to create Assets instance")
    
  def test_can_resolve_file_that_exists(self):
    a, i = self.setup()
    path = i.resolve("data", "arrows.png")
    a.notNull(path, "Failed to resolve path")

  def test_cant_resolve_file_that_does_not_exist(self):
    a, i = self.setup()
    failed = False
    try:
      _ = i.resolve("data", "blaf", "config.data")
    except:
      failed = True
    a.true(failed, "Verified stupid path")

  def test_can_use_custom_base_path(self):
    a, i = self.setup(os.path.join(os.getcwd(), os.path.pardir))
    path = i.resolve("nwidget", "data", "arrows.png")
    a.notNull(path, "Failed to resolve path")

if __name__ == "__main__":
  unittest.main()
