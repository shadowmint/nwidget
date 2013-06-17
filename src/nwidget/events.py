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
from .log import error
import inspect

class Events():
  """ Global events list handle """
  
  @staticmethod
  def reset(window):
    Events.__listeners = {}
    def dummy(*kargs, **kwargs):
      pass
    window.set_handler("on_mouse_motion", dummy)
    window.set_handler("on_mouse_press", dummy)
    window.set_handler("on_mouse_release", dummy)
    window.set_handler("on_text", dummy)
    window.set_handler("on_text_motion", dummy)
    window.set_handler("on_text_motion_select", dummy)
    window.set_handler("on_mouse_scroll", dummy)
    window.set_handler("on_mouse_drag", dummy)
    window.set_handler("on_activate", dummy)
    window.set_handler("on_deactivate", dummy)
    
  @staticmethod
  def listeners():
    try:
      _ = Events.__listeners
    except AttributeError:
      Events.__listeners = {}
    return Events.__listeners


class Listener():
  """ A single event listener """
  
  def __init__(self, code, callback):
    self.code = code
    self.callback = callback
    spec = inspect.getargspec(self.callback)
    self.args = len(spec.args)
    self.bb = spec
    if len(spec.args) > 0 and spec.args[0] == "self":
      self.args -= 1
    if not (0 <= self.args <= 2):
      raise InvalidCallbackException("The method passed did not match the required signature")
    
  def invoke(self, src):
    """ Invoke the callback """
    try:
      if self.args == 2:
        self.callback(self.code, src)
      elif self.args == 1:
        self.callback(src)
      else:
        self.callback()
    except Exception, e:
      error("Failed to invoke event callback for code '%s'" % self.code, e)


class InvalidCallbackException(Exception):
  pass


def listen(code, callback):
  """ Sets callback(code, caller) to be run when an event is triggered.
  
      nwidget treats all events equally, and all of them are triggered
      using event codes. This is typically done by setting the code
      on a widget, eg:
      
      my_button.on_click = "BUTTON_ID"
      
      You can then bind an event listener using:
      
      def callback(code, widget):
        pass
      nwidget.listen("BUTTON_ID", callback)
      
      This may seem strange given that most UI frameworks directly attach
      callbacks to their objects, like this:
      
      widget_blah.on_click = callback
      
      However, this is not appropriate for event binding via configuration
      files, where the callback must then be dynamically created. For more
      details on how this is used, see the layout module.

      NB. invoke looks at the function arguments and either calls
      callback(c, w), or callback(w) or callback() depending. So technically 
      any of these are valid; including callback(self, ...)
  """
  listeners = Events.listeners()
  try:
    items = listeners[code]
  except KeyError:
    listeners[code] = []
    items = listeners[code]
  listener = Listener(code, callback)
  items.append(listener)

  
def trigger(code, src):
  """ Trigger an event, from anywhere """
  listeners = Events.listeners()
  items = []
  try:
    items = listeners[code]
  except KeyError:
    pass
  print("For k(%s) results were: %r" % (code, items))
  for i in items:
    i.invoke(src)


def reset(window):
  """ Remove all listeners """
  Events.reset(window)


def clear(code):
  """ Remove all listeners for the given code """
  listeners = Events.listeners()
  listeners[code] = []


def remove(callback):
  """ Remove a single event listener from every where """
  listeners = Events.listeners()
  for k in listeners.keys():
    s = listeners[k]
    if callback in s:
      sn = []
      for i in s:
        if not i is callback:
          sn.append(i)
      listeners[k] = sn
