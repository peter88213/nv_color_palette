"""Build the nv_color_palette novelibre plugin package.
        
Note: VERSION must be updated manually before starting this script.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/nv_color_palette
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os
import sys

sys.path.insert(0, f'{os.getcwd()}/../../novelibre/tools')
from package_builder import PackageBuilder

VERSION = '0.2.0'


class PluginBuilder(PackageBuilder):

    PRJ_NAME = 'nv_color_palette'
    LOCAL_LIB = 'nvcolorpalette'
    GERMAN_TRANSLATION = True

    def add_extras(self):
        self.add_icons()


def main():
    pb = PluginBuilder(VERSION)
    pb.run()


if __name__ == '__main__':
    main()
