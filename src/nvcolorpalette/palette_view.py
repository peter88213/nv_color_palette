"""Provide a dialog to choose a color.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/nv_color_palette
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.gui.widgets.modal_dialog import ModalDialog


class PaletteView(ModalDialog):

    def __init__(self, chooser, ui, **kw):
        super().__init__(ui, **kw)
        chooser.color = '#ff0000'
