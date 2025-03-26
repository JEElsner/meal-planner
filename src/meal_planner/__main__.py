from .config import Config
from .text_ui import MealPlanShell

config = Config.load_config()

try:
    MealPlanShell(config).cmdloop()
except KeyboardInterrupt:
    pass