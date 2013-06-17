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
import pyglet
import nwidget
import model.node


class Snake(object):
  """ The snake """

  def __uv(self, xmin, ymin, xmax, ymax):
    return (xmin, ymin, xmax, ymin, xmax, ymax, xmin, ymax)

  def __init__(self, assets):
    path = assets.resolve("assets", "snake.png")
    texture = pyglet.image.load(path)
    self.node = model.node.StateNode()
    self.node.add_state("UP", model.node.ImageNode(texture=texture, uv=self.__uv(0, 0, 0.5, 0.5), width=64, height=64))
    self.node.add_state("LEFT", model.node.ImageNode(texture=texture, uv=self.__uv(0, 0.5, 0.5, 1), width=64, height=64))
    self.node.add_state("DOWN", model.node.ImageNode(texture=texture, uv=self.__uv(0.5, 0, 1, 0.5), width=64, height=64))
    self.node.add_state("RIGHT", model.node.ImageNode(texture=texture, uv=self.__uv(0.5, 0.5, 1, 1), width=64, height=64))
    self.node.state = "UP"
    self.node.scale = 0.5
    self.x = 0
    self.y = 0

  def up(self):
    self.node.state = "UP"

  def left(self):
    self.node.state = "LEFT"

  def right(self):
    self.node.state = "RIGHT"

  def down(self):
    self.node.state = "DOWN"

  def jump(self, x, y):
    self.x = x
    self.y = y
    self.node.position = (x, y)

  def move(self, distance, align):
    dx = 0
    dy = 0
    if align == "RIGHT":
      dx = distance
    elif align == "LEFT":
      dx = -distance
    elif align == "UP":
      dy = distance
    elif align == "DOWN":
      dy = -distance
    self.x += dx
    self.y += dy
    self.node.position = (self.x, self.y)
    return (dx, dy)
