#!/usr/bin/env python3
from pathlib import Path
import sys

print(sys.path[0])
sys.path.append(str(Path(sys.path[0]).parent)) if not list(Path(sys.path[0]).glob('utils')) else ''
print(sys.path[-1])

from utils.paths import get_py_path

if __name__ == '__main__':
    print(get_py_path())
