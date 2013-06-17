from nwidget.layout import *
import nwidget

class SampleUi(LayoutBase):

  def __init__(self):
    super(SampleUi, self).__init__()

  def widgets(self, helper):
    """ Create widgets """

    helper.scope(globals())

    # Basic button with layout
    widget(theme.button(),
      left = (LEFT, 20, MM),
      bottom = (TOP, -40, MM),
      right = (LEFT, 50, MM),
      top = (TOP, -20, MM),
      on_click = "MAIN_BUTTON_CLICK",
      text = "Sample Button"
    )

  def sync(self, data):
    """ Sync widget state to data elements """
    pass

# Instance
layout = SampleUi()
