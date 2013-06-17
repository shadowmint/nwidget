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
import random
import model
import math


# Game control constants
SNAKE_SPEED = 5
GROW_RATE = 25
MARKER_EAT_DIST = 10
MARKER_SCORE = 10000


class GameView(cocos.layer.Layer):
  """ Testing class """

  def __init__(self, assets):
    super(GameView, self).__init__()
    self.assets = nwidget.Assets()
    self.load_objects()
    pyglet.clock.schedule_interval(self.update, 0.03)

  def load_objects(self):

    assets = self.assets

    # Clear events from other views
    nwidget.events.clear(cocos.director.director.window)
    self.is_event_handler = True

    # View model & ui
    self.model = {
      "score" : 0,
      "dead" : False,
      "updated" : False,
      "play_time" : 0,
    }
    self.ui = model.Ui("game.py", self.model)
    self.add(self.ui, z=1) # Above the background

    # bind events
    nwidget.listen("GAME_RESTART", self.on_restart)
    nwidget.listen("GAME_GOTO_MENU", self.on_menu)

    # Background
    bg = model.Background(assets)
    self.add(bg.node)

    # Add path and snake
    self.snake = model.Snake(assets)
    self.path = model.Path()
    width, height = cocos.director.director.get_window_size()
    x = width / 2
    y = height / 2
    self.snake.jump(x, y)
    self.path.jump(x, y)
    self.add(self.snake.node)
    self.add(self.path)
    self.bounds = (0, 0, width, height)

    # Direction
    self.snake.right()
    self.vector = "RIGHT"
    self.speed = SNAKE_SPEED

    # Are we paused because we died?
    self.dead = False

    # Start~
    self.marker = None
    self.inc_dt = 0
    self.generate_marker()

  def update(self, dt):
    if not self.dead:

      # Update timer
      self.inc_dt += dt
      if self.inc_dt > 1:
        self.inc_dt = 0
        self.model["play_time"] += 1
        self.model["updated"] = True

      motion = self.snake.move(self.speed, self.vector)
      self.path.move(*motion)
      if self.check_snake_dies():
        self.on_died()
      if self.check_snake_eats_marker():
        self.on_marker()
        self.generate_marker()
        self.model["score"] += random.randint(MARKER_SCORE, MARKER_SCORE * 10)
        self.model["updated"] = True

  def check_snake_dies(self):
    if self.snake.x < self.bounds[0]:
      return True
    elif self.snake.y < self.bounds[1]:
      return True
    elif self.snake.x > self.bounds[2]:
      return True
    elif self.snake.y > self.bounds[3]:
      return True
    elif self.path.intersects():
      return True
    return False

  def check_snake_eats_marker(self):
    dx = self.snake.x - self.marker.node.position[0]
    dy = self.snake.y - self.marker.node.position[1]
    d = math.sqrt(dx*dx + dy*dy)
    if d < MARKER_EAT_DIST:
      return True
    return False

  def generate_marker(self):
    if self.marker is None:
      self.marker = model.Marker(self.assets)
      self.marker.node.scale = 0.4
      self.marker.node.position = (
        random.randint(self.bounds[0] + 40, self.bounds[2] - 40),
        random.randint(self.bounds[1] + 40, self.bounds[3] - 40)
      )
      self.add(self.marker.node)

  def on_restart(self, code, widget):
    self.model["score"] = 0
    self.model["dead"] = False
    self.model["updated"] = True
    self.model["play_time"] = 0

    width, height = cocos.director.director.get_window_size()
    x = width / 2
    y = height / 2

    self.path.reset()
    self.snake.jump(x, y)
    self.path.jump(x, y)

    # Direction
    self.snake.right()
    self.vector = "RIGHT"
    self.speed = SNAKE_SPEED

    # Are we paused because we died?
    self.dead = False

    # Start~
    self.inc_dt = 0
    self.generate_marker()

  def on_menu(self, code, widget):
    model.Game.menu()

  def on_marker(self):
    self.path.length += GROW_RATE
    self.remove(self.marker.node)
    self.marker = None
    self.model["score"] += 100

  def on_died(self):
    self.dead = True
    self.model["dead"] = True # Toggles ui state!
    self.model["updated"] = True # Toggles ui state!

  def on_left(self):
    if self.vector != "RIGHT":
      self.vector = "LEFT"
      self.snake.left()

  def on_right(self):
    if self.vector != "LEFT":
      self.vector = "RIGHT"
      self.snake.right()

  def on_up(self):
    if self.vector != "DOWN":
      self.vector = "UP"
      self.snake.up()

  def on_down(self):
    if self.vector != "UP":
      self.vector = "DOWN"
      self.snake.down()

  def on_key_press(self, key, modifiers):
    if key == pyglet.window.key.UP:
      self.on_up()
    elif key == pyglet.window.key.DOWN:
      self.on_down()
    elif key == pyglet.window.key.LEFT:
      self.on_left()
    elif key == pyglet.window.key.RIGHT:
      self.on_right()
