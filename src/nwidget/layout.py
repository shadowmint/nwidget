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
from .factory import Factory
from datetime import datetime
from .widgets import Block, Primitive
from .theme import Dummy
from .consts import *
from .log import error
from .assets import Assets
import pyglet
import math
import time


#region pycharm-code-complete-helpers
def edge(anchor, edge, unit):
  pass
def bound(xmin, ymin, xmax, ymax):
  pass
def widget(widget, bounds=None, keep=True, **kwargs):
  pass
window = 0
assets = Assets()
theme = Dummy()
TOP = 0
BOTTOM = 0
LEFT = 0
RIGHT = 0
PX = 0
PIXELS = 0
MM = 0
PERCENT = 0
INCH = 0
class CenterType(object):
  def __init__(self):
    self.X = 0
    self.Y = 0
CENTER = CenterType()
#endregion


class InvalidBoundsException(Exception):
  pass


class LayoutBase(object):
  """ Base type to extend when writing a ui layout """

  def __init__(self):
    self.timestamp = datetime.now()

  def widgets(self, helper):
    """ Override with widget list; return array of widgets """
    raise Exception("Not implemented")

  def sync(self, data):
    """ Override to set the state of the widget set """
    raise Exception("Not implemented")


class Helper():
  """ Helper class passed tot he layout base.
      Import the scope using helper.scope(globals())
  """

  def __init__(self, edge, bound, widget, theme, window, assets, xmin, ymin, xmax, ymax, xcenter, ycenter):
    self.edge = edge
    self.bound = bound
    self.widget = widget
    self.theme = theme
    self.window = window
    self.assets = assets
    self.TOP = ymax
    self.BOTTOM = ymin
    self.LEFT = xmin
    self.RIGHT = xmax
    self.PX = units.PX
    self.PIXELS = units.PX
    self.MM = units.MM
    self.PERCENT = units.PERCENT
    self.INCH = units.INCH
    self.CENTER = CenterType()
    self.CENTER.X = xcenter
    self.CENTER.Y = ycenter

  def scope(self, g):
    for i in self.__dict__.keys():
      g[i] = self.__dict__[i]


class Bound():
  """ A 4 point bound """

  def __init__(self, xmin, ymin, xmax, ymax):
    self.xmin = xmin
    self.ymin = ymin
    self.xmax = xmax
    self.ymax = ymax

  def apply(self, widget):
    widget.bounds(self.xmin, self.ymin, self.xmax, self.ymax)


class Edge():
  """ An edge marker """

  def __init__(self, wbounds, edge, offset, unit):
    """ Create a new instance with given edge, offset, units, calculate pixel values.
        Notice wbounds is a Bounds object for the window, not the window itself.
    """

    # If this a manually created edge value
    if edge in [align.LEFT, align.TOP, align.RIGHT, align.BOTTOM] and unit == units.PX:
      self.offset = offset
      self.axis = axis.X
      if edge == align.TOP or edge == align.BOTTOM:
        self.axis = axis.Y

    # Bad request
    elif edge in [align.LEFT, align.TOP, align.RIGHT, align.BOTTOM]:
      raise Exception("Invalid edge; can only be align if pixel value given")

    # Bad edge
    elif edge is None:
      raise Exception("Edge required")

    # Calculated edge value
    else:
      value = self.__resolve(wbounds, edge.axis, offset, unit)
      self.offset = edge.offset + value
      self.axis = edge.axis

  def __resolve(self, wbounds, ax, offset, unit):
    """ Does units -> pixels calculation """
    ov = math.fabs(offset)
    rtn = 0
    if unit == units.PX:
      rtn = ov
    elif unit == units.PERCENT:
      if ax == axis.X:
        rtn = (wbounds.xmax - wbounds.xmin) * (ov / 100.0)
      else:
        rtn = (wbounds.ymax - wbounds.ymin) * (ov / 100.0)
    elif unit == units.MM:
      rtn = dpmm * ov
    elif unit == units.INCH:
      rtn = dpi * ov
    return math.copysign(rtn, offset)


class Layout(Primitive):
  """ ... """

  def __init__(self, window, theme, assets, path):
    """ Load a widget layout with a specific theme.

        Notice that the layout file has to not only extend
        LayoutBase, but also set an instance of the class to
        the module property 'layout'
    """
    super(Layout, self).__init__()
    self.__factory = Factory()
    self.__show_bounds = False
    self.__show_edges = False
    self.__marker = None
    self.__widgets = []
    self.__bounds = []
    self.__edges = []
    self.__factory.load(path)
    self.__layout = self.__factory.prop("layout")
    self.__theme = theme
    self.__window = window
    self.__assets = assets
    self.model = None
    bounds = window.get_size()
    self.xmin = 0
    self.ymin = 0
    self.xmax = bounds[0]
    self.ymax = bounds[1]
    self.__reload()

  def show_edges(self, visible):
    """ Call this to turn on and off edge bound displays """
    self.__show_edges = visible

  def show_bounds(self, visible):
    """ Call this to turn on and off area bounds displays """
    self.__show_bounds = visible

  def __get_marker(self):
    """ Render the render help marker, create if required """
    if self.__marker is None:
      self.__marker = Block(solid=True)
    return self.__marker

  def edge(self, anchor, distance, unit):
    """ Special function to resolve an edge
        eg. b_left = edge(TOP, -10, PERCENT)

        Notice that TOP and RIGHT are +ve values, and to be inside
        the given layout a *negative* value must be added to them.
    """
    e = Edge(self.__wbounds, anchor, distance, unit)
    self.__edges.append(e)
    return e

  def bound(self, xmin, ymin, xmax, ymax):
    """ Special function to resolve a bounding rectangle
        eg. my_block = block(b_left, b_bottom, RIGHT, TOP)
    """
    b = Bound(xmin.offset, ymin.offset, xmax.offset, ymax.offset)
    self.__bounds.append(b)
    return b

  def __reload(self):
    """ Reload widget set, apply bounds and styles """

    # Reset
    self.__widgets = []
    self.__bounds = []
    self.__edges = []

    # Create a set of markers specifically for this window
    # The layout should use these to build the layout
    self.__wbounds = Bound(self.xmin, self.ymin, self.xmax, self.ymax)
    helper = Helper(
      self.edge,
      self.bound,
      self.widget,
      self.__theme,
      self.__window,
      self.__assets,
      Edge(self.__wbounds, align.LEFT, self.xmin, units.PX),
      Edge(self.__wbounds, align.BOTTOM, self.ymin, units.PX),
      Edge(self.__wbounds, align.RIGHT, self.xmax, units.PX),
      Edge(self.__wbounds, align.TOP, self.ymax, units.PX),
      Edge(self.__wbounds, align.LEFT, self.xmin + self.xmax / 2, units.PX),
      Edge(self.__wbounds, align.TOP, self.ymin + self.ymax / 2, units.PX),
    )

    # Load
    try:
      self.__layout.widgets(helper)
    except Exception, e:
      error("Invalid layout file detected", e)
      time.sleep(0.5)  # Cool off, don't spam

  def is_sequence(self, arg):
    return (not hasattr(arg, "strip") and
            hasattr(arg, "__getitem__") or
            hasattr(arg, "__iter__"))

  def widget(self, widget, bounds=None, keep=True, **styles):
    """ Load a widget, apply the bounds and styles to it

        The properties in styles are attached as style elements to
        the widget, except for left, right, top, bottom, x, y, width
        and height which are ignored if bounds is supplied, or used
        to construct bounds if it is None.

        The only other 'special' property is keep, which controls
        if a widget is kept in the internal reference for the layout.
        By default this is true, but in some circumstances it may
        be desirable to make it false. For example:

          items = widget(nwidget.VList(), left=...)
          items.add(widget(theme.button(), keep=False, left=...))

        
    """
    if bounds is None:
      if all (k in styles.keys() for k in ("left","right", "top", "bottom")):
        if self.is_sequence(styles["left"]):
          left = self.edge(*styles["left"])
        else:
          left = styles["left"] # Eg. Someone passes a real bound, or LEFT in
        if self.is_sequence(styles["top"]):
          top = self.edge(*styles["top"])
        else:
          top = styles["top"]
        if self.is_sequence(styles["bottom"]):
          bottom = self.edge(*styles["bottom"])
        else:
          bottom = styles["bottom"]
        if self.is_sequence(styles["right"]):
          right = self.edge(*styles["right"])
        else:
          right = styles["right"]
        bounds = self.bound(left, bottom, right, top)
      elif all (k in styles.keys() for k in ("x","y", "width", "height")):
        x = self.edge(*styles["x"])
        y = self.edge(*styles["y"])
        width = styles["width"][0]
        wunits = styles["width"][1]
        height = styles["height"][0]
        hunits = styles["height"][1]
        left = self.edge(x, -width / 2.0, wunits)
        right = self.edge(x, width / 2.0, wunits)
        bottom = self.edge(y, -height / 2.0, hunits)
        top = self.edge(y, height / 2.0, hunits)
        bounds = self.bound(left, bottom, right, top)

      # If we're not keeping the widget we don't care about the bounds;
      # the ui can look after that itself.
      elif keep:
        raise InvalidBoundsException("Invalid bounds")

    if bounds is not None:
      bounds.apply(widget)

    # Remove edge styles
    styles.pop("left", None)
    styles.pop("right", None)
    styles.pop("top", None)
    styles.pop("bottom", None)
    styles.pop("width", None)
    styles.pop("height", None)
    styles.pop("x", None)
    styles.pop("y", None)

    for key in styles.keys():
      value = styles[key]
      setattr(widget, key, value)
    if keep:
      self.__widgets.append(widget)
    return widget

  def watch(self, watching=True):
    """ Turn on watching for file changes """
    self.__factory.watch(watching)

  def __render_edges(self):
    """ Render edges """
    m = self.__get_marker()
    for e in self.__edges:
      m.color = (255, 255, 0, 50)
      if e.axis == axis.X:
        m.bounds(e.offset - 1, self.__wbounds.ymin, e.offset + 1, self.__wbounds.ymax)
      else:
        m.bounds(self.__wbounds.xmin, e.offset - 1, self.__wbounds.xmax, e.offset + 1)
      m.draw()

  def __render_bounds(self):
    """ Debug render bounds """
    m = self.__get_marker()
    for b in self.__bounds:
      m.color = (0, 255, 255, 128)
      b.apply(m)
      m.draw()

  def _draw(self):
    """ Render the layout; if watching, check for changes.
        The given model is passed to the UI for rendering each frame.
        The UI itself has to smartly handle the content of the model.
    """
    if self._updated:
      self.__reload()
      self._updated = False
    try:
      l = self.__factory.prop("layout")
      if l.timestamp != self.__layout.timestamp:
        self.__layout = l
        self.__reload()
      self.__layout.sync(self.model)
      for w in self.__widgets:
        w.draw()
      if self.__show_bounds:
        self.__render_bounds()
      if self.__show_edges:
        self.__render_edges()
    except Exception, e:
      error("Invalid layout file detected", e)
      time.sleep(0.5)  # Cool off, dont spam

