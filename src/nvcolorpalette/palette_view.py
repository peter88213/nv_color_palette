"""Provide a dialog to choose a color.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/nv_color_palette
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tkinter import colorchooser
from tkinter import ttk

from nvcolorpalette.nvcolorpalette_globals import HELP_PAGE
from nvcolorpalette.nvcolorpalette_globals import HELP_SITE
from nvcolorpalette.nvcolorpalette_globals import PALETTES
from nvcolorpalette.nvcolorpalette_globals import prefs
from nvcolorpalette.nvcolorpalette_locale import _
from nvcolorpalette.platform.platform_settings import KEYS
from nvcolorpalette.platform.platform_settings import PLATFORM
from nvlib.gui.widgets.modal_dialog import ModalDialog
from nvlib.gui.widgets.my_string_var import MyStringVar
from nvlib.model.hex_color import HexColor
import tkinter as tk


class PaletteView(ModalDialog):

    COLORS_PER_ROW = 12
    COLOR_FIELD_WIDTH = 2

    def __init__(self, chooser, ui, controller, title, initialcolor, **kw):

        def cancel():
            self.destroy()

        def change_predefined_palette(event=None):
            paletteName = predefinedPaletteVar.get()
            paletteIndex = paletteNames.index(paletteName)
            prefs['palette_index'] = paletteIndex
            draw_color_palette(
                predefinedPaletteArea,
                PALETTES[paletteName]
            )

        def choose_color():
            self._system_chooser_is_active = True
            color = colorchooser.askcolor(
                parent=self,
                title=title,
                color=self._selectedColor,
            )[1]
            self._system_chooser_is_active = False
            if color is not None:
                set_color_selection(color)

        def config_modify_custom_palette_button():
            modifyCustomPaletteButton['text'] = (
                _('Remove selected color') if self._selectedColor in prefs['custom_palette']
                else _('Add selected color')
            )

        def draw_color_palette(paletteArea, palette):

            # Clear the palette area.
            for child in paletteArea.winfo_children():
                child.destroy()
            paletteView = ttk.Frame(paletteArea)
            paletteView.pack(fill='both', expand=True)

            # Populate the palette area with the color fields.
            for i, color in enumerate(palette):
                tk.Button(
                    paletteView,
                    relief='flat',
                    overrelief='raised',
                    bg=color,
                    width=self.COLOR_FIELD_WIDTH,
                    command=lambda c=color: set_color_selection(c),
                ).grid(
                    row=i // self.COLORS_PER_ROW,
                    column=i % self.COLORS_PER_ROW,
                    padx=5,
                    pady=5,
                )

        def get_color_entry(event=None):
            color = colorEntryVar.get()
            if HexColor.is_hex_color(color):
                set_color_selection(color)
            else:
                colorEntryVar.set(self._selectedColor)

        def on_quit(event=None):
            if self._system_chooser_is_active:
                return 'break'

            self.destroy()

        def open_help_page(event=None):
            self._ctrl.open_help(
                page=HELP_PAGE,
                site=HELP_SITE
            )

        def modify_custom_palette(event=None):
            if self._selectedColor in prefs['custom_palette']:
                prefs['custom_palette'].remove(self._selectedColor)
            else:

                prefs['custom_palette'].append(self._selectedColor)
            draw_color_palette(
                customPaletteArea,
                prefs['custom_palette'],
            )
            config_modify_custom_palette_button()

        def return_selected_color():
            chooser.color = self._selectedColor
            self.destroy()

        def set_color_selection(color):

            def contrast_color(c):
                contrastCol = '#ffffff' if HexColor.is_dark(c) else '#000000'
                return contrastCol

            self._selectedColor = color
            selectedColorBgPreview['bg'] = color
            selectedColorBgPreview['fg'] = contrast_color(color)
            selectedColorFgPreview['fg'] = color
            colorEntryVar.set(color)
            config_modify_custom_palette_button()

        super().__init__(ui, **kw)
        self._ctrl = controller

        #--- Configure the pop-up window.
        self.resizable(0, 0)
        if PLATFORM == 'win':
            self.attributes('-toolwindow', True)
        self.title(title)
        self.protocol("WM_DELETE_WINDOW", on_quit)

        self._system_chooser_is_active = False
        # semaphore (necessary for Linux)

        chooser.color = None
        self._selectedColor = initialcolor

        mainPrefs = self._ctrl.get_preferences()
        initialcolor = initialcolor or mainPrefs['color_text_fg']

        #--- Predefined palette area.
        paletteNames = list(PALETTES)
        predefinedPaletteVar = tk.StringVar()
        ttk.OptionMenu(
            self,
            predefinedPaletteVar,
            paletteNames[int(prefs['palette_index'])],
            *paletteNames,
            command=change_predefined_palette,
        ).pack(anchor='w')

        predefinedPaletteArea = ttk.Frame(self)
        predefinedPaletteArea.pack(
            padx=5,
            pady=5,
            fill='both',
            expand=True,
        )

        ttk.Separator(
            self,
            orient='horizontal',
        ).pack(fill='x')

        #--- Custom palette area.

        # Header.
        customPaletteHeader = ttk.Frame(self)
        customPaletteHeader.pack(
            fill='both',
            expand=False,
        )
        ttk.Label(
            customPaletteHeader,
            text=_('Custom palette'),
        ).pack(
            side='left',
            padx=5,
            pady=5,
        )

        # Button to add/remove the current color.
        modifyCustomPaletteButton = ttk.Button(
            customPaletteHeader,
            command=modify_custom_palette,
        )
        modifyCustomPaletteButton.pack(
            side='right',
            padx=5,
            pady=5,
            fill='x',
            expand=True,
        )
        customPaletteArea = ttk.Frame(self)
        customPaletteArea.pack(
            padx=5,
            pady=5,
            fill='both',
            expand=True,
        )

        ttk.Separator(
            self,
            orient='horizontal',
        ).pack(fill='x')

        #--- User-defined color setting.
        colorEntryWindow = ttk.Frame(self)
        colorEntryWindow.pack(
            fill='x',
            expand=False,
        )

        # Hex color entry
        colorEntryVar = MyStringVar(value=initialcolor)
        colorEntry = ttk.Entry(
            colorEntryWindow,
            textvariable=colorEntryVar,
        )
        colorEntry.bind('<Return>', get_color_entry)
        colorEntry.pack(
            padx=5,
            pady=5,
            side='left',
        )

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

        ttk.Separator(
            self,
            orient='horizontal',
        ).pack(fill='x')

        #--- Current color selection preview.
        previewWindow = ttk.Frame(self)
        previewWindow.pack(
            padx=5,
            pady=5,
            fill='both',
            expand=False,
        )

        selectedColorBgPreview = tk.Label(
            previewWindow,
            text=_('Background'),
        )
        selectedColorBgPreview.pack(side='right', fill='x', expand=True)

        selectedColorFgPreview = tk.Label(
            previewWindow,
            text=_('Foreground'),
            bg=mainPrefs['color_text_bg'],
        )
        selectedColorFgPreview.pack(side='left', fill='x', expand=True)

        ttk.Separator(
            self,
            orient='horizontal',
        ).pack(fill='x')

        #--- Footer bar with buttons.
        footer = tk.Frame(self)
        footer.pack(
            fill='both',
            expand=False,
        )

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
            command=return_selected_color,
        ).pack(padx=5, pady=5, side='right')

        #--- Set key bindings.
        self.bind(KEYS.OPEN_HELP[0], open_help_page)
        self.bind(KEYS.QUIT_PROGRAM[0], on_quit)

        #--- Set data.
        draw_color_palette(
            predefinedPaletteArea,
            PALETTES[paletteNames[prefs['palette_index']]]
        )
        draw_color_palette(
            customPaletteArea,
            prefs['custom_palette'],
        )
        set_color_selection(initialcolor)
        config_modify_custom_palette_button()

