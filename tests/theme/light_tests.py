#!/usr/bin/env python

import src.bootstrap
import unittest
import time
import nwidget
from datetime import timedelta
from nwidget.helpers import *
_ = src.bootstrap


class Tests(PygletTestBase):

  def setup(self):
    self.enable_blending()
    assets = nwidget.Assets()
    path = assets.resolve("..", "..", "assets", "theme", "light")
    return Assert(), nwidget.theme.Light(path, self._window)
  
  def shutdown(self):
    self.stop_pyglet()
  
  def test_can_create_instance(self):
    self._width = 800

    def update():
      if self._tested:
        if self._elpased > timedelta(seconds=DEFAULT_SHORT_TEST):
          self.shutdown()

    def draw():
      if self._tested:
        self._window.clear()
        for i in self.__widgets:
          i.draw()

    def runner():
      a, i = self.setup()
      a.notNull(i, "Failed to create test instance")
      
      self.__widgets = []

      panel = i.panel()
      panel.bounds(10, 10, 150, 390)
      self.__widgets.append(panel)

      panel = i.panel()
      panel.bounds(160, 10, 390, 390)
      self.__widgets.append(panel)

      panel = i.panel()
      panel.bounds(410, 10, 790, 390)
      self.__widgets.append(panel)

      button = i.button()
      button.bounds(20, 315, 140, 345)
      button.text = "Button Two"
      button.disabled = True
      ref = button
      self.__widgets.append(button)  # <--- Notice the theme transparently invokes register() internally
      
      button = i.button()
      button.bounds(20, 350, 140, 380)
      button.text = "Enable"
      button.on_click = "BUTTON_SWAP_STATE"
      self.__widgets.append(button)

      boxes = nwidget.VList(padding=10)
      boxes.bounds(40, 190, 160, 300)
      boxes.add(i.checkbox(), 10, 10)
      boxes.add(i.checkbox(), 20, 20)
      boxes.add(i.checkbox(), 20, 20)
      boxes.add(i.checkbox(), 30, 30)
      boxes.item(0).disabled = True
      self.__widgets.append(boxes)

      def callback(code, button):
        if button.text == "Enable":
          ref.disabled = False
          boxes.item(0).disabled = False
          button.text = "Disable"
        else:
          ref.disabled = True
          boxes.item(0).disabled = True
          button.text = "Enable"
      nwidget.listen("BUTTON_SWAP_STATE", callback)

      bars = nwidget.VList(padding=5)
      bars.bounds(20, 80, 140, 180)
      bars.add(i.progress())
      bars.add(i.progress())
      bars.add(i.progress())
      bars.add(i.progress())
      bars.add(i.progress())
      bars.item(0).value = 0
      bars.item(1).value = 0.25
      bars.item(2).value = 0.5
      bars.item(3).value = 0.75
      bars.item(4).value = 1
      self.__widgets.append(bars)

      display_box = i.subpanel()
      display_box.bounds(170, 100, 380, 250)
      self.__widgets.append(display_box)

      display = i.text()
      display.bounds(183, 100, 370, 235)
      display.text = ": Text goes here!\n: Press enter to see more!"
      display.color = (0, 0, 0, 255)
      display.keep = 8
      self.__widgets.append(display)

      arrows = nwidget.HList(padding=4)
      arrows.bounds(25, 40, 140, 65)
      self.__widgets.append(arrows)

      a1 = i.arrow_left()
      a1.on_click = "ARROW_CLICK"
      arrows.add(a1, width=25)

      a2 = i.arrow_right()
      a2.on_click = "ARROW_CLICK"
      arrows.add(a2, width=25)

      a3 = i.arrow_up()
      a3.on_click = "ARROW_CLICK"
      arrows.add(a3, width=25)

      a4 = i.arrow_down()
      a4.on_click = "ARROW_CLICK"
      arrows.add(a4, width=25)

      def disable_it(code, widget):
        widget.disabled = True
      nwidget.listen("ARROW_CLICK", disable_it)

      hint = i.hint()
      hint.bounds(180, 75, 370, 90)
      hint.text = "Type below and press enter to update text list"
      self.__widgets.append(hint)

      textbox = i.textbox()
      textbox.bounds(180, 30, 370, 70)
      textbox.text = "Type stuff here..."
      textbox.on_focus = "TB1_FOCUS"
      textbox.on_enter = "TB1_SUBMIT"
      textbox.limit = 20
      textbox.multiline = False
      self.__widgets.append(textbox)

      def clear_tb(_, widget):
        widget.text = ""

      def submit_tb(_, widget):
        display.append(": " + widget.text)
        widget.text = ""

      nwidget.listen("TB1_FOCUS", clear_tb)
      nwidget.listen("TB1_SUBMIT", submit_tb)

      header = i.header()
      header.text = "Light Theme Test"
      header.bounds(180, 330, 370, 390)
      self.__widgets.append(header)

      subheader = i.subheader()
      subheader.text = "subheading here"
      subheader.bounds(180, 300, 370, 370)
      self.__widgets.append(subheader)

      info = i.text()
      info.bounds(180, 250, 370, 320)
      info.text = "Bacon ipsum dolor sit amet turkey shoulder biltong leberkas corned beef turducken hamburger sirloin. Short loin"
      self.__widgets.append(info)

      header = i.header()
      header.text = "Options test"
      header.bounds(430, 330, 790, 390)
      self.__widgets.append(header)

      block = nwidget.VList(padding=10)
      block.bounds(430, 130, 760, 435)
      self.__widgets.append(block)

      label = i.label()
      label.text = "Value 43:"

      bar = i.progress()
      bar.value = 0.34

      item = nwidget.HList(padding=25)
      item.add(label, 150)
      item.add(bar, height=15)

      block.add(item, height=25)

      label = i.label()
      label.text = "Awesomenesss:"

      bar = i.progress()
      bar.value = 1.0

      item = nwidget.HList(padding=25)
      item.add(label, 150)
      item.add(bar, height=20)

      block.add(item, -1, 25)

      label = i.label()
      label.text = "Anonymous statistics:"

      box = i.checkbox()
      box.change()

      item = nwidget.HList(padding=25)
      item.add(label, 150)
      item.add(box, 20, 20)

      block.add(item, -1, 25)

      label = i.label()
      label.text = "Debug mode:"

      box = i.checkbox()

      item = nwidget.HList(padding=25)
      item.add(label, 150)
      item.add(box, 20, 20)

      block.add(item, -1, 25)

      label = i.label()
      label.text = "More ninjas:"

      box = i.checkbox()

      item = nwidget.HList(padding=25)
      item.add(label, 150)
      item.add(box, 20, 20)

      block.add(item, -1, 25)

      label = i.label()
      label.text = "Select resolution:"

      options = i.options({"LOW": "640 x 480", "MEDIUM": "800 x 600", "HIGH": "1024 x 768", "NORMAL": "1200 x 1600"})

      item = nwidget.HList(padding=25)
      item.add(label, 150)
      item.add(options)

      block.add(item, -1, 25)

      ok = i.accept()
      ok.on_click = "ARROW_CLICK"
      ok.bounds(720, 90, 752, 122)
      self.__widgets.append(ok)

      reject = i.reject()
      reject.on_click = "ARROW_CLICK"
      reject.bounds(755, 360, 775, 380)
      self.__widgets.append(reject)

    self.run_pyglet(runner, draw, update)

if __name__ == "__main__":
  unittest.main()
