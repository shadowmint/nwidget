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


def enum(*sequential, **named):
  """ Enum helper to generate integer values 
      usage: ENUM_TYPE = enum(VALUE, VALUE2, VALUE3)
      
      The result will be VALUE = 1, VALUE2 = 2, etc.
  """
  enums = dict(zip(sequential, range(len(sequential))), **named) 
  return type('Enum', (), enums)


def bitflags(*sequential, **named):
  """ Enum helper to generate bit-flag values 
      usage: ENUM_TYPE = bitflags(VALUE, VALUE2, VALUE3)
      
      The result will be VALUE = 0x1, VALUE2 = 0x2, VALUE3 = 0x4, etc.
  """
  values = []
  base = 1
  for _ in range(len(sequential)):
    values.append(base)
    base *= 2
  enums = dict(zip(sequential, values), **named) 
  return type('Enum', (), enums)


def register(items, globals):
  """ Register an enumeration as inside the current global scope
      usage: TYPE = enum(V1, V2, V3)
             register(TYPE)
             x = V1
  """
  for name in items.keys():
      globals[name] = items[name]