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

import pyglet
import cocos
import model
import nwidget

class CreditsView(cocos.layer.Layer):
  """ Testing class """

  def __init__(self, assets):
    super(CreditsView, self).__init__()

    # Clear events from other views
    nwidget.events.clear(cocos.director.director.window)
    self.is_event_handler = True

    self.ui = model.Ui("credits.py", {})
    self.add(self.ui)

    # Background
    bg = model.Background(assets)
    self.add(bg.node)

    nwidget.listen("CREDITS_MENU", model.Game.menu)
