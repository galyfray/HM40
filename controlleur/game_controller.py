class GameController(object):
    def __init__(self):
        pass

    @staticmethod
    def on_play_button_click(event, widget):
        if not widget.get_game().is_running():
            widget.get_game().run()
