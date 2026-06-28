"""Write LibreOffice color palettes to a JSON file."""

import glob
import json
import re

import palettes

color_palettes = {}
for file in glob.iglob('*.soc'):
    with open(file, 'r') as f:
        text = f.read()
        color_list = re.findall('#......', text)
        color_palettes[file.removesuffix('.soc')] = color_list

with open('palettes.json', 'w') as f:
    json.dump(color_palettes, f)

