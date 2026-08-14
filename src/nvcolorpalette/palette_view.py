"""Provide a dialog to choose a color.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/nv_color_palette
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tkinter import ttk

from nvcolorpalette.nvcolorpalette_globals import COLORS
from nvcolorpalette.nvcolorpalette_globals import HELP_PAGE
from nvcolorpalette.nvcolorpalette_globals import HELP_SITE
from nvcolorpalette.nvcolorpalette_locale import _
from nvlib.gui.platform.platform_settings import KEYS
from nvlib.gui.widgets.modal_dialog import ModalDialog
from nvlib.model.hex_color import HexColor
import tkinter as tk


class PaletteView(ModalDialog):

    COLORS_PER_ROW = 8
    COLOR_FIELD_WIDTH = 5

    def __init__(self, chooser, ui, controller, title, initialcolor, **kw):

        def cancel():
            self.destroy()

        def contrast_color(c):
            contrastCol = '#ffffff' if HexColor.is_dark(c) else '#000000'
            return contrastCol

        def open_help_page(event=None):
            self._ctrl.open_help(
                page=HELP_PAGE,
                site=HELP_SITE
            )

        def return_color():
            self._chooser.color = self._color
            self.destroy()

        def set_current_color(color):
            self._color = color
            self._currentColorInv['bg'] = color
            self._currentColorInv['fg'] = contrast_color(color)
            self._currentColor['fg'] = color

        super().__init__(ui, **kw)
        self._ctrl = controller
        self.title(title)

        self._chooser = chooser
        self._chooser.color = None
        self._color = None

        prefs = self._ctrl.get_preferences()
        initialcolor = initialcolor or prefs['color_text_fg']

        self._paletteArea = ttk.Frame(self)
        self._paletteArea.pack(fill='both', expand=True)

        ttk.Separator(
            self,
            orient='horizontal',
        ).pack(fill='x')

        #--- Current color selection preview.
        self._preview = ttk.Frame(self)
        self._preview.pack(fill='both', expand=False)

        self._currentColorInv = tk.Label(
            self._preview,
            text=_('Inverted display'),
            fg=contrast_color(initialcolor),
            bg=initialcolor,
        )
        self._currentColorInv.pack(side='right', fill='x', expand=True)

        self._currentColor = tk.Label(
            self._preview,
            text=_('Regular display'),
            fg=initialcolor,
            bg=prefs['color_text_bg'],
        )
        self._currentColor.pack(side='left', fill='x', expand=True)

        ttk.Separator(
            self,
            orient='horizontal',
        ).pack(fill='x')

        #--- Footer bar with buttons.
        self._footer = ttk.Frame(self)
        self._footer.pack(fill='both', expand=False)

        # "Cancel" button.
        ttk.Button(
            self._footer,
            text=_('Cancel'),
            command=cancel,
        ).pack(padx=5, pady=5, side='right')

        # "Help" button.
        ttk.Button(
            self._footer,
            text=_('Help'),
            command=open_help_page,
        ).pack(padx=5, pady=5, side='right')

        # "Ok" button.
        ttk.Button(
            self._footer,
            text=_('Apply'),
            command=return_color,
        ).pack(padx=5, pady=5, side='right')

        #--- Set Key bindings.
        self.bind(KEYS.OPEN_HELP[0], open_help_page)

        #--- Draw the color palette.
        for i, color in enumerate(COLORS):
            tk.Button(
                self._paletteArea,
                relief='flat',
                overrelief='raised',
                bg=color,
                width=self.COLOR_FIELD_WIDTH,
                command=lambda c=color: set_current_color(c),
            ).grid(
                row=i // self.COLORS_PER_ROW,
                column=i % self.COLORS_PER_ROW,
                padx=5,
                pady=5,
            )

