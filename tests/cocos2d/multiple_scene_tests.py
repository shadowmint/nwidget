try:
  import bootstrap
except:
  pass
import sys
import os
import cocos
from cocos.director import director
from cocos.actions import *
from cocos.layer import *
from cocos.sprite import Sprite
import pyglet
import nwidget
from nwidget.cocos2d import CocosLayer


class TestLayer(cocos.layer.Layer):
    def __init__(self):
        super( TestLayer, self ).__init__()
        
        x,y = director.get_window_size()
        
        sprite1 = Sprite( 'data/grossini.png' )
        sprite2 = Sprite( 'data/grossinis_sister1.png' )
        sprite3 = Sprite( 'data/grossinis_sister2.png' )

        sprite1.position = (x/2, y/2 )
        sprite2.position = (x/4, y/2 )
        sprite3.position = (3*x/4.0, y/2 )

        self.add( sprite2 )
        self.add( sprite1 )
        self.add( sprite3 )

        sprite1.do( RotateBy( 360,1 ) * 16 )
        sprite2.do( RotateBy( -360,1 ) * 16 )
        sprite3.do( RotateBy( -360,1 ) * 16 )


class LayoutUi(CocosLayer):
  """ nwidget layout ui """

  def __init__(self):
    a = nwidget.Assets()
    super(LayoutUi, self).__init__(
      nwidget.theme.Gothic, 
      a.resolve("..", "..", "assets", "theme", "gothic"),
      a.resolve("ui", "sample.py"),
      a.resolve("ui")
    )

    # Model
    self.model = {"main_button_enabled": True, "updated": True, "main_text": "Try clicking me", "turn_off": False}

    # Events
    nwidget.listen("MAIN_BUTTON_CLICK", self.click_event)

    # Turn on debugging 
    # self.layout.watch()
    # self.layout.show_edges(True)
    # self.layout.show_bounds(True)

  def click_event(self, code, widget):
    print("Button clicked: " + str(code))


if __name__ == "__main__":
    director.init( resizable=True )
    main_scene = cocos.scene.Scene()
    main_scene.transform_anchor = (320,240)

    child1_scene = cocos.scene.Scene()
    child2_scene = cocos.scene.Scene()
    child3_scene = cocos.scene.Scene()
    child4_scene = cocos.scene.Scene()

    sprites = TestLayer()
    sprites.transform_anchor = 320,240

    child1_scene.add( ColorLayer( 0,0,255,255 ) )
    child1_scene.add( LayoutUi() )
    child1_scene.scale = 1.5
    child1_scene.position = (-160,-120)
    child1_scene.transform_anchor = (320,240)

    child2_scene.add( ColorLayer( 0,255,0,255) )
    child2_scene.add( sprites )
    child2_scene.scale = 1.5
    child2_scene.position = (160,120)
    child2_scene.transform_anchor = (320,240)

    child3_scene.add( ColorLayer( 255,0,0,255) )
    child3_scene.add( sprites )
    child3_scene.scale = 1.5
    child3_scene.position = (-160,120)
    child3_scene.transform_anchor = (320,240)

    child4_scene.add( ColorLayer( 255,255,255,255) )
    child4_scene.add( sprites )
    child4_scene.scale = 1.5
    child4_scene.position = (160,-120)
    child4_scene.transform_anchor = (320,240)

    main_scene.add( child1_scene )
    main_scene.add( child2_scene )
    main_scene.add( child3_scene )
    main_scene.add( child4_scene )

    rot = RotateBy(-360,2)
    rot2 = RotateBy(360,4)

    sleep = Delay(5)

    sleep2 = Delay(5)

    sc1 = ScaleTo(0.5, 0.5) + Delay(1.5)
    sc2 = Delay(0.5) + ScaleTo(0.5, 0.5) + Delay(1.0)
    sc3 = Delay(1.0) + ScaleTo(0.5, 0.5) + Delay(0.5)
    sc4 = Delay(1.5) + ScaleTo(0.5, 0.5)

    child1_scene.do( sc4 + sleep + rot + sleep + rot + rot  )
    child2_scene.do( sc3 + sleep + rot + sleep + rot + Reverse(rot) )
    child3_scene.do( sc2 + sleep + rot + sleep + rot + Reverse(rot) ) 
    child4_scene.do( sc1 + sleep + rot + sleep + rot + rot)

    main_scene.do( sleep + Reverse(rot) *2 + rot * 2 + sleep)

    sprites.do( Delay(4) + rot2 * 3 )

    def quit(self):
      exit()
    pyglet.clock.schedule_interval(quit, 10)
    director.run (main_scene)
