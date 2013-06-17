from nwidget.layout import *
import nwidget


# Widgets
class Sample2(LayoutBase):
  """ Example UI """

  def __init__(self):
    super(Sample2, self).__init__()

  def widgets(self, helper):
    """ Create widgets """

    helper.scope(globals())

    # Widgets
    widget(
      theme.button(),
      left =  (RIGHT, -40, MM),
      bottom = (TOP, -20, MM),
      right = RIGHT,
      top = TOP,
      on_click = "TURN_OFF_OWN_DEBUG",
      text = "Turn debug off on parent"
    )

    widget(
      theme.button(),
      left = LEFT,
      bottom = (TOP, -20, MM),
      right = (LEFT, 40, MM),
      top = TOP,
      on_click = "TURN_OFF_CHILD_DEBUG",
      text = "Turn debug on child off"
    )

    self.LAYOUT = widget(
      nwidget.Layout(window, theme, assets, assets.resolve("sample1.py")),
      left = (LEFT, 50, PX),
      bottom = (BOTTOM, 50, PX),
      right = (RIGHT, -50, PX),
      top = (TOP, -50, PX)
    )

    # Turn on debugging
    self.LAYOUT.watch()
    self.LAYOUT.show_edges(True)
    self.LAYOUT.show_bounds(True)

  def sync(self, data):
    """ Sync widget state to data elements """
    if data["updated"] and data["turn_off"]:
      self.LAYOUT.show_edges(False)
      self.LAYOUT.show_bounds(False)
    self.LAYOUT.model = data


# Instance
layout = Sample2()
