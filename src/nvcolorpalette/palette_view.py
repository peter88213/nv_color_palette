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
from nvlib.gui.widgets.my_string_var import MyStringVar
from tkinter import colorchooser


class PaletteView(ModalDialog):

    COLORS_PER_ROW = 8
    COLOR_FIELD_WIDTH = 5

    def __init__(self, chooser, ui, controller, title, initialcolor, **kw):

        def cancel():
            self.destroy()

        def choose_color():
            self.wm_attributes('-topmost', False)
            color = colorchooser.askcolor(
                title=title,
                color=self._color,
            )[1]
            if color is not None:
                set_current_color(color)
            self.wm_attributes('-topmost', True)

        def contrast_color(c):
            contrastCol = '#ffffff' if HexColor.is_dark(c) else '#000000'
            return contrastCol

        def get_color_entry(event=None):
            color = self._colorVar.get()
            if HexColor.is_hex_color(color):
                set_current_color(color)
            else:
                self._colorVar.set(self._color)

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
            currentColorPreviewInv['bg'] = color
            currentColorPreviewInv['fg'] = contrast_color(color)
            currentColorPreview['fg'] = color
            self._colorVar.set(self._color)

        super().__init__(ui, **kw)
        self._ctrl = controller
        self.title(title)

        self._chooser = chooser
        self._chooser.color = None
        self._color = initialcolor

        prefs = self._ctrl.get_preferences()
        initialcolor = initialcolor or prefs['color_text_fg']

        paletteArea = ttk.Frame(self)
        paletteArea.pack(fill='both', expand=True)

        ttk.Separator(
            self,
            orient='horizontal',
        ).pack(fill='x')

        #--- Current color selection preview.
        previewWindow = ttk.Frame(self)
        previewWindow.pack(fill='both', expand=False)

        currentColorPreviewInv = tk.Label(
            previewWindow,
            text=_('Inverted display'),
            fg=contrast_color(initialcolor),
            bg=initialcolor,
        )
        currentColorPreviewInv.pack(side='right', fill='x', expand=True)

        currentColorPreview = tk.Label(
            previewWindow,
            text=_('Regular display'),
            fg=initialcolor,
            bg=prefs['color_text_bg'],
        )
        currentColorPreview.pack(side='left', fill='x', expand=True)

        #--- User-defined color setting.
        colorEntryWindow = ttk.Frame(self)
        colorEntryWindow.pack(fill='both', expand=True)

        # Hex color entry
        self._colorVar = MyStringVar(value=initialcolor)
        colorEntry = ttk.Entry(
            colorEntryWindow,
            textvariable=self._colorVar,
        )
        colorEntry.bind('<Return>', get_color_entry)
        colorEntry.pack(padx=5, pady=5, side='left')

        # System color chooser.
        ttk.Button(
            colorEntryWindow,
            text=_('Color chooser'),
            command=choose_color,
        ).pack(
            padx=5,
            pady=5,
            side='right',
            fill='x',
            expand=True,
        )

        #--- Footer bar with buttons.
        ttk.Separator(
            self,
            orient='horizontal',
        ).pack(fill='x')
        footer = tk.Frame(self)
        footer.pack(fill='both', expand=False)

        # "Cancel" button.
        ttk.Button(
            footer,
            text=_('Cancel'),
            command=cancel,
        ).pack(padx=5, pady=5, side='right')

        # "Help" button.
        ttk.Button(
            footer,
            text=_('Help'),
            command=open_help_page,
        ).pack(padx=5, pady=5, side='right')

        # "Apply" button.
        ttk.Button(
            footer,
            text=_('Apply'),
            command=return_color,
        ).pack(padx=5, pady=5, side='right')

        #--- Set Key bindings.
        self.bind(KEYS.OPEN_HELP[0], open_help_page)

        #--- Draw the color palette.
        for i, color in enumerate(COLORS):
            tk.Button(
                paletteArea,
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

