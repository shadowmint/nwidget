## nwidget

nwidget is a simple UI library build on top of pyglet.

#### Here's the ten second pitch: 

Using pyglet or cocos2D? Frustrated with rubbish python UI libraries 
that don't work? 

Try nwidget. 

- Edit your UI layout *live* as you use the application.
- Use device independent layout files without yet another pointless DSL.
- Specifically written for games, including 'game like' UI widgets.
- Fully themeable, comes with built in 'light' and 'gothic' themes.

### Showcase

![Light Theme](https://raw.github.com/shadowmint/nwidget/master/assets/img/light.png) 

![Gothic Theme](https://raw.github.com/shadowmint/nwidget/master/assets/img/gothic.png) 


### Usage

The quickest way to get started is by looking at the sample
app included in samples/snake.

You can also find specific examples in the tests folder:

- For directly invoking the library: tests/nwidget
- For using the in-built theme libraries: tests/theme
- For using device independent layout files: tests/layout
- For working with cocos2d: tests/cocos2d

#### Example using a layout file:

    import nwidget.cocos2d
    import nwidget

    class Ui(nwidget.cocos2d.CocosLayer):
      """ Common ui base """

      def __init__(self, path, model):
        a = nwidget.Assets()
        super(Ui, self).__init__(
          nwidget.theme.Gothic,
          a.resolve("assets", "gothic"),
          a.resolve("ui", path),
          nwidget.Assets(a.resolve("ui"))
        )

        # Model
        self.model = model

        # Turn on debugging
        self.layout.watch()
        self.layout.show_edges(True)
        self.layout.show_bounds(True)


    class GameView(cocos.layer.Layer):
      """ Testing class """

      def __init__(self):
        super(GameView, self).__init__()

        # Read events, discard old event bindings
        nwidget.events.clear(cocos.director.director.window)
        self.is_event_handler = True

        # View model & ui
        self.model = {
          "score" : 0,
          "dead" : False,
          "updated" : False,
          "play_time" : 0,
        }
        self.ui = model.Ui("game.py", self.model)
        self.add(self.ui, z=1) # Above the background

        # bind events
        nwidget.listen("GAME_RESTART", self.on_restart)
        nwidget.listen("GAME_GOTO_MENU", self.on_menu)

        # Background
        bg = model.Background(assets)
        self.add(bg.node)
        # ... etc.

#### Example layout file:

    from nwidget.layout import *
    import nwidget

    class GameWidgets(LayoutBase):

      def __init__(self):
        super(GameWidgets, self).__init__()
        self.__ready = False

      def widgets(self, helper):
        """ Create widgets """

        helper.scope(globals())

        # Top panel
        widget(theme.subpanel(),
          left   = (LEFT, 0, MM),
          bottom = (TOP, -3, PERCENT),
          right  = (RIGHT, 0, MM),
          top    = (TOP, 0, MM)
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

        widget(theme.checkbox(),
          x     = (LEFT, 0, INCH),
          y     = (TOP, 0.25, INCH),
          width = (45, PX),
          top   = (45, PX),
        )

      def sync(self, data):
        """ Sync widget state to data elements
            Notice how we sync on reload using 'ready'
        """
        if data["updated"] or not self.__ready:
          self.play_time.text = "play time: %d seconds" % data["play_time"]
          data["updated"] = False
          self.__ready = True

    # Instance
    layout = GameUi()

### Q&A

#### What's the 'watch' thing?

nwdiget is based around the concept of stand alone .py files that control
UI layout, instead of using a DSL (eg. Kivy) for this.

These files live in their own directory and are assets rather than part of
a module; they are parsed as string at runtime to run the ui.

The benefit of doing this is that its no extra effort to parse and load the
ui files multiple times; if an nwidget layout is set to watch mode, it 
periodically checks the file system for a newer timestamp on the ui file
and reloads it as required.

The 'sync' method provides data binding from a persistent model state 
that is not part of the ui class, so you can *literally* play the game
and edit the UI *at the same time*.

Yes, this *is* slow, because it continually watches the file system for
changes and rebinds UI content; on the other hand, it's crazy useful.

#### Python 3?

When pyglet does it, we'll do it. Most of the code is already python 3
friendly; the rest is a work in progress.

#### Can I use it with Cocos2D?

Yes; look in tests/cocos2d or in sample/snake

#### Do I really need Numpy for this? 

Unfortunately yes. The pyglet font system is pretty broken; there's no way 
to really do this nicely without using fonttools, and unfortunately that 
comes with a dependency on Numpy. 

#### Docs?

Use https://github.com/shadowmint/go-worker to views the docs, or your
favourite text editor.

#### Bundled dependencies? Really?

Well...

- setuptools is broken and can't install numpy, so setup.py doesn't work.
- virtualenv is broken on macs, because it doesn't install pythonw correctly.

So, the easiest way to handle this is just to bundle everything up into the lib
directory and invoke it via custom bootstrap. Look in src/bootstrap.py for this
mess.

It's vile, but, it works, and it'll *always* work.

This is a 'fix one day, when people figure out what the hell they're doing with
distutils'.

### Dependencies to get started

pip install pyglet cocos2d fonttools numpy

Or:

Install SDL from here:
http://www.libsdl.org/download-1.2.php

Install SDL mixer from here:
http://www.libsdl.org/projects/SDL_mixer/

Install Numpy from here:
http://www.scipy.org/Download

Everything else is bundled in the lib/ folder.
