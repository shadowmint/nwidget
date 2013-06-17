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
import nwidget
import model
from nwidget.cocos2d import *


class TestView(cocos.layer.Layer):
  """ Testing class """

  def __init__(self, assets):
    super(TestView, self).__init__()
    self.assets = assets

    # Get events 
    nwidget.events.clear(cocos.director.director.window)
    self.is_event_handler = True

    # Ui layer
    ui = CocosWidget()
    self.add(ui, z=1)

    # Load background
    bg = model.Background(self.assets)
    self.add(bg.node)

    # Load marker
    marker = model.Marker(self.assets)
    marker.node.position = 50, 50
    marker.node.scale = 0.25
    self.add(marker.node)

    # Snake instructions
    ui.widgets.append(
      nwidget.Label(
        text="Press arrow keys to change snake sprite",
        size=13,
        color=(255, 255, 255, 255)
      ).bounds(20, 150, 600, 180)
    )

    # Load snake
    snake = model.Snake(self.assets)
    snake.node.position = 50, 100
    snake.node.scale = 0.5
    self.add(snake.node)
    self.snake = snake

    # Path instructions
    ui.widgets.append(
      nwidget.Label(
        text="Press arrow keys to move path in that direction\nL to increase length of path, R to reset path",
        size=13,
        color=(255, 255, 255, 255)
      ).bounds(20, 300, 600, 425)
    )

    # Load a path and draw it
    self.path = model.Path()
    self.reset_path()
    self.path.move(x=-50)
    self.path.move(y=-30)
    self.path.move(x=-100)
    self.path.move(y=-20)
    self.path.move(y=-20)
    self.add(self.path)

  def reset_path(self):
    self.path.reset()
    self.path.x = 100
    self.path.y = 200
    self.path.length = 150
    self.path.move(x=100)
    self.path.move(y=100)

  def check_path(self):
    if self.path.intersects():
      self.path.color = (127, 0, 0, 127)
    else:
      self.path.color = (127, 127, 127, 127)

  def on_key_press(self, key, modifiers):
    md = 5
    if key == pyglet.window.key.L:
      self.path.length += 5
    if key == pyglet.window.key.R:
      self.reset_path()
    elif key == pyglet.window.key.UP:
      self.snake.up()
      self.path.move(y=md)
    elif key == pyglet.window.key.DOWN:
      self.snake.down()
      self.path.move(y=-md)
    elif key == pyglet.window.key.LEFT:
      self.snake.left()
      self.path.move(x=-md)
    elif key == pyglet.window.key.RIGHT:
      self.snake.right()
      self.path.move(x=md)
    self.check_path()
