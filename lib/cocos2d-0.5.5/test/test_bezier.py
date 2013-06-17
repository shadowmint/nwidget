# This code is so you can run the samples without installing the package
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
#

testinfo = "s, t 1.5, s, t 3.5, s, t 5.1, s, q"
tags = "Bezier"

import cocos
from cocos.director import director
from cocos.actions import Bezier
from cocos.sprite import Sprite
import pyglet

from bezier import path

class TestLayer(cocos.layer.Layer):
    def __init__(self):
        super( TestLayer, self ).__init__()

        x,y = director.get_window_size()

        self.sprite = Sprite('grossini.png', (x/4, y/4) )
        self.add( self.sprite )
        self.sprite.do( Bezier( path, 5 ) )

def main():
    director.init()
    test_layer = TestLayer ()
    main_scene = cocos.scene.Scene (test_layer)
    director.run (main_scene)

if __name__ == '__main__':
    main()
