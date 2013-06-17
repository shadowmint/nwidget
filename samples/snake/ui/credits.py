from nwidget.layout import *
import nwidget

class CreditsUi(LayoutBase):

  def __init__(self):
    super(CreditsUi, self).__init__()

  def widgets(self, helper):
    """ Create widgets """

    helper.scope(globals())

    # Header
    widget(theme.header(),
      width  = (40, MM),
      height = (30, MM),
      x      = (CENTER.X, 0, MM),
      y      = (TOP, -15, MM),
      text   = "Credits!",
      size   = 30,
      align  = nwidget.align.CENTER,
    )

    # Credits~
    path = assets.resolve("assets/credits.txt")
    with open(path, "r") as fp:
      text = fp.read()

    widget(theme.text(),
      left   = (LEFT, 20, MM),
      right  = (RIGHT, -20, MM),
      top    = (TOP, -30, MM),
      bottom = (BOTTOM, -20, MM),
      text = text,
      align = nwidget.align.CENTER,
    )

    # Go back~
    widget(theme.button(),
      width    = (40, MM),
      height   = (14, MM),
      x        = (CENTER.X, 0, MM),
      y        = (BOTTOM, 20, MM),
      text     = "Back",
      on_click = "CREDITS_MENU"
    )

  def sync(self, data):
    pass

# Instance
layout = CreditsUi()
