# This code is so you can run the samples without installing the package
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
#

testinfo = "s, t 0.3, s, t 0.6, s, t 1, s, q"
tags = "skeleton, BitmapSkin, Animate"

import cPickle

import cocos
from cocos.director import director
from cocos.sprite import Sprite
from cocos import skeleton
import pyglet

import sample_skeleton
import sample_skin


class TestLayer(cocos.layer.Layer):
    def __init__(self):
        super( TestLayer, self ).__init__()

        x,y = director.get_window_size()
        self.skin = skeleton.BitmapSkin(sample_skeleton.skeleton,
                                        sample_skin.skin)
        self.add( self.skin )
        x, y = director.get_window_size()
        self.skin.position = x/2, y/2
        anim = cPickle.load(open("SAMPLE.anim"))
        self.skin.do( cocos.actions.Repeat( skeleton.Animate(anim) ) )

def main():
    director.init()
    test_layer = TestLayer()
    bg_layer = cocos.layer.ColorLayer(255,255,255,255)
    main_scene = cocos.scene.Scene()
    main_scene.add(bg_layer, z=-10)
    main_scene.add(test_layer, z=10)
    director.run(main_scene)

if __name__ == '__main__':
    main()
