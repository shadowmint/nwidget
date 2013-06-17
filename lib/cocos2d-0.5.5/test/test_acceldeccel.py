# This code is so you can run the samples without installing the package
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
#

testinfo = "s, t 2.0, s, t 4.1, s, q"
tags = "AccelDeccel"

import cocos
from cocos.director import director
from cocos.actions import AccelDeccel, MoveBy, Reverse, Repeat
from cocos.sprite import Sprite
import pyglet

class TestLayer(cocos.layer.Layer):
    def __init__(self):
        super( TestLayer, self ).__init__()

        x,y = director.get_window_size()

        self.sprite = Sprite('grossini.png', (0, y/2) )
        self.add( self.sprite  )
        mov = AccelDeccel( MoveBy( (x, 0 ), 4 ) )
        self.sprite.do( Repeat( mov + Reverse(mov) ))

def main():
    director.init()
    test_layer = TestLayer ()
    main_scene = cocos.scene.Scene (test_layer)
    director.run (main_scene)

if __name__ == '__main__':
    main()
