# Copyright 2013 Douglas Linder
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:
# 
#   http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import
import nwidget
from .enum import enum
from .assets import Assets
from .consts import *

# Defined set of text types used by the theme
text_type = enum("NORMAL", "SMALL", "HEADER", "SUBHEADER", "LABEL")


class Dummy():
  """ Dummy theme to use as a template """

  def __init__(self, path="", window=None):
    self.__assets = Assets(path)
    self.__window = window

  def panel(self):
    """ Returns a themed panel """
    pass

  def subpanel(self):
    """ Returns a themed panel for inside a panel """
    pass

  def button(self):
    """ Returns a themed button """
    pass

  def text(self):
    """ Returns a generic themed label """
    pass

  def hint(self):
    """ Return a themed label for tiny hints """
    pass

  def header(self):
    """ Return a themed label for a heading """
    pass

  def subheader(self):
    """ Return a themed label for a subheading """
    pass

  def label(self):
    """ Return a label for a form element """
    pass

  def options(self, options):
    """ Returns an option select for the given dictionary of key -> value pairs """
    pass

  def textbox(self):
    """ Return a themed text area for text input """
    pass

  def checkbox(self):
    """ Returns an X / [] checkbox toggle button """
    pass

  def progress(self):
    """ Returns a themed progress bar """
    pass

  def accept(self):
    """ Returns a themed image button for 'accept' """
    pass

  def reject(self):
    """ Returns a themed image button for 'reject' """
    pass

  def arrow_left(self):
    """ Returns a themed image button with a 'left' arrow """
    pass

  def arrow_right(self):
    """ Returns a themed image button with a 'right' arrow """
    pass

  def arrow_up(self):
    """ Returns a themed image button with a 'up' arrow """
    pass

  def arrow_down(self):
    """ Returns a themed image button with a 'down' arrow """
    pass


class Light():
  """ A simple black-on-white theme for nwidget """

  def __init__(self, path, window=None):
    """ Create a theme instance with a base path reference.
        Window may be None, but no events will be bound if so.
    """
    self.__assets = nwidget.Assets(path)
    self.__window = window

  def panel(self):
    """ Returns a themed panel """
    a = self.__assets
    rtn = nwidget.Panel()
    rtn.texture = a.resolve("panel.png")
    return rtn

  def subpanel(self):
    """ Returns a themed panel """
    a = self.__assets
    rtn = nwidget.Panel()
    rtn.texture = a.resolve("subpanel.png")
    return rtn

  def button(self):
    """ Returns a themed button """
    a = self.__assets
    rtn = nwidget.Button()
    rtn.texture = a.resolve("button.png")
    rtn.texture_over = a.resolve("button_over.png")
    rtn.texture_down = a.resolve("button_down.png")
    rtn.texture_disabled = a.resolve("button_disabled.png")
    rtn.font_color = (30, 30, 30, 255)
    rtn.font_over = (0, 0, 0, 255)
    rtn.font_down = (100, 100, 110, 255)
    rtn.font_disabled = (90, 90, 90, 255)
    rtn.text = "Button"
    rtn.font = a.resolve("roboto.ttf")
    rtn.font_size = self.__font_size()
    if platform == platforms.WINDOWS:
      rtn.label_offset = -1
    rtn.on_click = ""
    rtn.register(self.__window)
    return rtn

  def text(self):
    """ Return a label for text output """
    a = self.__assets
    rtn = nwidget.Label()
    rtn.color = (30, 30, 30, 255)
    rtn.text = "Label"
    rtn.font = a.resolve("roboto.ttf")
    rtn.align = nwidget.align.LEFT
    rtn.valign = nwidget.align.TOP
    rtn.size = self.__font_size()
    return rtn

  def hint(self):
    """ Return a label for tiny hints """
    a = self.__assets
    rtn = nwidget.Label()
    rtn.color = (90, 90, 90, 255)
    rtn.text = "Label"
    rtn.font = a.resolve("roboto.ttf")
    rtn.align = nwidget.align.LEFT
    rtn.valign = nwidget.align.CENTER
    rtn.size = self.__font_size(text_type.SMALL)
    return rtn

  def textbox(self):
    """ Return a text area for text input """
    a = self.__assets
    rtn = nwidget.Textbox()
    rtn.panel = a.resolve("textbox.png")
    rtn.panel_focus = a.resolve("textbox_focus.png")
    rtn.color = (30, 30, 30, 255)
    rtn.text = "Textbox"
    rtn.font = a.resolve("roboto.ttf")
    rtn.size = self.__font_size()
    rtn.register(self.__window)
    return rtn

  def header(self):
    """ Return a themed label for a heading """
    a = self.__assets
    rtn = nwidget.Label()
    rtn.color = (20, 20, 20, 255)
    rtn.text = "Header"
    rtn.font = a.resolve("aller.ttf")
    rtn.size = self.__font_size(text_type.HEADER)
    return rtn

  def subheader(self):
    """ Return a themed label for a subheading """
    a = self.__assets
    rtn = nwidget.Label()
    rtn.color = (70, 70, 70, 255)
    rtn.text = "Header"
    rtn.font = a.resolve("aller.ttf")
    rtn.size = self.__font_size(text_type.SUBHEADER)
    return rtn

  def label(self):
    """ Return a themed label for a subheading """
    a = self.__assets
    rtn = nwidget.Label()
    rtn.color = (70, 70, 70, 255)
    rtn.text = "Label:"
    rtn.font = a.resolve("roboto.ttf")
    rtn.align = nwidget.align.RIGHT
    rtn.size = self.__font_size(text_type.LABEL)
    return rtn

  def options(self, options):
    """ Returns an option select for the given dictionary of key -> value pairs """
    rtn = nwidget.Toggle()
    rtn.register(self.__window)
    for k in options.keys():
      element = self.button()
      element.text = options[k]
      rtn.add(element, k)
    return rtn

  def checkbox(self):
    """ Returns an X / [] checkbox toggle button """
    a = self.__assets
    t = a.resolve("toggle.png")
    rtn = nwidget.Toggle()
    rtn.register(self.__window)
    b = nwidget.ImageButton(
      texture=t,
      texture_down=t,
      texture_over=t,
      uv=(0, 0, 0.25, 0, 0.25, 0.25, 0, 0.25),
      uv_over=(0.25, 0, 0.5, 0, 0.5, 0.25, 0.25, 0.25),
      uv_down=(0.5, 0, 0.75, 0, 0.75, 0.25, 0.5, 0.25)
    )
    b.register(self.__window)
    rtn.add(b, "ON")
    b = nwidget.ImageButton(
      texture=t,
      texture_down=t,
      texture_over=t,
      uv=(0, 0.25, 0.25, 0.25, 0.25, 0.5, 0, 0.5),
      uv_over=(0.25, 0.25, 0.5, 0.25, 0.5, 0.5, 0.25, 0.5),
      uv_down=(0.5, 0.25, 0.75, 0.25, 0.75, 0.5, 0.5, 0.5)
    )
    b.register(self.__window)
    rtn.add(b, "OFF")
    b = nwidget.Image(texture=t, uv=(0.75, 0, 1, 0, 1, 0.25, 0.75, 0.25))
    rtn.disabled_widget = b
    return rtn

  def progress(self):
    """ Returns a themed progress bar """
    a = self.__assets
    rtn = nwidget.Partial(texture=a.resolve("slider.png"), texture_under=a.resolve("slider_under.png"), panel=True)
    rtn.anchor = nwidget.align.LEFT
    rtn.value = 0.5
    return rtn

  def accept(self):
    """ Returns a themed image button for 'accept' """
    a = self.__assets
    rtn = nwidget.ImageButton()
    rtn.from_row(a.resolve("icons.png"), (0, 0.5, 1, 0.75))
    rtn.register(self.__window)
    return rtn

  def reject(self):
    """ Returns a themed image button for 'reject' """
    a = self.__assets
    rtn = nwidget.ImageButton()
    rtn.from_row(a.resolve("icons.png"), (0, 0.75, 1, 1))
    rtn.register(self.__window)
    return rtn

  def arrow_left(self):
    """ Returns a themed image button with a 'left' arrow """
    a = self.__assets
    rtn = nwidget.ImageButton()
    rtn.from_row(a.resolve("arrows.png"), (0, 0.25, 1, 0.5))
    rtn.register(self.__window)
    return rtn

  def arrow_right(self):
    """ Returns a themed image button with a 'right' arrow """
    a = self.__assets
    rtn = nwidget.ImageButton()
    rtn.from_row(a.resolve("arrows.png"), (0, 0.5, 1, 0.75))
    rtn.register(self.__window)
    return rtn

  def arrow_up(self):
    """ Returns a themed image button with a 'up' arrow """
    a = self.__assets
    rtn = nwidget.ImageButton()
    rtn.from_row(a.resolve("arrows.png"), (0, 0, 1, 0.25))
    rtn.register(self.__window)
    return rtn

  def arrow_down(self):
    """ Returns a themed image button with a 'down' arrow """
    a = self.__assets
    rtn = nwidget.ImageButton()
    rtn.from_row(a.resolve("arrows.png"), (0, 0.75, 1, 1))
    rtn.register(self.__window)
    return rtn

  def __font_size(self, purpose=text_type.NORMAL):
    rtn = 10
    if purpose == text_type.NORMAL:
      if platform == platforms.WINDOWS:
        rtn = 9
      else:
        rtn = 10

    elif purpose == text_type.SMALL:
      if platform == platforms.WINDOWS:
        rtn = 6
      else:
        rtn = 7

    elif purpose == text_type.HEADER:
      if platform == platforms.WINDOWS:
        rtn = 14
      else:
        rtn = 15

    elif purpose == text_type.SUBHEADER:
      if platform == platforms.WINDOWS:
        rtn = 12
      else:
        rtn = 13

    elif purpose == text_type.LABEL:
      if platform == platforms.WINDOWS:
        rtn = 10
      else:
        rtn = 11

    return rtn

  def __uv(self, xmin, ymin, xmax, ymax):
    return [xmin, ymin, xmin, ymax, xmax, ymax, xmax, ymin]


class Gothic():
  """ A simple black-on-white theme for nwidget """

  def __init__(self, path, window=None):
    """ Create a theme instance with a base path reference.
        Window may be None, but no events will be bound if so.
    """
    self.__assets = nwidget.Assets(path)
    self.__window = window

  def panel(self):
    """ Returns a themed panel """
    a = self.__assets
    rtn = nwidget.Panel()
    rtn.texture = a.resolve("panel.png")
    return rtn

  def subpanel(self):
    """ Returns a themed panel """
    a = self.__assets
    rtn = nwidget.Panel()
    rtn.texture = a.resolve("subpanel.png")
    return rtn

  def button(self):
    """ Returns a themed button """
    a = self.__assets
    rtn = nwidget.Button()
    rtn.texture = a.resolve("button.png")
    rtn.texture_over = a.resolve("button_over.png")
    rtn.texture_down = a.resolve("button_down.png")
    rtn.texture_disabled = a.resolve("button_disabled.png")
    rtn.font_color = (205, 205, 205, 255)
    rtn.font_over = (255, 255, 255, 255)
    rtn.font_down = (100, 100, 110, 255)
    rtn.font_disabled = (90, 90, 90, 255)
    rtn.text = "Button"
    rtn.font = a.resolve("orotund.ttf")
    rtn.font_size = self.__font_size(text_type.LABEL)
    rtn.on_click = ""
    if platform == platforms.WINDOWS:
      rtn.label_offset = -1
    rtn.register(self.__window)
    return rtn

  def text(self):
    """ Return a label for text output """
    a = self.__assets
    rtn = nwidget.Label()
    rtn.color = (210, 210, 210, 255)
    rtn.text = "Label"
    rtn.font = a.resolve("orotund.ttf")
    rtn.align = nwidget.align.LEFT
    rtn.valign = nwidget.align.TOP
    rtn.size = self.__font_size()
    return rtn

  def hint(self):
    """ Return a label for tiny hints """
    a = self.__assets
    rtn = nwidget.Label()
    rtn.color = (255, 255, 255, 255)
    rtn.text = "Label"
    rtn.font = a.resolve("orotund.ttf")
    rtn.align = nwidget.align.LEFT
    rtn.valign = nwidget.align.CENTER
    rtn.size = self.__font_size(text_type.SMALL)
    return rtn

  def textbox(self):
    """ Return a text area for text input """
    a = self.__assets
    rtn = nwidget.Textbox()
    rtn.panel = a.resolve("textbox.png")
    rtn.panel_focus = a.resolve("textbox_focus.png")
    rtn.color = (210, 210, 210, 255)
    rtn.caret_color = (255, 255, 195)
    rtn.text = "Textbox"
    rtn.font = a.resolve("orotund.ttf")
    rtn.size = self.__font_size()
    rtn.register(self.__window)
    return rtn

  def header(self):
    """ Return a themed label for a heading """
    a = self.__assets
    rtn = nwidget.Label()
    rtn.color = (255, 255, 255, 255)
    rtn.text = "Header"
    rtn.font = a.resolve("deutsch.ttf")
    rtn.size = self.__font_size(text_type.HEADER)
    return rtn

  def subheader(self):
    """ Return a themed label for a subheading """
    a = self.__assets
    rtn = nwidget.Label()
    rtn.color = (245, 245, 245, 255)
    rtn.text = "Header"
    rtn.font = a.resolve("deutsch.ttf")
    rtn.size = self.__font_size(text_type.SUBHEADER)
    return rtn

  def label(self):
    """ Return a themed label for a subheading """
    a = self.__assets
    rtn = nwidget.Label()
    rtn.color = (225, 225, 225, 255)
    rtn.text = "Label:"
    rtn.font = a.resolve("orotund.ttf")
    rtn.align = nwidget.align.RIGHT
    rtn.size = self.__font_size(text_type.LABEL)
    return rtn

  def options(self, options):
    """ Returns an option select for the given dictionary of key -> value pairs """
    rtn = nwidget.Toggle()
    rtn.register(self.__window)
    for k in options.keys():
      element = self.button()
      element.text = options[k]
      rtn.add(element, k)
    return rtn

  def checkbox(self):
    """ Returns an X / [] checkbox toggle button """
    a = self.__assets
    t = a.resolve("toggle.png")
    rtn = nwidget.Toggle()
    rtn.register(self.__window)
    b = nwidget.ImageButton(
      texture=t,
      texture_down=t,
      texture_over=t,
      uv=(0, 0, 0.25, 0, 0.25, 0.25, 0, 0.25),
      uv_over=(0.25, 0, 0.5, 0, 0.5, 0.25, 0.25, 0.25),
      uv_down=(0.5, 0, 0.75, 0, 0.75, 0.25, 0.5, 0.25)
    )
    b.register(self.__window)
    rtn.add(b, "ON")
    b = nwidget.ImageButton(
      texture=t,
      texture_down=t,
      texture_over=t,
      uv=(0, 0.25, 0.25, 0.25, 0.25, 0.5, 0, 0.5),
      uv_over=(0.25, 0.25, 0.5, 0.25, 0.5, 0.5, 0.25, 0.5),
      uv_down=(0.5, 0.25, 0.75, 0.25, 0.75, 0.5, 0.5, 0.5)
    )
    b.register(self.__window)
    rtn.add(b, "OFF")
    b = nwidget.Image(texture=t, uv=(0.75, 0, 1, 0, 1, 0.25, 0.75, 0.25))
    rtn.disabled_widget = b
    return rtn

  def progress(self):
    """ Returns a themed progress bar """
    a = self.__assets
    rtn = nwidget.Partial(texture=a.resolve("slider.png"), texture_under=a.resolve("slider_under.png"), panel=True)
    rtn.anchor = nwidget.align.LEFT
    rtn.value = 0.5
    return rtn

  def accept(self):
    """ Returns a themed image button for 'accept' """
    a = self.__assets
    rtn = nwidget.ImageButton()
    rtn.from_row(a.resolve("icons.png"), (0, 0.75, 1, 1))
    rtn.register(self.__window)
    return rtn

  def reject(self):
    """ Returns a themed image button for 'reject' """
    a = self.__assets
    rtn = nwidget.ImageButton()
    rtn.from_row(a.resolve("icons.png"), (0, 0.5, 1, 0.75))
    rtn.register(self.__window)
    return rtn

  def arrow_left(self):
    """ Returns a themed image button with a 'left' arrow """
    a = self.__assets
    rtn = nwidget.ImageButton()
    rtn.from_row(a.resolve("arrows.png"), (0, 0.25, 1, 0.5))
    rtn.register(self.__window)
    return rtn

  def arrow_right(self):
    """ Returns a themed image button with a 'right' arrow """
    a = self.__assets
    rtn = nwidget.ImageButton()
    rtn.from_row(a.resolve("arrows.png"), (0, 0.5, 1, 0.75))
    rtn.register(self.__window)
    return rtn

  def arrow_up(self):
    """ Returns a themed image button with a 'up' arrow """
    a = self.__assets
    rtn = nwidget.ImageButton()
    rtn.from_row(a.resolve("arrows.png"), (0, 0, 1, 0.25))
    rtn.register(self.__window)
    return rtn

  def arrow_down(self):
    """ Returns a themed image button with a 'down' arrow """
    a = self.__assets
    rtn = nwidget.ImageButton()
    rtn.from_row(a.resolve("arrows.png"), (0, 0.75, 1, 1))
    rtn.register(self.__window)
    return rtn

  def __font_size(self, purpose=text_type.NORMAL):
    rtn = 10
    if purpose == text_type.NORMAL:
      rtn = 10

    elif purpose == text_type.SMALL:
      if platform == platforms.WINDOWS:
        rtn = 7
      else:
        rtn = 7

    elif purpose == text_type.HEADER:
      rtn = 17

    elif purpose == text_type.SUBHEADER:
      if platform == platforms.WINDOWS:
        rtn = 14
      else:
        rtn = 13

    elif purpose == text_type.LABEL:
      rtn = 11

    return rtn

  def __uv(self, xmin, ymin, xmax, ymax):
    return [xmin, ymin, xmin, ymax, xmax, ymax, xmax, ymin]

