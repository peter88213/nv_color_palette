"""Provide a dialog to choose a color.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/nv_color_palette
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tkinter import ttk

from nvcolorpalette.nvcolorpalette_globals import PALETTES
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

    COLORS_PER_ROW = 12
    COLOR_FIELD_WIDTH = 2

    def __init__(self, chooser, ui, controller, title, initialcolor, **kw):

        def cancel():
            self.destroy()

        def change_palette(event=None):
            chooser.paletteIndex = palettes.index(
                self._predefinedPaletteVar.get()
            )
            self._draw_color_palette(
                self._paletteArea,
                PALETTES[
                    palettes[chooser.paletteIndex]
                ]
            )

        def choose_color():
            self._system_chooser_is_active = True
            color = colorchooser.askcolor(
                parent=self,
                title=title,
                color=self._color,
            )[1]
            self._system_chooser_is_active = False
            if color is not None:
                self._set_current_color(color)

        def get_color_entry(event=None):
            color = self._colorVar.get()
            if HexColor.is_hex_color(color):
                self._set_current_color(color)
            else:
                self._colorVar.set(self._color)

        def on_quit(event=None):
            if self._system_chooser_is_active:
                return 'break'

            self.destroy()

        def open_help_page(event=None):
            self._ctrl.open_help(
                page=HELP_PAGE,
                site=HELP_SITE
            )

        def return_color():
            self._chooser.color = self._color
            self.destroy()

        super().__init__(ui, **kw)
        self._ctrl = controller
        self.title(title)
        self.protocol("WM_DELETE_WINDOW", on_quit)
        self._system_chooser_is_active = False
        # semaphore (necessary for Linux)

        self._chooser = chooser
        self._chooser.color = None
        self._color = initialcolor

        prefs = self._ctrl.get_preferences()
        initialcolor = initialcolor or prefs['color_text_fg']

        #--- Predefined palette area.
        palettes = list(PALETTES)
        self._predefinedPaletteVar = tk.StringVar()
        ttk.OptionMenu(
            self,
            self._predefinedPaletteVar,
            palettes[chooser.paletteIndex],
            *palettes,
            command=change_palette,
        ).pack(anchor='w')

        self._paletteArea = ttk.Frame(self)
        self._paletteArea.pack(fill='both', expand=True)

        ttk.Separator(
            self,
            orient='horizontal',
        ).pack(fill='x')

        #--- Current color selection preview.
        previewWindow = ttk.Frame(self)
        previewWindow.pack(fill='both', expand=False)

        self._currentColorPreviewInv = tk.Label(
            previewWindow,
            text=_('Background'),
        )
        self._currentColorPreviewInv.pack(side='right', fill='x', expand=True)

        self._currentColorPreview = tk.Label(
            previewWindow,
            text=_('Foreground'),
            bg=prefs['color_text_bg'],
        )
        self._currentColorPreview.pack(side='left', fill='x', expand=True)

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

        self._set_current_color(initialcolor)

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

        self._draw_color_palette(
            self._paletteArea,
            PALETTES[
                palettes[chooser.paletteIndex]
            ]
        )

    def _draw_color_palette(self, paletteArea, palette):

        # Clear the palette area.
        for field in paletteArea.grid_slaves():
            field.grid_forget()

        # Populate the palette area with the color fields.
        for i, color in enumerate(palette):
            tk.Button(
                paletteArea,
                relief='flat',
                overrelief='raised',
                bg=color,
                width=self.COLOR_FIELD_WIDTH,
                command=lambda c=color: self._set_current_color(c),
            ).grid(
                row=i // self.COLORS_PER_ROW,
                column=i % self.COLORS_PER_ROW,
                padx=5,
                pady=5,
            )

    def _set_current_color(self, color):

        def contrast_color(c):
            contrastCol = '#ffffff' if HexColor.is_dark(c) else '#000000'
            return contrastCol

        self._color = color
        self._currentColorPreviewInv['bg'] = color
        self._currentColorPreviewInv['fg'] = contrast_color(color)
        self._currentColorPreview['fg'] = color
        self._colorVar.set(self._color)
