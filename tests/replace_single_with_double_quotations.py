# coding: utf-8
import re
from IPython.lib import clipboard


raw = clipboard.osx_clipboard_get().replace("'", '"')
name = re.search(r'/createTable/(?P<name>[a-z_]+)/', raw).groupdict('name').get('name')
print(f'\n### Creating the Table `{name}`:\n{raw.strip()}')
