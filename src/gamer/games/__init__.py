# importing game instances as sub-package
# moving Game class out of instance folder
from . import instances
Game = instances.Game

from . import instances
helpers = instances.helpers
