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
import math


class Path(cocos.cocosnode.CocosNode):
  """ Draws a path that the snake has walked over """

  def __init__(self):
    super(Path, self).__init__()
    self.reset()

  def reset(self):
    self.__points = []
    self.color = (120, 120, 120, 64)
    self.x = 0
    self.y = 0
    self.width = 4
    self.length = 0
    self._total_length = 0

  def jump(self, x=0, y=0):
    self.x = x
    self.y = y

  def move(self, x=0, y=0):
    """ Move the marker a particular distance """

    # Skip stupid moves
    if x == 0 and y == 0:
      return

    # Add a new marker (which may move the most recent marker)
    if len(self.__points) == 0:
      self.add(self.x, self.y)
    p = self.__points[len(self.__points) - 1]
    self.x = p[0] + x
    self.y = p[1] + y
    self.add(self.x, self.y)

    # Calculate total length
    if self._total_length > self.length:
      self.prune()

  def prune(self):
    bad_size = self._total_length - self.length
    while bad_size > 0:
      if len(self.__points) < 2:
        return
      dx = self.__points[1][0] - self.__points[0][0]
      dy = self.__points[1][1] - self.__points[0][1]
      dist = math.fabs(dx + dy) # 2d only, yay~
      if bad_size > dist:
        self.__points.pop(0)
        bad_size -= dist
      else:
        if dx > 0:
          self.__points[0][0] += bad_size
        elif dx < 0:
          self.__points[0][0] -= bad_size
        elif dy > 0:
          self.__points[0][1] += bad_size
        elif dy < 0:
          self.__points[0][1] -= bad_size
        bad_size = 0

  def add(self, x, y):
    if len(self.__points) < 2:
      self.__points.append([x, y])
    else:
      p1 = self.__points[len(self.__points) - 1]
      p2 = self.__points[len(self.__points) - 2]
      dx = p1[0] - p2[0]
      dy = p1[1] - p2[1]
      ddx = p1[0] - x
      ddy = p1[1] - y
      if (dx == 0 and ddx == 0) or (dy == 0 and ddy == 0):
        if ddy < 0 and dy > 0:
          p1[1] = y
        elif ddy > 0 and dy < 0:
          p1[1] = y
        if ddx < 0 and dx > 0:
          p1[0] = x
        elif ddx > 0 and dx < 0:
          p1[0] = x
      else:
        self.__points.append([x, y])

  def intersects(self):
    """ Check if the snake overlaps itself """
    match = False
    for i in range(len(self.__points) - 1):
      p1 = self.__points[i]
      p2 = self.__points[i + 1]
      bounds = self.__line_segment(p1, p2)
      if not bounds is None:
        xmin = bounds[0]
        ymin = bounds[1]
        xmax = bounds[0]
        ymax = bounds[1]
        for j in range(len(bounds)):
          if not (j % 2):
            if bounds[j] < xmin:
              xmin = bounds[j]
            elif bounds[j] > xmax:
              xmax = bounds[j]
          else:
            if bounds[j] < ymin:
              ymin = bounds[j]
            elif bounds[j] > ymax:
              ymax = bounds[j]
        x = self.x
        y = self.y
        # TODO: Determine direction, and check two leading edge points; ie. last vector ----> then points are x+width,y+width x+width,y-width
        if x > xmin and x < xmax and y > ymin and y < ymax:
          match = True
          break
    return match

  def draw(self):
    """ Draw a line for the given path """
    if len(self.__points) >= 2:
      self._total_length = 0
      for i in range(len(self.__points) - 1):
        p1 = self.__points[i]
        p2 = self.__points[i + 1]
        coords = self.__line_segment(p1, p2)
        if not coords is None:
          pyglet.graphics.draw_indexed(4, pyglet.gl.GL_TRIANGLES,
            [0, 1, 2, 1, 2, 3],
            ('v2i', coords),
            ('c4b', self.color * 4)
          )
          coords = self.__line_cap(p2)
          pyglet.graphics.draw_indexed(4, pyglet.gl.GL_TRIANGLES,
            [0, 1, 2, 0, 2, 3],
            ('v2i', coords),
            ('c4b', self.color * 4)
          )

  def __line_cap(self, p1):
    rtn = [
      int(p1[0] + self.width),
      int(p1[1] + self.width),
      int(p1[0] + self.width),
      int(p1[1] - self.width),
      int(p1[0] - self.width),
      int(p1[1] - self.width),
      int(p1[0] - self.width),
      int(p1[1] + self.width),
    ]
    return rtn

  def __line_segment(self, p1, p2):
    vector = (p1[0] - p2[0], p1[1] - p2[1])
    length = math.sqrt(vector[0] * vector[0] + vector[1] * vector[1])
    if length == 0:
      return None
    self._total_length += length
    factor = 1.0 / length
    perp = (-vector[1], vector[0])
    perp = (perp[0] * factor, perp[1] * factor)
    rtn = [
      int(p1[0] + (perp[0] * self.width)),
      int(p1[1] + (perp[1] * self.width)),
      int(p1[0] - (perp[0] * self.width)),
      int(p1[1] - (perp[1] * self.width)),
      int(p2[0] + (perp[0] * self.width)),
      int(p2[1] + (perp[1] * self.width)),
      int(p2[0] - (perp[0] * self.width)),
      int(p2[1] - (perp[1] * self.width)),
    ]
    return rtn
