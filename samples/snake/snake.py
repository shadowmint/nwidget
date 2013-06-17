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

import sys


# Check for options
opt_testing = len(sys.argv) == 2 and sys.argv[1] == "--test"
opt_help = not opt_testing and len(sys.argv) != 1

# Run game
if __name__ == "__main__":
  if opt_help:
    print("To run normally: python snake.py")
    print("   To run tests: python snake.py --test")
  else:
    import bootstrap
    import cocos
    import model
    cocos.director.director.init(width=400, height=400)
    app = model.Game()
    app.run(testing=opt_testing)
