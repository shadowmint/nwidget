try:
  import bootstrap
except:
  pass
import pyglet
import cocos
import nwidget
from nwidget.cocos2d import CocosLayer


class DirectUi(cocos.cocosnode.CocosNode):
  """ nwidget direct ui """

  def __init__(self):
    super(DirectUi, self).__init__()
    self.block = nwidget.Block(color=(255, 0, 0, 255))
    self.block.bounds(10, 10, 100, 100)

  def draw(self):
    self.block.draw()


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


class Hello(cocos.layer.Layer):
  """ Typical cocos2d layer """

  def __init__(self):
    super( Hello, self ).__init__()

    sprite = cocos.sprite.Sprite("data/cat.jpg")
    sprite.position = 150, 150
    self.add(sprite)

    # Load image, convert to sequence of images for animation, create sprite animation.
    raw = pyglet.image.load('data/cat.jpg')
    raw_seq = pyglet.image.ImageGrid(raw, 5, 5)
    anim = pyglet.image.Animation.from_image_sequence(raw_seq, 0.05, True)
    sprite2 = cocos.sprite.Sprite(anim)
    sprite2.position = 300, 300
    self.add(sprite2)
 
 
def quit(self):
  exit()

if __name__ == "__main__":
  cocos.director.director.init()
  hello_layer = Hello ()
  direct = DirectUi()
  layout = LayoutUi()
  main_scene = cocos.scene.Scene (hello_layer, direct, layout)
  pyglet.clock.schedule_interval(quit, 5)
  cocos.director.director.run (main_scene)
