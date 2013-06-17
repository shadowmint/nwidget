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
from .enum import enum
import platform as _p

# Set of alignment constants
align = enum(
  "LEFT",
  "RIGHT",
  "CENTER",
  "TOP",
  "BOTTOM",
)

# Various supported unit types
units = enum(
  "PX",
  "MM",
  "INCH",
  "PERCENT"
)

# Axis consts
axis = enum("X", "Y")

# Button state constants
widget = enum(
  "NORMAL",
  "OVER",
  "DOWN",
  "DISABLED"
)

# Platforms
platforms = enum(
  "WINDOWS",
  "MAC",
  "LINUX"
)

# Current platform
if _p.system() == "Windows":
  platform = platforms.WINDOWS
elif _p.system() == "Linux":
  platform = platforms.LINUX
elif _p.system() == "Darwin":
  platform = platforms.MAC

# Figure out the display dpi; too bad pyglet doesn't support this
# We're really just guessing here; TODO: Make this work better
dpi = 72
if platform == platforms.MAC:
  dpi = 96

# Calculate dpmm
dpmm = dpi / 25.4

