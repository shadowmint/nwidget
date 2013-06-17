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


class Marker(object):
  """ The 'dot' for the snake to eat and make itself longer """

  def __init__(self, assets):
    path = assets.resolve("assets", "point.png")
    raw = pyglet.image.load(path)
    seq = pyglet.image.ImageGrid(raw, 4, 4)
    anim = pyglet.image.Animation.from_image_sequence(seq, 0.05, True)
    self.node = cocos.sprite.Sprite(anim)
