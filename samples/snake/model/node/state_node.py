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


class StateNode(cocos.cocosnode.CocosNode):
  """ Cocos2D has no native support for state based animation. """

  def __init__(self):
    super(StateNode, self).__init__()
    self.state = None
    self.__last_state = None
    self.__states = {}

  def add_state(self, key, node):
    self.__states[key] = node

  def draw(self):
    if not self.state is None:
      state = self.__states[self.state]
      if self.state != self.__last_state:
        self.__last_state = self.state
      state.position = self.position
      state.scale = self.scale
      state.draw()
