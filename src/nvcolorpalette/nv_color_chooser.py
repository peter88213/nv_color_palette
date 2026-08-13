"""Provide a class to choose a color.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/nv_color_palette
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvcolorpalette.palette_view import PaletteView


class NvColorChooser:

    def __init__(self, ui, controller):
        self._ui = ui
        self._ctrl = controller
        self.color = None

    def choose_color(self, title='', initialcolor=None):
        palette = PaletteView(self, self._ui, self._ctrl, title, initialcolor)
        palette.wait_window(palette)

        return self.color
