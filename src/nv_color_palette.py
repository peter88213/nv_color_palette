"""A color palette dialog for novelibre.

Requires Python 3.7+
Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/nv_color_palette
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
"""
from pathlib import Path

from nvcolorpalette.nvcolorpalette_locale import _
from nvcolorpalette.nv_color_chooser import NvColorChooser
from nvcolorpalette.nvcolorpalette_globals import HELP_PAGE
from nvcolorpalette.nvcolorpalette_globals import HELP_SITE
from nvcolorpalette.nvcolorpalette_globals import prefs
from nvlib.configuration.configuration_json import ConfigurationJson
from nvlib.controller.plugin.plugin_base import PluginBase


class Plugin(PluginBase):
    """A color palette dialog plugin class."""
    VERSION = '@release'
    API_VERSION = '5.64'
    DESCRIPTION = 'Color palette dialog'
    URL = 'https://github.com/peter88213/nv_color_palette'
    HELP_SITE = HELP_SITE
    HELP_PAGE = HELP_PAGE
    INI_FILENAME = 'color_palette.json'
    INI_FILEPATH = '.novx/config'

    SETTINGS = dict(
        palette_index=1,
        custom_palette=[],
    )
    OPTIONS = {}

    def install(self, model, view, controller):
        """Install the plugin at runtime.
        
        Positional arguments:
            model -- reference to the novelibre main model instance.
            view -- reference to the novelibre main view instance.
            controller -- reference to the novelibre main controller instance.

        Extends the superclass method.
        """
        super().install(model, view, controller)
        self._icon = self._get_icon('colors.png')

        #--- Configure the user interface.

        self._add_help_menu_entry(_('Color palette plugin help'))

        # --- Load configuration.
        try:
            homeDir = str(Path.home()).replace('\\', '/')
            configDir = f'{homeDir}/{self.INI_FILEPATH}'
        except:
            configDir = '.'
        self._configuration = ConfigurationJson(
            settings=self.SETTINGS,
            options=self.OPTIONS,
            filePath=f'{configDir}/{self.INI_FILENAME}',
        )
        self._configuration.read()
        prefs.update(self._configuration.settings)
        prefs.update(self._configuration.options)

        #--- Replace the color chooser strategy class.

        self._ui.colorChooser = NvColorChooser(self._ui, self._ctrl)

    def on_quit(self):
        for keyword in prefs:
            if keyword in self._configuration.options:
                self._configuration.options[keyword] = prefs[keyword]
            elif keyword in self._configuration.settings:
                self._configuration.settings[keyword] = prefs[keyword]
        self._configuration.write()
        self._ui.colorChooser.on_quit()
