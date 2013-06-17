import nwidget.cocos2d
import nwidget

class Ui(nwidget.cocos2d.CocosLayer):
  """ Common ui base """

  def __init__(self, path, model):
    a = Ui.assets()
    super(Ui, self).__init__(
      nwidget.theme.Gothic,
      a.resolve("assets", "gothic"),
      a.resolve("ui", path),
      Ui.ui_assets() 
    )

    # Model
    self.model = model

    # Turn on debugging
    self.layout.watch()
    #self.layout.show_edges(True)
    #self.layout.show_bounds(True)

  @classmethod
  def assets(cls):
    try:
      rtn = cls.__assets
    except:
      cls.__assets = nwidget.Assets()
    return cls.__assets

  @classmethod
  def ui_assets(cls):
    try:
      rtn = cls.__ui_assets
    except:
      path = Ui.assets().resolve("ui")
      cls.__ui_assets = nwidget.Assets(path)
    return cls.__ui_assets
