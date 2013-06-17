import nwidget
from nwidget.layout import *

class MenuUi(LayoutBase):

  def __init__(self):
    super(MenuUi, self).__init__()

  def widgets(self, helper):
    """ Create widgets """

    helper.scope(globals())

    # Header
    # Notice how this uses assets *inside* the ui folder for ui things.
    widget(nwidget.Image(),
      width = (50, MM),
      height = (20, MM),
      x = (CENTER.X, 0, MM),
      y = (CENTER.Y, 35, MM),
      texture = assets.resolve("assets", "title.png"),
      uv = (0, 0.6, 1, 0.6, 1, 1, 0, 1),
    )

    # Menu
    menu = widget(
      nwidget.VList(),
      width = (40, MM),
      height = (50, MM),
      x = (CENTER.X, 0, MM),
      y = (CENTER.Y, -5, MM),
      padding = 20
    )

    menu.add(widget(theme.button(), keep=False, text="Exit", on_click="MENU_EXIT"))
    menu.add(widget(theme.button(), keep=False, text="Credits", on_click="MENU_CREDITS"))
    menu.add(widget(theme.button(), keep=False, text="Play game", on_click="MENU_PLAY_GAME"))

  def sync(self, data):
    pass

# Instance
layout = MenuUi()
