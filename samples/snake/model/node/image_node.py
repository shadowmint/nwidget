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


class ImageNode(cocos.cocosnode.CocosNode):
  """ Cocos2D has no native support for large backgrounds~ """

  def __init__(self, texture=None, uv=[0, 0, 1, 0, 1, 1, 0, 1], width=0, height=0):
    super(ImageNode, self).__init__()
    self.texture = texture
    self.uv = uv
    self.width = width
    self.height = height
    self.dont_anchor = False

  def draw(self):
    if not self.texture is None:

      # Apply scale manually...
      width = self.width * self.scale
      height = self.height * self.scale

      if self.dont_anchor:
        xmin = self.x
        ymin = self.y
        xmax = self.x + width
        ymax = self.y + height
      else:
        xmin = self.x - width / 2
        ymin = self.y - height / 2
        xmax = self.x + width / 2
        ymax = self.y + height / 2

      texture = self.texture.get_texture()
      pyglet.gl.glEnable(texture.target)
      pyglet.gl.glBindTexture(texture.target, texture.id)
      pyglet.graphics.draw_indexed(4, pyglet.gl.GL_TRIANGLES,
        [0, 1, 2, 0, 2, 3], (
          'v2i', (
            int(math.floor(xmin)), int(math.floor(ymin)),
            int(math.floor(xmax)), int(math.floor(ymin)),
            int(math.floor(xmax)), int(math.floor(ymax)),
            int(math.floor(xmin)), int(math.floor(ymax)),
          )
        ), ('t2f', self.uv)
      )
      pyglet.gl.glDisable(texture.target)
