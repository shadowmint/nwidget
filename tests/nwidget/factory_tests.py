#!/usr/bin/env python
import src.bootstrap
import unittest
import nwidget
import time
from nwidget.factory import Factory
from nwidget.helpers import *
_ = src.bootstrap

class Tests(unittest.TestCase):

  def setup(self):
    instance = Factory()
    return Assert(), nwidget.Assets(), instance
  
  def test_can_create_instance(self):
    t, _, i = self.setup()
    t.notNull(i, "Failed to create Config instance")
    
  def test_cannot_load_missing_file(self):
    t, a, i = self.setup()
    path = a.resolve("data", "sample1.py")
    path += ".dfsdfdsfsd"
    loaded = i.load(path)
    t.false(loaded, "Invalid return value")

  def test_can_load_file(self):
    t, a, i = self.setup()
    path = a.resolve("data", "sample1.py")

    fp = open(path, "w")
    fp.write("text = \"Hello World\"")
    fp.close()

    loaded = i.load(path)
    value = i.prop("text")

    t.true(loaded, "Invalid return value")
    t.equals(value, "Hello World", "Failed to read module value")

  def test_does_not_update_file_if_not_watching(self):
    t, a, i = self.setup()
    path = a.resolve("data", "sample1.py")

    fp = open(path, "w")
    fp.write("text = \"Hello World\"")
    fp.close()

    time.sleep(1)

    i.load(path)
    value = i.prop("text")

    t.equals(value, "Hello World", "Failed to read module value")

    time.sleep(1)

    fp = open(path, "w")
    fp.write("text = \"Hello WORLD\"")
    fp.close()

    value = i.prop("text")
    
    t.equals(value, "Hello World", "Failed to read module value")

  def test_can_update_file(self):
    t, a, i = self.setup()
    path = a.resolve("data", "sample1.py")

    fp = open(path, "w")
    fp.write("text = \"Hello World\"")
    fp.close()

    i.load(path)
    i.watch(True)  # Notice watching now
    value = i.prop("text")

    t.equals(value, "Hello World", "Failed to read module value")

    time.sleep(1)

    fp = open(path, "w")
    fp.write("text = \"Hello WORLD\"")
    fp.close()

    value = i.prop("text")
    
    t.equals(value, "Hello WORLD", "Failed to read module value")

if __name__ == "__main__":
  unittest.main()
