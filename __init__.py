bl_info = {
    "name"       : "嘉然之声 (Sound Daily)",
    "author"     : "Atticus",
    "version"    : (0, 4),
    "blender"    : (2, 93, 0),
    "location"   : "3D视窗>侧面板",
    "description": "时刻聆听圣嘉然吧，获取属于你的建模纯度",
    'warning'    : "",
    "doc_url"    : "",
    "category"   : "Sound",
}

import bpy
import importlib
import sys
import os
from itertools import groupby

# get folder name
__folder_name__ = __name__
__dict__ = {}
addon_dir = os.path.dirname(__file__)

# get all .py file path
py_paths = [os.path.join(root, f) for root, dirs, files in os.walk(addon_dir) for f in files if
            f.endswith('.py') and f != '__init__.py']

for path in py_paths:
    name = os.path.basename(path)[:-3]
    correct_path = path.replace('\\', '/')
    # split path with folder name
    dir_list = [list(g) for k, g in groupby(correct_path.split('/'), lambda x: x == __folder_name__) if
                not k]
    # combine path and make dict like this: 'name:folder.name'
    if 'preset' not in dir_list[-1]:
        r_name_raw = __folder_name__ + '.' + '.'.join(dir_list[-1])
        __dict__[name] = r_name_raw[:-3]

# auto reload
for name in __dict__.values():
    if name in sys.modules:
        importlib.reload(sys.modules[name])
    else:
        globals()[name] = importlib.import_module(name)
        setattr(globals()[name], 'modules', __dict__)


def register():
    for name in __dict__.values():
        if name in sys.modules and hasattr(sys.modules[name], 'register'):
            try:
                sys.modules[name].register()
            except ValueError:  # open a template file may cause this problem
                pass


def unregister():
    for name in __dict__.values():
        if name in sys.modules and hasattr(sys.modules[name], 'unregister'):
            sys.modules[name].unregister()


if __name__ == '__main__':
    register()
