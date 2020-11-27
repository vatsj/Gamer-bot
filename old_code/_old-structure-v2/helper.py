"""
helper function for importing other files using relative paths
uses information about its absolute path (stored in rootDir)
"""

print("RUNNING HELPER MODULE")

import os
import importlib
import sys

# manually setting root dir
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
# gameDir = rootDir + "/src/types/Game.py"
# playerDir = rootDir + "/src/types/Player.py"

# imports and returns module given by path
def import_helper(relPath, name):
    absPath = ROOT_DIR + relPath

    # imports path as "module"
    spec = importlib.util.spec_from_file_location(name, absPath)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)

    return module
