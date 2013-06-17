#!/usr/bin/env python

from __future__ import print_function
from datetime import timedelta
import src.bootstrap
import unittest
import nwidget
from nwidget.helpers import *

_ = src.bootstrap


class Tests(PygletTestBase):
  def shutdown(self):
    self.stop_pyglet()
    nwidget.ImageButton.clear_assets()

  def test_can_run_flat_buttons(self):
    def update():
      if self._tested:
        if self._elpased > timedelta(seconds=8):
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
      a = nwidget.Assets()

      # Text button select with both buttons
      b_next = nwidget.Button(text="next", on_click="S_NEXT_1")
      b_prev = nwidget.Button(text="prev", on_click="S_NEXT_2")
      items = nwidget.HList()
      marker = nwidget.Block(solid=False, color=(255, 0, 0, 255))

      b_prev.bounds(10, 10, 50, 50)
      items.bounds(50, 10, 200, 50)
      b_next.bounds(200, 10, 240, 50)

      selector = nwidget.Select(next=b_next, prev=b_prev, marker=marker, list=items)
      selector.on_change = "SELECTED"

      for i in range(10):
        b = nwidget.Block(solid=True, color=(0, 0, 25 * i, 255))
        selector.add(b, "ITEM_" + str(i), -1, 10 * i)
      selector.index = 3

      selector.register(self._window)
      b_prev.register(self._window)
      b_next.register(self._window)
      self.__widgets.append(selector)

      def scb1(_, widget):
        print("Currently selected item is: %s" % widget.selected)

      nwidget.listen("SELECTED", scb1)

      # Vertical list with image buttons, marker, and restricted display count
      b_next = nwidget.ImageButton(on_click="SELECT_2")
      b_next.from_row(a.resolve("data", "arrows.png"), (0, 0, 1, 0.25))
      marker = nwidget.Block(solid=False, color=(255, 255, 255, 255))
      items = nwidget.VList(padding=5)

      items.bounds(10, 100, 60, 340)
      b_next.bounds(10, 340, 60, 390)

      selector = nwidget.Select(next=b_next, list=items, marker=marker)

      for i in range(10):
        img = nwidget.Image(texture=a.resolve("data", "select1.png"))
        low = 0.1 * i
        high = 0.1 * (i + 1)
        img.uv = (low, low, low, high, high, high, high, low)
        selector.add(img, "ITEM_" + str(i))

      selector.index = 0
      selector.display_count = 5

      b_next.register(self._window)
      selector.register(self._window)
      self.__widgets.append(selector)

      # Image buttons, active item enabled only
      # The marker here is a semi-transparent image overlay
      b_next = nwidget.ImageButton(on_click="SELECT_3_NEXT")
      b_next.from_row(a.resolve("data", "arrows.png"), (0, 0.75, 1, 1))
      b_prev = nwidget.ImageButton(on_click="SELECT_3_PREV") # <-- different event code
      b_prev.from_row(a.resolve("data", "arrows.png"), (0, 0.25, 1, 0.5))
      marker = nwidget.Image(texture=a.resolve("data", "marker1.png"))
      items = nwidget.HList(padding=5)

      items.bounds(150, 200, 350, 250)
      b_prev.bounds(100, 200, 150, 250)
      b_next.bounds(350, 200, 400, 250)

      selector = nwidget.Select(next=b_next, list=items, marker=marker, prev=b_prev)
      selector.display_count = 5
      selector.index = 2
      selector.display_start = 0
      selector.on_change = "SELECT_3_UPDATE"

      for i in range(10):
        b = nwidget.ImageButton()
        b.texture = a.resolve("data", "select2.png")
        b.texture_over = a.resolve("data", "select2.png")
        b.texture_down = a.resolve("data", "select2.png")
        b.texture_disabled = a.resolve("data", "select2.png")
        xo = i * 0.1
        xe = xo + 0.1
        b.uv = (xo, 0.3, xe, 0.3, xe, 0.4, xo, 0.4)
        b.uv_over = (xo, 0.2, xe, 0.2, xe, 0.3, xo, 0.3)
        b.uv_down = (xo, 0.1, xe, 0.1, xe, 0.2, xo, 0.2)
        b.uv_disabled = (xo, 0, xe, 0, xe, 0.1, xo, 0.1)
        b.register(self._window)
        if i != selector.index:
          b.disabled = True
        selector.add(b, "BUTTON_" + str(i))

      def scb3(_, w):
        for i in range(10):
          wx = w.item(i)
          wx.disabled = not (i == w.index)
          pass
      nwidget.listen("SELECT_3_UPDATE", scb3)

      b_next.register(self._window)
      b_prev.register(self._window)
      selector.register(self._window)
      self.__widgets.append(selector)

    self.run_pyglet(runner, draw, update)


if __name__ == "__main__":
  unittest.main()
