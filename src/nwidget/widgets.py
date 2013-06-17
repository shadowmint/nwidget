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
from __future__ import division
import math
import pyglet
from . import events
from .factory import Factory
from .consts import align, widget
from .log import trace, error


class Primitive(object):
  """ Base type for all Primitives """
  
  _updated = False
  """ If this Primitive has been updated by a property set """
  
  _props = {}
  """ Set of properties held """
  
  __magic_keys = ["_props", "_updated"]
  
  def __init__(self):    
    self._props = {}
    self._updated = True
    self.xmin = 0             # Minimum x bound
    self.xmax = 0             # Maximum x bound
    self.ymin = 0             # Minimum y bound
    self.ymax = 0             # Maximum y bound
    self.visible = True       # If the primitive is rendered
    self._registered = False  # If the primitive has already bound events
    self.__window = None      # Reference to the root event handler
  
  def bounds(self, xmin, ymin, xmax, ymax):
    self.xmin = xmin
    self.xmax = xmax
    self.ymin = ymin
    self.ymax = ymax
    return self
    
  def draw(self):
    if self.visible:
      self._draw()
      if not self._registered:
        try:
          if not self.__window is None:
            self._registered = True
            self._register(self.__window)
        except Exception, e:
          error("Failed to register events on widget '%s'" % self, e)
          
  def _draw(self):
    """ Override with details of how to draw this """
    pass

  def register(self, window):
    """ Attach the window to register events with later """
    self.__window = window

  def _register(self, window):
    """ Override in widget with event bindings """
    pass

  @staticmethod
  def assets():
    """ Cache of loaded assets by path """
    try:
      rtn = Primitive.__assets
    except AttributeError:
      Primitive.__assets = {}
      rtn = Primitive.__assets
    return rtn
  
  @staticmethod
  def clear_assets():
    Primitive.__assets = {}
    
  def __getattr__(self, key):
    #print("Get attribute: %s -> %r" % (str(key), self.__dict__))
    if key.startswith("_"):
      return self.__dict__[key]
    return self._props[key]

  def __setattr__(self, key, value):
    #print("Set attribute: %s -> %s"%(str(key), str(value)))
    if key in self.__magic_keys:
      self.__dict__[key] = value
    elif key.startswith("_"):
      self.__dict__[key] = value
    else:
      if not key in self._props:
        self._props[key] = value
        self._updated = True
      else:
        if not self._props[key] == value and not self._props[key] is value:
          self._props[key] = value
          self._updated = True
        
        
class Block(Primitive):
  
  def __init__(self, solid=False, color=(255, 255, 255, 128)):
    super(Block, self).__init__()
    self.solid = solid # Is this a solid?
    self.color = color # The color to render
  
  def __color(self):
    """ Some crazy pyglet thing makes colors max out at 127 """
    if len(self.color) != 4:
      raise Exception("Invalid color for block '%r' (RGBA required)" % (self.color,))
    return (int(self.color[0] / 2), int(self.color[1] / 2), int(self.color[2] / 2), int(self.color[3] / 2))
    
  def _draw(self):
    if self.solid:
      pyglet.graphics.draw_indexed(4, pyglet.gl.GL_TRIANGLES,
        [0, 1, 2, 0, 2, 3],
        ('v2i', (int(math.floor(self.xmin)), int(math.floor(self.ymin)),
                 int(math.floor(self.xmax)), int(math.floor(self.ymin)),
                 int(math.floor(self.xmax)), int(math.floor(self.ymax)),
                 int(math.floor(self.xmin)), int(math.floor(self.ymax)))),
        ('c4b', self.__color() * 4)
      )
    else:
      pyglet.graphics.draw_indexed(4, pyglet.gl.GL_LINE_LOOP,
        [0, 1, 2, 3],
        ('v2i', (int(math.floor(self.xmin)), int(math.floor(self.ymin)),
                 int(math.floor(self.xmax)), int(math.floor(self.ymin)),
                 int(math.floor(self.xmax)), int(math.floor(self.ymax)),
                 int(math.floor(self.xmin)), int(math.floor(self.ymax)))),
        ('c4b', self.__color() * 4)
      )
      
class Image(Primitive):
  
  def __init__(self, texture=None, uv=(0, 0, 1, 0, 1, 1, 0, 1)):
    super(Image, self).__init__()
    self.uv = uv           # UV coordinates for this image
    self.texture = texture # Path to the texture for this image
    self.__texture = None  # Actual texture instance
  
  def __reload(self):
    cache = Primitive.assets()
    if self.__texture is None:
      if not self.texture in cache:
        cache[self.texture] = pyglet.image.load(self.texture)
        trace("Loaded new image '%s'" % self.texture)
      self.__texture = cache[self.texture]
      
  def _draw(self):
    self.__reload()
    texture = self.__texture.get_texture()
    pyglet.gl.glEnable(texture.target)
    pyglet.gl.glBindTexture(texture.target, texture.id)
    pyglet.graphics.draw_indexed(4, pyglet.gl.GL_TRIANGLES,
      [0, 1, 2, 0, 2, 3], (
        'v2i', (
          int(math.floor(self.xmin)), int(math.floor(self.ymin)),
          int(math.floor(self.xmax)), int(math.floor(self.ymin)),
          int(math.floor(self.xmax)), int(math.floor(self.ymax)),
          int(math.floor(self.xmin)), int(math.floor(self.ymax)),
        )
      ), ('t2f', self.uv)
    )
    pyglet.gl.glDisable(texture.target)


class Label(Primitive):
  """ Label Primitive; notice font styles are given in the 'styles' property """
  
  def __init__(self, text="", font="", color=(255, 255, 255, 255), size=10, align=align.LEFT, valign=align.CENTER, keep=1):
    super(Label, self).__init__()
    self.text = text      # Text for this label
    self.font = font      # Font path for this label
    self.color = color    # RGBA color for this label
    self.size = size      # Font size in pixels
    self.align = align    # Horizontal alignment
    self.valign = valign  # Vertical alignment
    self.keep = keep      # Controls the behaviour of append()
    self._font = font     # System font name to use
    self._doc = None
    self._layout = None
    self._backup = False  # Used to trigger double refresh for drawing

  def append(self, text):
    """
        Adds more content to this label, prefixed with \n

        If the 'keep' value is > 0, the last 'keep' lines are retained,
        and the oldest lines are deleted off the front of the text content.

        Note this is carefully done to avoid a full rebuild.
    """
    if self.keep > 0:
      self.text += "\n" + text
      lines = self.text.split("\n")
      if len(lines) > self.keep:
        lines = lines[-self.keep:]
      text = "\n".join(lines)
    else:
      text = self.text + "\n" + text
    self.text = text
    self._doc.text = self.text
    self._updated = False

  def _update(self):
    """ Sync from styles, etc. to local properties 
        Notice we force a double update to get the vertical alignment.
    """
    if self._updated or self._backup:
      if self._updated:
        self._backup = True
      else:
        self._backup = False
      self._updated = False
      self._layout.x = self.xmin
      self._layout.y = self.ymin
      self._layout.width = self.xmax - self.xmin
      self._layout.height = self.ymax - self.ymin
      self._layout.multiline = True
      self._layout.content_valign = self._valign_key()
      self._doc.set_style(0, len(self.text), {
        "color" : self.color, 
        "font_name" : self._font,
        "font_size" : self.size,
        "align" : self._align_key(),
      })
      self._doc.text = self.text

  def _valign_key(self):
    if self.valign == align.TOP:
      return "top"
    elif self.valign == align.CENTER:
      return "center"
    elif self.valign == align.BOTTOM:
      return "bottom"
    return "center"
    
  def _align_key(self):
    if self.align == align.LEFT:
      return "left"
    elif self.align == align.RIGHT:
      return "right"
    elif self.align == align.CENTER:
      return "center"
    return "left"
    
  def _font_name(self, path):
    """Get the short name from the font's names table"""
    from fontTools import ttLib
    FONT_SPECIFIER_NAME_ID = 4
    FONT_SPECIFIER_FAMILY_ID = 1
    font = ttLib.TTFont(path)
    name = ""
    family = ""
    for record in font['name'].names:
      if record.nameID == FONT_SPECIFIER_NAME_ID and not name:
        if '\000' in record.string:
          name = unicode(record.string, 'utf-16-be').encode('utf-8')
        else:
          name = record.string
      elif record.nameID == FONT_SPECIFIER_FAMILY_ID and not family:
        if '\000' in record.string:
          family = unicode(record.string, 'utf-16-be').encode('utf-8')
        else:
          family = record.string
      if name and family:
        break

    # Can't figure out the right font name to put in the override?
    # Try turning debug mode on~
    debug = False
    if debug:
      for record in font['name'].names:
        if '\000' in record.string:
          item = unicode(record.string, 'utf-16-be').encode('utf-8')
        else:
          item = record.string
        trace("Potential name match for '%s': '%s'" % (path, item))

    # If there is an override because the fucking os name for the font
    # is different to the actual name of the font, then load and use 
    # that.
    factory = Factory()
    if factory.load(path + ".py"):
      name_mangler = factory.prop("font")
      name = name_mangler(name)

    return name, family
         
  def _load_font(self):
    """ Load a font, find the name, cache the result """
    cache = Primitive.assets()
    if not self.font == "":
      if not self.font in cache:
        pyglet.font.add_file(self.font)
        name, _ = self._font_name(self.font)
        cache[self.font] = name
        trace("Loaded font '%s' from %s" % (name, self.font))
      self._font = cache[self.font]
    
  def __reload(self):
    """ Load font, etc. """
    if self._doc is None:
      width = self.xmax - self.xmin
      height = self.ymax - self.ymin
      self._load_font()
      self._doc = pyglet.text.document.FormattedDocument(text=".")
      self._layout = pyglet.text.layout.ScrollableTextLayout(self._doc, width, height)
    self._update()
    
  def _draw(self):
    self.__reload()
    self._layout.draw()
    
    
class Widget(Primitive):
  """ A collection of primitives which are collectively drawn """

  def __init__(self):
    super(Widget, self).__init__()
    self._elements = []       # Set of elements held
    self.disabled = False     # If the widget is disabled

  def _rebuild(self):
    """ Override in widget with content builder """
    pass

  def _update(self):
    if self._updated:
      self._rebuild()
      self._updated = False
  
  def _draw(self):
    self._update()
    for i in self._elements:
      if not i is None:
        i.draw()
  
  def _intersects(self, x, y):
    return (x >= self.xmin) and (y >= self.ymin) and (x <= self.xmax) and (y <= self.ymax)

  
class PanelMap(object):
  """ Keeps track of pixel mappings 
      
      The PanelMap creates two arrays, a uv array that can used directly,
      and a set of bounds.
      
      In order to get the set of bounds for an arbitrary sizes block,
      pass the parent into the bounds() method.
      
      The UV values can be used directly.
  """
  
  def __init__(self, texture):
    cache = Primitive.assets()
    if not texture in cache:
      cache[texture] = pyglet.image.load(texture)
      trace("Loaded new image '%s'" % texture)
    self.__texture = cache[texture]
    self.uv = []
    self.left = 0       # Size of 'left' area pixels
    self.right = 0      # Size of 'right' area pixels
    self.top = 0        # Size of 'top' area pixels
    self.bottom = 0     # Size of 'bottom' area pixels
    self.__bounds = []
    self.__map()
  
    
  def __find_edges(self):
    """ Returns the offset in LEFT, RIGHT, TOP, BOTTOM in pixels """
    data = self.__texture.get_image_data()
    width = data.width
    height = data.height
    pixels = data.get_data("RGBA", -data.width * 4)
    
    self.left = 0
    for i in range(width):
      offset = 0 * width + i
      r = ord(pixels[offset*4+0])
      g = ord(pixels[offset*4+1])
      b = ord(pixels[offset*4+2])
      if r == 255 and g == 255 and b == 255:
        self.left += 1
      else:
        break
      
    self.right = 0
    for i in range(width):
      offset = 0 * width + (width - 1) - i
      r = ord(pixels[offset*4+0])
      g = ord(pixels[offset*4+1])
      b = ord(pixels[offset*4+2])
      if r == 255 and g == 255 and b == 255:
        self.right += 1
      else:
        break
      
    self.top = 0
    for i in range(height):
      offset = i * width + 0
      r = ord(pixels[offset*4+0])
      g = ord(pixels[offset*4+1])
      b = ord(pixels[offset*4+2])
      if r == 255 and g == 255 and b == 255:
        self.top += 1
      else:
        break
      
    self.bottom = 0
    for i in range(width):
      offset = (height - (i + 1)) * width + 0
      r = ord(pixels[offset*4+0])
      g = ord(pixels[offset*4+1])
      b = ord(pixels[offset*4+2])
      if r == 255 and g == 255 and b == 255:
        self.bottom += 1
      else:
        break
      
    # Remove edges
    data.set_data("RGBA", -width * 4, pixels)
    pixels = list(pixels)
    for i in range(width):
      offset = 0 * width + i
      pixels[offset*4+0] = chr(0)
      pixels[offset*4+1] = chr(0)
      pixels[offset*4+2] = chr(0)
      pixels[offset*4+3] = chr(0)
    for i in range(width):
      offset = (height - (i + 1)) * width + 0
      pixels[offset*4+0] = chr(0)
      pixels[offset*4+1] = chr(0)
      pixels[offset*4+2] = chr(0)
      pixels[offset*4+3] = chr(0)
    pixels = "".join(pixels)
    data.set_data("RGBA", -width * 4, pixels)
        
    return (
      self.left / width, 
      self.right / width, 
      self.top / height,
      self.bottom / height
    )
  
  def __map(self):
    """ Explore the loaded texture and divide it into UV blocks 
        Sets 9 UV coordinate maps for Top left, top, right, etc.
    """
    left, right, top, bottom = self.__find_edges()
    self.uv = [
      (0, 1 - top, left, 1 - top, left, 1, 0, 1), # TL
      (left, 1 - top, 1 - right, 1 - top, 1 - right, 1, left, 1), # T
      (1 - right, 1 - top, 1, 1 - top, 1, 1, 1 - right, 1), # TR
      (0, bottom, left, bottom, left, 1 - top, 0, 1 - top), # L
      (left, bottom, 1 - right, bottom, 1 - right, 1 - top, left, 1 - top), # C
      (1 - right, bottom, 1, bottom, 1, 1 - top, 1 - right, 1 - top), # R
      (0, 0, left, 0, left, bottom, 0, bottom), # BL
      (left, 0, 1 - right, 0, 1 - right, bottom, left, bottom), # B
      (1 - right, 0, 1, 0, 1, bottom, 1 - right, bottom), # BR
    ]
    
  def bounds(self, parent):
    """ Pass the parent primitive to map over, a bound set will be returned. 
        Bounds are returned in the same order of as the UV coordinates:
    """
    top = self.top
    left = self.left
    right = self.right
    bottom = self.bottom
    xmin = parent.xmin
    xmax = parent.xmax
    ymin = parent.ymin
    ymax = parent.ymax
    data = [
      [xmin,         ymax - top,    xmin + left,  ymax],
      [xmin + left,  ymax - top,    xmax - right, ymax],
      [xmax - right, ymax - top,    xmax,         ymax],
      [xmin,         ymin + bottom, xmin + left,  ymax - top],
      [xmin + left,  ymin + bottom, xmax - right, ymax - top],
      [xmax - right, ymin + bottom, xmax,         ymax - top],
      [xmin,         ymin,          xmin + left,  ymin + bottom],
      [xmin + left,  ymin,          xmax - right, ymin + bottom],
      [xmax - right, ymin,          xmax,         ymin + bottom],
    ]

    # If any values are outside the bounds, fix them
    for b in data:
      if b[0] > b[2]:
        b[0] = b[2]
      if b[1] > b[3]:
        b[1] = b[3]

    return data  
    
    
class Panel(Widget):
  """ A collection of images arranged into the typical 9-grid as a background panel. 
  
      The layout of an image is used to control the texture distribution.
      
      The image should be in the form:
      
      BBBBWWWWWWWWWWBB
      B....---------..
      B..Image Data ..
      W---- Here    --
      W----         --
      W----         --
      B....------.....
      B....------.....
      
      ie. A single row and column on the top left of the image, that define the edges
      of the mapped section.
      
      The pixels inside the 'B' zone (.), frames by black pixels are not tiled and
      used as static edges for the panel.
      
      The 'W' zone pixels are tiled to form the edges (-) and the remainder of
      the image is tiled over the rest of the content ( ).
      
      Calculating the layout from an image is an expensive operation, but the results
      of the calculation are cached after the first time.
  """
  
  def __init__(self, texture=""):
    super(Panel, self).__init__()
    self.__map = None      # The texture mapping for this panel
    self.texture = texture # Texture for this panel
    
  def __key(self):
    return "Panel__" + self.texture
  
  def _rebuild(self):
    cache = Primitive.assets()
    self._elements = []
    if self.__map is None:
      if not self.__key() in cache:
        cache[self.__key()] = PanelMap(self.texture)
        trace("Loaded panel map for image '%s'" % self.texture)
      self.__map = cache[self.__key()]
    bounds = self.__map.bounds(self)
    for i in range(len(self.__map.uv)):
      uv = self.__map.uv[i]
      b = bounds[i]
      if b[0] >= self.xmin and b[1] >= self.ymin and b[2] <= self.xmax and b[3] <= self.ymax:
        item = Image()
        item.bounds(b[0], b[1], b[2], b[3])
        item.texture = self.texture
        item.uv = uv
        self._elements.append(item)
      
      # Debugging
      # bl = Block()
      # bl.bounds(b[0], b[1], b[2], b[3])
      # bl.solid = False
      # bl.color = (255, 0, 255, 255)
      # self._elements.append(bl)
  
  
class Button(Widget):
  """ Text button 

      Notice that there is no event handler on this widget;
      look at nwdiget.listen() to bind events against named
      triggers and set the trigger property to a specific id.

      Creating pretty buttons is a quite tiresome, see 
      nwidget.theme.* for some common bindings.

      You may manually trigger events using click()
  """
  def __init__(
      self,
      texture = None,
      texture_over = None,
      texture_down = None,
      texture_disabled = None,
      frame = (100, 100, 100, 255),
      frame_over = (130, 130, 130, 255),
      frame_down = (80, 80, 80, 255),
      frame_disabled = (40, 40, 40, 255),
      on_click = "",
      font_color = (0, 0, 0, 255),
      font_over = (10, 10, 10, 255),
      font_down = (255, 255, 255, 255),
      font_disabled = (10, 10, 10, 255),
      text = "",
      font = "",
      font_size = 10,
    ):
    super(Button, self).__init__()

    # Panel styles, used if self.texture is set
    self.texture = texture                   # texture if using a panel
    self.texture_over = texture_over         # texture if using a panel over
    self.texture_down = texture_down         # texture if using a panel down
    self.texture_disabled = texture_disabled # texture if using a panel disabled

    # Block styles, used if no texture
    self.frame = frame                       # Background color
    self.frame_over = frame_over             # Background color on over
    self.frame_down = frame_down             # Background color on down
    self.frame_disabled = frame_disabled     # Background color on disabled

    # State and events
    self.on_click = on_click                 # Event id triggered on click

    # Label colors
    self.font_color = font_color             # RGBA for text normally
    self.font_over = font_over               # RGBA for text when disabled
    self.font_down = font_down               # RGBA for text when disabled
    self.font_disabled = font_disabled       # RGBA for text when disabled

    # Label styles
    self.text = text                         # Text for this button
    self.font = font                         # Font path for this button
    self.font_size = font_size               # Font size in magical pyglet units
    self.label_offset = 0                    # Some fonts dont align properly; correct with this.
    
    # Internal state
    self.__state = widget.NORMAL
    self.__blocks = None
    self.__label = None

  def on_mouse_motion(self, x, y, dx, dy):
    """ Attach any handlers required for this widget """
    if self.__state == widget.NORMAL and self._intersects(x, y):
      self.__state = widget.OVER
      self.__reflow()
    elif self.__state == widget.OVER and not self._intersects(x, y):
      self.__state = widget.NORMAL
      self.__reflow()
    
  def on_mouse_press(self, x, y, press, modifiers):
    """ Attach any handlers required for this widget """
    if not self.__state == widget.DISABLED and self._intersects(x, y):
      self.__state = widget.DOWN
      self.__reflow()
    
  def on_mouse_release(self, x, y, press, modifiers):
    """ Attach any handlers required for this widget """
    if not self.__state == widget.DISABLED:
      if self._intersects(x, y):
        self.__state = widget.OVER
        self.__reflow()
        self.click()
      else:
        self.__state = widget.NORMAL
        self.__reflow()

  def click(self):
    """ Trigger click event """
    if self.on_click != "":
      events.trigger(self.on_click, self)

  def _register(self, window):
    """ Attach mouse tracking events """
    window.push_handlers(self)

  def __edge(self, color):
    """ Appropriate edge color """
    rtn = [
      int(color[0] / 2),
      int(color[1] / 2),
      int(color[2] / 2),
      255,
    ]
    return rtn
  
  def _rebuild(self):
    if self.disabled:
      self.__state = widget.DISABLED
    elif self.__state == widget.DISABLED:
      self.__state = widget.NORMAL
    self.__label = Label(font=self.font, color=self.font_color, size=self.font_size, text=self.text, align=align.CENTER, valign=align.CENTER)
    self.__label.bounds(self.xmin, self.ymin, self.xmax, self.ymax)
    if self.texture is None:
      self.__blocks = {
        widget.NORMAL : [
          Block(solid=True, color=self.frame), 
          Block(solid=False, color=self.__edge(self.frame)),
          Label(font=self.font, color=self.font_color, size=self.font_size, text=self.text, align=align.CENTER, valign=align.CENTER),
        ],
        widget.OVER : [
          Block(solid=True, color=self.frame_over), 
          Block(solid=False, color=self.__edge(self.frame_over)),
          Label(font=self.font, color=self.font_over, size=self.font_size, text=self.text, align=align.CENTER, valign=align.CENTER)
        ],
        widget.DOWN : [
          Block(solid=True, color=self.frame_down), 
          Block(solid=False, color=self.__edge(self.frame_down)),
          Label(font=self.font, color=self.font_down, size=self.font_size, text=self.text, align=align.CENTER, valign=align.CENTER)
        ],
        widget.DISABLED : [
          Block(solid=True, color=self.frame_disabled), 
          Block(solid=False, color=self.__edge(self.frame_disabled)),
          Label(font=self.font, color=self.font_disabled, size=self.font_size, text=self.text, align=align.CENTER, valign=align.CENTER)
        ],
      }
    else:
      self.__blocks = {
        widget.NORMAL : [
          Panel(texture=self.texture), 
          Label(font=self.font, color=self.font_color, size=self.font_size, text=self.text, align=align.CENTER, valign=align.CENTER),
        ],
        widget.OVER : [
          Panel(texture=self.texture_over), 
          Label(font=self.font, color=self.font_over, size=self.font_size, text=self.text, align=align.CENTER, valign=align.CENTER)
        ],
        widget.DOWN : [
          Panel(texture=self.texture_down), 
          Label(font=self.font, color=self.font_down, size=self.font_size, text=self.text, align=align.CENTER, valign=align.CENTER)
        ],
        widget.DISABLED : [
          Panel(texture=self.texture_disabled), 
          Label(font=self.font, color=self.font_disabled, size=self.font_size, text=self.text, align=align.CENTER, valign=align.CENTER)
        ],
      }
    for i in self.__blocks.keys():
      set = self.__blocks[i]
      for j in set:
        if isinstance(j, Label):
          j.bounds(self.xmin, self.ymin + self.label_offset, self.xmax, self.ymax + self.label_offset)
        else:
          j.bounds(self.xmin, self.ymin, self.xmax, self.ymax)
        j.draw()
    self.__reflow()
    
  def __reflow(self):
    """ Rebuild the display elements list """
    if not self.__blocks is None:
      self._elements = self.__blocks[self.__state]


class ImageButton(Widget):
  """ Image button with three states """
  
  def __init__(
    self,
    texture="",
    texture_over="",
    texture_down="",
    texture_disabled="",
    uv=(0, 0, 1, 0, 1, 1, 0, 1),
    uv_over=(0, 0, 1, 0, 1, 1, 0, 1),
    uv_down=(0, 0, 1, 0, 1, 1, 0, 1),
    uv_disabled=(0, 0, 1, 0, 1, 1, 0, 1),
    on_click = ""
  ):
    super(ImageButton, self).__init__()
    self.texture = texture                    # Texture for normal image
    self.texture_over = texture_over          # Texture for roll over
    self.texture_down = texture_down          # Texture for down
    self.texture_disabled = texture_disabled  # Texture for disabled
    self.uv = uv                              # UV coordinates for normal image
    self.uv_over = uv_over                    # UV coordinates for over image
    self.uv_down = uv_down                    # UV coordinates for down image
    self.uv_disabled = uv_disabled            # UV coordinates for disabled image
    self.on_click = on_click                  # Event triggered on a click
    
    # Internal state
    self.__state = widget.NORMAL
    self.__images = None
    
  def _rebuild(self):
    """ Rebuild the images for this widget """
    
    # Disabled?
    if self.disabled:
      self.__state = widget.DISABLED
    elif self.__state == widget.DISABLED:
      self.__state = widget.NORMAL
      
    # Set image set
    self.__images = {
      widget.NORMAL : [
        Image(texture=self.texture, uv=self.uv),
      ],
      widget.OVER : [
        Image(texture=self.texture_over, uv=self.uv_over)
      ],
      widget.DOWN : [
        Image(texture=self.texture_down, uv=self.uv_down)
      ],
      widget.DISABLED : [
        Image(texture=self.texture_disabled, uv=self.uv_disabled)
      ],
    }
    
    # Resize images
    for i in self.__images.keys():
      set = self.__images[i]
      for j in set:
        j.bounds(self.xmin, self.ymin, self.xmax, self.ymax)
        
    self.__reflow()
  
  def __reflow(self):
    """ Rebuild the display elements list """
    if not self.__images is None:
      self._elements = self.__images[self.__state]

  def click(self):
    """ Trigger click event """
    if self.on_click != "":
      events.trigger(self.on_click, self)

  def _register(self, window):
    """ Attach mouse tracking events """
    window.push_handlers(self)

  def on_mouse_motion(self, x, y, dx, dy):
    """ Attach any handlers required for this widget """
    if self.__state == widget.NORMAL and self._intersects(x, y):
      self.__state = widget.OVER
      self.__reflow()
    elif self.__state == widget.OVER and not self._intersects(x, y):
      self.__state = widget.NORMAL
      self.__reflow()
    
  def on_mouse_press(self, x, y, press, modifiers):
    """ Attach any handlers required for this widget """
    if not self.__state == widget.DISABLED and self._intersects(x, y):
      self.__state = widget.DOWN
      self.__reflow()
    
  def on_mouse_release(self, x, y, press, modifiers):
    """ Attach any handlers required for this widget """
    if not self.__state == widget.DISABLED:
      if self._intersects(x, y):
        self.__state = widget.OVER
        self.__reflow()
        self.click()
      else:
        self.__state = widget.NORMAL
        self.__reflow()
        
  def from_column(self, texture, bounds=(0, 0, 1, 1)):
    """ Loads the required properties automatically from an image.

        Assuming that the given bounds on the given texture are a 
        square in the form:

          +----------------------------
          + Texture
          +----------------------------
          + Texture over
          +----------------------------
          + Texture down
          +----------------------------
          + Texture disabled
          +----------------------------

        The bounds should be in the form (xmin, ymin, xmax, ymax) 
        and be uv coordinates. The default is the entire texture.
    """
    self.texture = texture
    self.texture_over = texture
    self.texture_down = texture
    self.texture_disabled = texture
    self.uv = self.__uv_from_bounds(bounds, (0, 0.75, 1, 1))
    self.uv_over = self.__uv_from_bounds(bounds, (0, 0.5, 1, 0.75))
    self.uv_down = self.__uv_from_bounds(bounds, (0, 0.25, 1, 0.5))
    self.uv_disabled = self.__uv_from_bounds(bounds, (0, 0, 1, 0.25))
  
  def from_row(self, texture, bounds=(0, 0, 1, 1)):
    """ Loads the required properties automatically from an image.

        Assuming that the given bounds on the given texture are a 
        square in the form:

          +-----------------------+
          +     +     +     +     +
          +  T  +  O  +  D  +  D  +
          +  e  +  v  +  o  +  i  +
          +  x  +  e  +  w  +  s  +
          +  t  +  r  +  n  +  a  +
          +  u  +     +     +  b  +
          +  r  +     +     +  l  +
          +  e  +     +     +  e  +
          +     +     +     +  d  +
          +     +     +     +     +
          +-----------------------+

        The bounds should be in the form (xmin, ymin, xmax, ymax) 
        and be uv coordinates. The default is the entire texture.
    """
    self.texture = texture
    self.texture_over = texture
    self.texture_down = texture
    self.texture_disabled = texture
    self.uv = self.__uv_from_bounds(bounds, (0, 0, 0.25, 1))
    self.uv_over = self.__uv_from_bounds(bounds, (0.25, 0, 0.5, 1))
    self.uv_down = self.__uv_from_bounds(bounds, (0.5, 0, 0.75, 1))
    self.uv_disabled = self.__uv_from_bounds(bounds, (0.75, 0, 1, 1))
  
  def from_square(self, texture, bounds=(0, 0, 1, 1)):
    """ Loads the required properties automatically from an image.

        Assuming that the given bounds on the given texture are a 
        square in the form:

          +---------------------------+
          +             +             +
          +   Texture   +     Over    +
          +             +             +
          +---------------------------+
          +             +             +
          +    Down     +   Disabled  +
          +             +             +
          +---------------------------+

        The bounds should be in the form (xmin, ymin, xmax, ymax) 
        and be uv coordinates. The default is the entire texture.
    """
    self.texture = texture
    self.texture_over = texture
    self.texture_down = texture
    self.texture_disabled = texture
    self.uv = self.__uv_from_bounds(bounds, (0, 0.5, 0.5, 1))
    self.uv_over = self.__uv_from_bounds(bounds, (0.5, 0.5, 1, 1))
    self.uv_down = self.__uv_from_bounds(bounds, (0, 0, 0.5, 0.5))
    self.uv_disabled = self.__uv_from_bounds(bounds, (0.5, 0, 1, 0.5))
    
  def __uv_from_bounds(self, base, bounds):
    """ Calculate a uv from a bound set """
    xmin = base[0]
    ymin = base[1]
    width = base[2] - base[0]
    height = base[3] - base[1]
    rtn = (
      xmin + bounds[0] * width,
      ymin + bounds[1] * height,
      xmin + bounds[2] * width,
      ymin + bounds[1] * height,
      xmin + bounds[2] * width,
      ymin + bounds[3] * height,
      xmin + bounds[0] * width,
      ymin + bounds[3] * height
    )
    return rtn


class TextArea(Label):
  """ An editable text area """

  def __init__(
    self,
    text="",
    font="",
    color=(255, 255, 255, 255),
    size=10,
    align=align.LEFT,
    valign=align.CENTER,
    multiline=True,
    caret_color=(0, 0, 0),
    limit=-1,
    on_change="",
    on_enter=""
  ):
    super(TextArea, self).__init__(text, font, color, size, align, valign)
    self.multiline = multiline      # If this is a single line
    self.caret_color = caret_color  # The color to draw the caret
    self.limit = limit              # Character limit, or -1 for none
    self.on_change = on_change      # The event to fire on text change
    self.on_enter = on_enter        # The event to fire on text change to + '\n'

    # Internals
    self.__focus = False
    self._caret = None

  def __reload(self):
    """ Load font, etc. """
    if self._doc is None:
      width = self.xmax - self.xmin
      height = self.ymax - self.ymin
      self._load_font()
      self._doc = pyglet.text.document.FormattedDocument(text=".")
      self._layout = pyglet.text.layout.IncrementalTextLayout(self._doc, width, height)
      self._caret = pyglet.text.caret.Caret(self._layout)
      self._caret.color = self.caret_color
      self._caret.visible = False
    self._update()

  def _register(self, window):
    window.push_handlers(self)

  def _draw(self):
    self.__reload()
    self._layout.draw()
    
  def focus(self, has_focus=True):
    self.__focus = has_focus
    if not self._caret is None:
      self._caret.visible = has_focus

  def change(self):
    self.text = self._doc.text
    self._updated = False
    if self.on_change != "":
      events.trigger(self.on_change, self)

  def enter(self):
    if self.on_enter != "":
      events.trigger(self.on_enter, self)

  def on_text(self, text):
    """ Caret isn't smart enough to do this properly; help out """
    if self.__focus:
      enter = "\n" in text or "\r" in text
      if not self.multiline:
        text = text.replace('\n', '')
        text = text.replace('\r', '')
      if self.limit == -1:
        self._caret.on_text(text)
        self.change()
      elif len(self._doc.text) < self.limit:
        self._caret.on_text(text)
        self.change()
      if enter:
        self.enter()
    
  def on_text_motion(self, motion, select=False):
    if self.__focus:
      self._caret.on_text_motion(motion, select)
  
  def on_text_motion_select(self, motion):
    if self.__focus:
      self._caret.on_text_motion_select(motion)
  
  def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
    if self.__focus:
      self._caret.on_mouse_scroll(x, y, scroll_x, scroll_y)
  
  def on_mouse_press(self, x, y, button, modifiers):
    if self.__focus:
      self._caret.on_mouse_press(x, y, button, modifiers)
  
  def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
    if self.__focus:
      self._caret.on_mouse_drag(x, y, dx, dy, buttons, modifiers)
  
  def on_activate(self):
    if self.__focus:
      self._caret.on_activate()
  
  def on_deactivate(self):
    if self.__focus:
      self._caret.on_deactivate()


class Textbox(Widget):
  """ A themed click-to-focus textbox widget """
  
  def __init__(
    self, 
    text="",
    font="",
    color=(255, 255, 255, 255),
    size=10,
    align=align.LEFT,
    valign=align.CENTER,
    multiline=True,
    caret_color=(0, 0, 0),
    limit=-1,
    padding=10,
    panel="",
    panel_focus="",
    on_change="",
    on_enter=""
  ):
    super(Textbox, self).__init__()

    # text config (see TextArea)
    self.text = text
    self.font = font
    self.color = color
    self.size = size
    self.align = align
    self.valign = valign
    self.multiline = multiline
    self.caret_color = caret_color
    self.limit = limit           

    # Panel properties
    self.padding = padding          # The padding between panel edge and text area
    self.panel = panel              # The image to use for the background panel
    self.panel_focus = panel_focus  # The image to use for the background when focued
    self.on_change = on_change      # Event triggered when the input changes
    self.on_enter = on_enter        # Event triggered when '\n' is entered

    self.__focus = False            # If this panel currently has focus
    self.__sets = None

  def _register(self, window):
    self.__text.register(window)
    window.push_handlers(self)
  
  def _rebuild(self):
    """ Build components """
    if self.__sets == None:
      self.__text = TextArea(
        text=self.text,
        font=self.font,
        color=self.color,
        size=self.size,
        align=self.align,
        valign=self.valign,
        multiline=self.multiline,
        caret_color=self.caret_color,
        limit=self.limit,
        on_change=self.on_change,
        on_enter=self.on_enter
      )
      self.__sets = {
        True : [
          Panel(texture=self.panel_focus),
          self.__text,
        ],
        False : [
          Panel(texture=self.panel),
          self.__text,
        ],
      }
      for s in self.__sets.keys():
        for w in self.__sets[s]:
          if isinstance(w, Panel):
            w.bounds(self.xmin, self.ymin, self.xmax, self.ymax)
          else:
            w.bounds(self.xmin + self.padding, self.ymin + self.padding, self.xmax - self.padding, self.ymax - self.padding)
    self._reflow()

  def _reflow(self):
    """ Change the active widget group """
    self._elements = self.__sets[self.__focus]
    self.__text.focus(self.__focus)

  def on_mouse_press(self, x, y, press, modifiers):
    """ Attach any handlers required for this widget """
    if self._intersects(x, y):
      self.__focus = True
      self._reflow()
    else:
      self.__focus = False
      self._reflow()
    

class List(Widget):
  """ Base class for list types """

  def __init__(self):
    super(List, self).__init__()
    self._items = []   # Set of items in this list
    self._sizes = {}   # Set of per-item size overrides
    self._bounds = []  # Array of pixel-size bounds for elements

  def add(self, widget, width=-1, height=-1):
    """ Add a widget to the list """
    self._updated = True
    self._items.append(widget)
    if width >= 0 or height >= 0:
      self._sizes[widget] = [width, height]

  def remove(self, widget):
    """ Remove a widget from the list """
    self._updated = True
    self._items.remove(widget)
    if widget in self._sizes:
      self._sizes.pop(widget, None)

  def clear(self):
    """ Remove all items """
    self._items = []
    self._sizes = {}
    self._bounds = []

  def any(self):
    """ If we have any items in this list """
    return len(self._items) > 0

  def item(self, index):
    """ Return a specific item """
    if 0 <= index < len(self._items):
      return self._items[index]
    return None

  def _rebuild(self):
    self._layout()
    for i in range(len(self._items)):
      b = self._bounds[i]
      self._items[i].bounds(*b)
    self._elements = self._items

  def _layout(self):
    """ Override in the sub-type """
    pass


class VList(List):
  """ Vertical list """

  def __init__(self, padding=0):
    super(VList, self).__init__()
    self.padding = padding

  def _layout(self):
    """  Figure out size and rebind """

    # Located defined size elements
    used = (len(self._items) - 1) * self.padding
    ucount = len(self._items)
    for i in self._sizes.keys():
      if self._sizes[i][1] > 0:
        used += self._sizes[i][1]
        ucount -= 1
    free_space = self.ymax - self.ymin - used

    # Size for auto-gen parts
    allocated = 0
    if ucount > 0:
      allocated = free_space / ucount

    # Apply sizing
    offset = 0
    default_height = allocated
    default_width = self.xmax - self.xmin
    for k in range(len(self._items)):
      widget = self._items[k]
      o = 0
      w = default_width
      h = default_height
      if widget in self._sizes:
        data = self._sizes[widget]
        if data[0] >= 0:
          w = data[0]
        if data[1] >= 0:
          h = data[1]
          if h < default_height:
            o = (default_height - h) / 2
      self._bounds.append([
        self.xmin,
        self.ymin + offset + o,
        self.xmin + w,
        self.ymin + offset + h + o
      ])
      offset += h + self.padding


class HList(List):
  """ Horizontal list """

  def __init__(self, padding=0):
    super(HList, self).__init__()
    self.padding = padding

  def _layout(self):
    """  Figure out size and rebind """

    # Located defined size elements
    used = (len(self._items) - 1) * self.padding
    ucount = len(self._items)
    for i in self._sizes.keys():
      if self._sizes[i][0] > 0:
        used += self._sizes[i][0]
        ucount -= 1
    free_space = self.xmax - self.xmin - used

    # Size for auto-gen parts
    allocated = 0
    if ucount > 0:
      allocated = free_space / ucount

    # Apply sizing
    offset = 0
    default_height = self.ymax - self.ymin
    default_width = allocated
    for k in range(len(self._items)):
      widget = self._items[k]
      o = 0
      w = default_width
      h = default_height
      if widget in self._sizes:
        data = self._sizes[widget]
        if data[0] >= 0:
          w = data[0]
        if data[1] >= 0:
          h = data[1]
          if h < default_height:
            o = (default_height - h) / 2
      self._bounds.append([
        self.xmin + offset,
        self.ymin + o,
        self.xmin + offset + w,
        self.ymin + h + o
      ])
      offset += w + self.padding


class Stack(List):
  """ A group of widgets with the same bounds

      Its occasionally useful to use this to combine, for example, a panel
      and a label into one item that can be rendered as a single widget.
  """

  def __init__(self):
    super(Stack, self).__init__()

  def _layout(self):
    """  Figure out size and rebind """
    for k in range(len(self._items)):
      self._bounds.append([self.xmin, self.ymin, self.xmax, self.ymax])


class Toggle(Widget):
  """ Toggles between multiple widgets on down event.

      Notice that, for example, a button being clicked
      swaps to the next state AND triggers the buttons on
      event. 

      Each widget has an associated name value, which is
      passed on the event.

      You can manually trigger events using change()
  """

  def __init__(self, disabled=False, disabled_widget=None, index=0, on_change=""):
    super(Toggle, self).__init__()
    self.index = index                      # Current selected widget index
    self.disabled = disabled                # If the widget is currently disabled
    self.disabled_widget = disabled_widget  # Widget to display when disabled
    self.on_change = ""                     # Event to trigger when it changes
    self.state = ""                         # State marker; set after change
    self._items = []                        # Set of items in this list
    self.__state = widget.NORMAL            # Current widget state
    self.__skeys = {}                       # Magic value associated with an index

  def add(self, widget, value):
    """ Add a widget to the list """
    self._updated = True
    self._items.append(widget)
    self.__skeys[widget] = value

  def remove(self, widget):
    """ Remove a widget from the list """
    self._updated = True
    self._items.remove(widget)
    self.__skeys.pop(widget, None)

  def on_mouse_release(self, x, y, press, modifiers):
    """ Trigger an event if required """
    if not self.__state == widget.DISABLED:
      if self._intersects(x, y):
        self.__state = widget.NORMAL
        self.change()

  def _register(self, window):
    window.push_handlers(self)

  def change(self):
    """ Trigger a change event """
    self.index += 1
    if self.index >= len(self._items):
      self.index = 0

    # Update state entry
    w = self._items[self.index]
    self.state = self.__skeys[w]

    self._updated = False
    self._reflow()
    if self.on_change != "":
        events.trigger(self.on_change, self)

  def _rebuild(self):

    # Update state
    if self.disabled:
      self.__state = widget.DISABLED
    else:
      self.__state = widget.NORMAL

    # No idea what changed, rebuild all
    if not self.disabled_widget is None:
      self.disabled_widget.bounds(self.xmin, self.ymin, self.xmax, self.ymax)
    for i in range(len(self._items)):
      self._items[i].bounds(self.xmin, self.ymin, self.xmax, self.ymax)

    # Always reflow
    self._reflow()

  def _reflow(self):
    if not self.__state == widget.DISABLED:
      self._elements = [self._items[self.index]]
    else:
      if not self.disabled_widget is None:
        self._elements = [self.disabled_widget]


class Select(Widget):
  """ An arbitrary container with a 'selected' cursor that moves.

      Use this to implement, for example, weapon select:

      << [ Gun ]   Sword    Duck >>

         ^                       ^
         Cursor                  Button 

      To use this, create a list, a pair of buttons and a
      'selected' marker. Layout of these items is up to the caller.

      The select simply keeps track of what's displayed in the
      list, and where the marker is.

      If the list is disabled, the buttons are disabled too.

      Use a semi-transparent Image for the select item,
      or a non-solid block, etc.

      To display health or other vary-over-time data,
      use a Partial.

      You may manually trigger events using next() and
      prev()

      If the display_count is less than the total number of
      elements in the list, only the current display_count
      items are shown.

      Nb. The bounds on the Select widget itself are ignored;
      set the bounds on the elements manually.
  """
  def __init__(
    self,
    next=None,
    prev=None,
    list=None,
    marker=None,
    disabled=False,
    index=0,
    display_count=-1,
    on_change=""
  ):
    super(Select, self).__init__()
    self.next = next                    # The next button
    self.prev = prev                    # The prev button
    self.marker = marker                # The selected element marker
    self.list = list                    # The list to display elements in
    self.disabled = disabled            # If this select is enabled or not
    self.display_count = display_count  # Count of items to display, at most
    self.display_start = index          # First displayed item, defaults to index
    self.index = index                  # Currently selected index
    self.on_change = on_change          # Change of selected item
    self.selected = ""                  # Id of selected item

    # Internals
    self._items = []           # Set of all items
    self._data = {}            # Set of per-item size overrides, and codes
    self._display = []         # Set of items currently on display
    self._disabled = disabled  # Cached disable state
    self._display_end = 0      # Last rendered item

    # Keep track of elements manually to avoid a massive rebuild for no reason
    # TODO: Replace this with a per-property updated state on Primitive
    self._next = None
    self._prev = None
    self._list = None
    self._list_updated = True

  def _on_next_event(self, code, widget):
    self.change()

  def _on_prev_event(self, code, widget):
    self.change(False)

  def add(self, widget, code="", width=-1, height=-1):
    """ Add a widget to the list """
    self._updated = True
    self._items.append(widget)
    self._data[widget] = [width, height, code]
    self._list_updated = True

  def remove(self, widget):
    """ Remove a widget from the list """
    self._updated = True
    self._items.remove(widget)
    self._sizes.pop(widget, None)
    self._list_updated = True

  def item(self, index):
    """ Return a specific item """
    if 0 <= index < len(self._items):
      return self._items[index]
    return None

  def change(self, forward=True):
    """ Manually trigger next event """
    self._updated = True

    # Update the index marker
    move_left = False
    move_right = False
    if forward:
      if self.index == self._display_end:
        move_right = True
      self.index += 1
      if self.index >= len(self._items):
        self.index = 0
    else:
      if self.index == self.display_start:
        move_left = True
      self.index -= 1
      if self.index < 0:
        self.index = len(self._items) - 1

    # Correct for sub-display set:
    if 0 < self.display_count < len(self._items):
      if move_left:
        self.display_start = self.index
      if move_right:
        self.display_start = self.index - self.display_count + 1
        if self.display_start < 0:
          self.display_start += len(self._items)

    if not self.index in self._display:
      self._list_updated = True
    self.selected = self._data[self._items[self.index]][2]
    if self.on_change != "":
      events.trigger(self.on_change, self)

  def _register(self, window):
    window.push_handlers(self)

  def _rebuild(self):
    if not self._next is self.next:
      events.remove(self._on_next_event)
      if not self.next is None:
        events.listen(self.next.on_click, self._on_next_event)
        self._next = self.next
    if not self._prev is self.prev:
      events.remove(self._on_prev_event)
      if not self.prev is None:
        events.listen(self.prev.on_click, self._on_prev_event)
        self._prev = self.prev
    if not self._list is self.list:
      self._list = self.list
      self._list_updated = True
    if self._disabled != self.disabled:
      self._disabled = self.disabled
      self.list.disabled = self.disabled
      self.next.disabled = self.disabled
      self.prev.disabled = self.disabled
      self.marker.disabled = self.disabled
    if self._list_updated:
      self._rebuild_list()
    self._elements = [self.next, self.prev, self.list, self.marker]
    self.next.disabled = False
    if self.list.any():
      selected = self._items[self.index]
      if not selected is None and not self.marker is None:
        self._list.draw()
        self.marker.bounds(selected.xmin, selected.ymin, selected.xmax, selected.ymax)

  def _rebuild_list(self):
    """ Rebuild the content of the list """
    self._display = []
    self.list.clear()
    if 0 < self.display_count < len(self._items):
      count = 0
      offset = self.display_start
      while count < self.display_count:
        self.__rebuild_list_item(self._items[offset])
        self._display_end = offset
        offset += 1
        count += 1
        if offset >= len(self._items):
          offset = 0
    else:
      for i in range(len(self._items)):
        self.__rebuild_list_item(self._items[i])
        self._display_end = i

  def __rebuild_list_item(self, i):
    self.list.add(i, self._data[i][0], self._data[i][1])
    self._display.append(i)


class Partial(Widget):
  """ Displays part of one image and part of another.
      
      The primary texture is displayed when amount = 1.0,
      and hidden when amount is 0.0.

      The cross fade is horizontal or vertical as appropriate
      given the provided "anchor" and the windowing moves toward
      that edge linearly.
      
      eg. anchor = TOP, x = primary, . = secondary, amount = 0.8

      x x x x x x x 
      x x x x x x x 
      x x x x x x x 
      x x x x x x x 
      x x x x x x x 
      x x x x x x x   <--- 80% is 'primary' from TOP
      x x x x x x x 
      x x x x x x x 
      . . . . . . .   <--- 20% is 'secondary'
      . . . . . . . 

      Use this for health bars, and stuff, not Select.

      Notice that the primary is rendered OVER the secondary, 
      so for example, you can do a diablo style health orb;
      the secondary ('under') texture is always rendered 100%.

      If no 'under' texture is provided, no underlay is rendered
      and the secondary section will be blank.
  """

  def __init__(
    self, 
    texture="", 
    texture_under="", 
    uv=[0, 0, 1, 0, 1, 1, 0, 1], 
    uv_under=[0, 0, 1, 0, 1, 1, 0, 1],
    anchor=align.TOP,
    value=1.0,
    panel=False,
  ):
    super(Partial, self).__init__()
    self.texture = texture              # The top texture 
    self.texture_under = texture_under  # The bottom texture
    self.uv = uv                        # UV coordinates for the top texture
    self.uv_under = uv_under            # UV coordinates for the bottom texture
    self.anchor = anchor                # The edge anchor 
    self.value = value                  # 0 -> 1 range of how much of the texture to display
    self.panel = panel                  # If true, ignore uv and uv_under and tread texture as panels
    self.__under = None
    self.__over = None

  def _rebuild(self):
    """ Display rebuild """

    # Build under if one exists or has changed
    if self.texture_under != "":
      if self.__under is None or self.__under.texture != self.texture_under or (not self.panel and self.__under.uv != self.uv_under):
        if self.panel:
          self.__under = Panel(self.texture_under)
        else:
          self.__under = Image(texture=self.texture_under, uv=self.uv_under)
        self.__under.bounds(self.xmin, self.ymin, self.xmax, self.ymax)
        self._elements.append(self.__under)

    # Build over if changed
    if self.__over is None or self.__over.texture != self.texture or (not self.panel and self.__over.uv != self.uv):
      if self.panel:
        self.__over = Panel(self.texture)
      else:
        self.__over = Image(texture=self.texture, uv=self.uv)

    # Reflow display bounds on over
    bounds = [self.xmin, self.ymin, self.xmax, self.ymax]
    bounds = self._aligned_bounds(bounds)
    self.__over.bounds(bounds[0], bounds[1], bounds[2], bounds[3])
    if not self.panel:
      self.__over.uv = self._aligned_uv(self.uv)

    # Rebuild elements array either way
    self._elements = [self.__over]
    if not self.__under is None:
      self._elements.insert(0, self.__under)

  def _aligned_uv(self, raw):
    """ Return an xmin, ymin, xmax, ymin based on anchor and value """
    b = self._aligned_bounds([raw[0], raw[1], raw[4], raw[5]])
    uv = [b[0], b[1], b[2], b[1], b[2], b[3], b[0], b[3]]
    return uv

  def _aligned_bounds(self, bounds):
    """ Return an xmin, ymin, xmax, ymin based on anchor and value """
    if self.anchor == align.LEFT:
      bounds[2] = bounds[0] + self.value * (bounds[2] - bounds[0])
    elif self.anchor == align.RIGHT:
      bounds[0] = bounds[2] - self.value * (bounds[2] - bounds[0])
    if self.anchor == align.BOTTOM:
      bounds[3] = bounds[1] + self.value * (bounds[3] - bounds[1])
    elif self.anchor == align.TOP:
      bounds[1] = bounds[3] - self.value * (bounds[3] - bounds[1])
    return bounds


class Dialog(Widget):
  """ Display arbitrary content in a popup dialog 
      
      The layouts of the items in the dialog are 
      defined by the bounds of the dialog.

      Note that this dialog is always closable, 
      and is not mobile. To have an 'accept' or 
      'accept / reject' dialog, use the content
      and customize it manually.

      Functionally this acts as a list, similar to
      VList or HList.

      Dialog is only widget that universally locks
      events and prevent other objects from receiving
      them.

      Until the dialog widget is closed, only widgets
      that are child elements of the dialog may receive
      events.
  """
  pass
