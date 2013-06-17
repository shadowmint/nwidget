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
import cocos
from .layout import Layout


class CocosLayer(cocos.cocosnode.CocosNode):
  """ Simple helper class to use nwidget with cocos2d.

      Use it like this:

        class LayoutUi(CocosLayer):

          def event(self, code, widget):
            print("Event!")

          def __init__(self):
            a = nwidget.Assets()
            super(LayoutUi, self).__init__(
              nwidget.theme.Gothic, 
              a.resolve("..", "..", "theme", "gothic"),
              a.resolve("ui", "sample.py"),
              a.resolve("ui")
            )

            self.model = {"a":"b"}

            nwidget.listen("MAIN_BUTTON_CLICK", self.event)

      You can then use this as a standard cocos2d layer, 
      and insert it into a scene:

        layout = LayoutUi()
        main_scene = cocos.scene.Scene (hello_layer, direct, layout)
        cocos.director.director.run (main_scene)

      Be aware that this is a *pyglet* ui, not a natively cocos2d
      one, and as such, scene transformations are not taken into 
      account when processing ui input.

      Use scene transformations to transition between ui's; but to
      accurately track input a full-screen scene must be used.
  """

  def __init__(self, theme, theme_path, layout, layout_path):
    super(CocosLayer, self).__init__()
    window = cocos.director.director.window
    theme = theme(theme_path, window)
    self.layout = Layout(window, theme, layout_path, layout)
    self.model = {}

  def draw(self):
    self.layout.model = self.model
    self.layout.draw()


class CocosWidget(cocos.cocosnode.CocosNode):
  """ Simple cocos widget container """

  def __init__(self, widgets=None):
    super(CocosWidget, self).__init__()
    if widgets is None:
      self.widgets = []
    else:
      self.widgets = widgets

  def draw(self):
    for i in self.widgets:
      i.draw()
