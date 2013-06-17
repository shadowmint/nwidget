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
import pyglet
import cocos
import nwidget
import views

class Game(object):

  def run(self, testing=False):
    assets = nwidget.Assets()
    if testing:
      layer = views.TestView(assets)
    else:
      layer = views.MainView(assets) 
    scene = cocos.scene.Scene(layer)
    cocos.director.director.run(scene)

  @staticmethod
  def menu():
    assets = nwidget.Assets()
    layer = views.MainView(assets)
    scene = cocos.scene.Scene(layer)
    cocos.director.director.run(scene)

  @staticmethod
  def play():
    assets = nwidget.Assets()
    layer = views.GameView(assets)
    scene = cocos.scene.Scene(layer)
    cocos.director.director.run(scene)

  @staticmethod
  def credits():
    assets = nwidget.Assets()
    layer = views.CreditsView(assets)
    scene = cocos.scene.Scene(layer)
    cocos.director.director.run(scene)

  @staticmethod
  def exit():
    exit(0)
