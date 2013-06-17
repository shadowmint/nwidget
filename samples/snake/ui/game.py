from nwidget.layout import *
import nwidget

class GameUi(LayoutBase):

  def __init__(self):
    super(GameUi, self).__init__()
    self.__ready = False

  def widgets(self, helper):
    """ Create widgets """

    helper.scope(globals())

    # Top panel

    self.score = widget(
      theme.text(),
      left   = (LEFT, 3, MM),
      right  = (RIGHT, 0, MM),
      top    = (TOP, 0, MM),
      bottom = (TOP, -8, MM),
      text   = "score: 0",
      valign = nwidget.align.CENTER
    )

    self.play_time = widget(
      theme.text(),
      left   = (LEFT, 0, MM),
      bottom = (TOP, -8, MM),
      right  = (RIGHT, -3, MM),
      top    = (TOP, 0, MM),
      text   = "play time: 0 seconds",
      valign = nwidget.align.CENTER,
      align  = nwidget.align.RIGHT
    )

    # 'You died' UI; hidden by default.
    deads_debug = True
    self.deads = []

    self.deads.append(
      widget(
        theme.panel(),
        left    = (CENTER.X, -30, MM),
        bottom  = (CENTER.Y, -31, MM),
        right   = (CENTER.X, 30, MM),
        top     = (CENTER.Y, 22, MM),
        visible = deads_debug
      )
    )

    self.deads.append(
      widget(theme.header(),
        left    = (CENTER.X, -26, MM),
        bottom  = (CENTER.Y, 0, MM),
        right   = (CENTER.X, 24, MM),
        top     = (CENTER.Y, 25, MM),
        color   = (195, 0, 0, 255),
        text    = "Your snake DIED!",
        align   = nwidget.align.CENTER,
        visible = deads_debug,
      )
    )

    self.final_score = widget(
      theme.text(),
      left    = (CENTER.X, -24, MM),
      bottom  = (CENTER.Y, -10, MM),
      right   = (CENTER.X, 23, MM),
      top     = (CENTER.Y, 5.5, MM),
      text    = "...but you did score 12323 points before it died",
      align   = nwidget.align.CENTER,
      visible = deads_debug,
    )
    self.deads.append(self.final_score)

    self.deads.append(
      widget(
        theme.button(),
        x        = (CENTER.X, 0, MM),
        y        = (CENTER.Y, -10, MM),
        width    = (40, MM),  # Sometime more convenient to do via width and height
        height   = (10, MM),
        text     = "Play again?",
        visible  = deads_debug,
        on_click = "GAME_RESTART",
      )
    )

    self.deads.append(
      widget(
        theme.button(),
        x        = (CENTER.X, 0, MM),
        y        = (CENTER.Y, -21, MM),
        width    = (40, MM),
        height   = (10, MM),
        text     = "Return to menu",
        visible  = deads_debug,
        on_click = "GAME_GOTO_MENU",
      )
    )

  def sync(self, data):
    """ Sync widget state to data elements
        Notice how we sync on reload using 'ready'
    """
    if data["updated"] or not self.__ready:
      self.score.text = "score: %d" % data["score"]
      self.final_score.text = "...but you did score %d points before it died" % data["score"]
      self.play_time.text = "play time: %d seconds" % data["play_time"]
      if data["dead"]:
        for i in self.deads:
          i.visible = True
      else:
        for i in self.deads:
          i.visible = False
      data["updated"] = False
      self.__ready = True

# Instance
layout = GameUi()
