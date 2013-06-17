# This code is so you can run the samples without installing the package
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
#

testinfo = "s, t 2, s, t 5.1, s, t 5.2, s, q"
tags = "sequence, MoveBy, Place"

import cocos
from cocos.director import director
from cocos.actions import Place, MoveBy
from cocos.sprite import Sprite


import pyglet

class TestLayer(cocos.layer.Layer):
    def __init__(self):
        super( TestLayer, self ).__init__()

        x,y = director.get_window_size()

        self.sprite = Sprite( 'grossini.png', (x,y/2)  )
        self.add( self.sprite )
        self.sprite.do( Place( (0, y/2) ) + MoveBy( (x/2, 0) ) )

def main():
    director.init()
    test_layer = TestLayer ()
    main_scene = cocos.scene.Scene (test_layer)
    director.run (main_scene)

if __name__ == '__main__':
    main()
