# This code is so you can run the samples without installing the package
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
#

testinfo = "s, t 0.5, s, t 1, s, t 1.5, s, t 2, s, t 2.5, s, q"
tags = "Repeat"

import cocos
from cocos.director import director
from cocos.actions import Repeat, Rotate, MoveBy, Place
from cocos.sprite import Sprite
import pyglet

class TestLayer(cocos.layer.Layer):
    def __init__(self):
        super( TestLayer, self ).__init__()

        x,y = director.get_window_size()

        self.sprite = Sprite( 'grossini.png', (x/2, y/2) )
        self.add( self.sprite )
        move = MoveBy((100,0), 1)
        rot = Rotate(360, 1)
        seq = Place((x/4,y/2)) + rot + move
        self.sprite.do( Repeat ( seq ) )

def main():
    director.init()
    test_layer = TestLayer ()
    main_scene = cocos.scene.Scene (test_layer)
    director.run (main_scene)

if __name__ == '__main__':
    main()
