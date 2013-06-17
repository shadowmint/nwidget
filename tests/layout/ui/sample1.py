from nwidget.layout import *
import nwidget


# Widgets
class ThisUi(LayoutBase):
  """ Example UI """

  def __init__(self):
    super(ThisUi, self).__init__()

  def widgets(self, helper):
    """ Create widgets """

    helper.scope(globals())

    # Common edges
    LEFT_OFFSET = edge(LEFT, 10, MM)

    # Define bounds
    BUTTON_PANEL_HEADER = bound(
      LEFT_OFFSET,
      edge(TOP, -20, MM),
      edge(LEFT_OFFSET, 50, PERCENT),
      edge(TOP, -10, MM)
    )
    CENTRAL_PANEL = bound(
      edge(CENTER.X, -20, MM),
      edge(CENTER.Y, -10, MM),
      edge(CENTER.X, 20, MM),
      edge(CENTER.Y, 10, MM)
    )
    BUTTON_SET = bound(
      LEFT_OFFSET,
      edge(BOTTOM, 20, MM),
      edge(CENTER.X, -40, MM),
      edge(TOP, -25, MM)
    )

    # Widgets
    self.MAIN_BUTTON = widget(theme.button(), BUTTON_PANEL_HEADER, text="Click me", color=(255, 0, 0, 255))
    self.OTHER_BUTTON = widget(theme.button(), CENTRAL_PANEL, text="Click Me", color=(255, 255, 0, 255), font_size=6)
    self.BUTTONS = widget(nwidget.VList(), BUTTON_SET)
    for i in range(5):
      b = theme.button()
      b.text = "Button : " + str(i)
      self.BUTTONS.add(b)

    # Set event codes for app to handle
    self.MAIN_BUTTON.on_click = "MAIN_BUTTON_CLICK"
    self.OTHER_BUTTON.on_click = "DEBUG_CLICK"

  def sync(self, data):
    """ Sync widget state to data elements """
    if data["updated"]:
      self.MAIN_BUTTON.disabled = not data['main_button_enabled']
      self.MAIN_BUTTON.text = data['main_text']
      data["updated"] = False


# Instance
layout = ThisUi()
