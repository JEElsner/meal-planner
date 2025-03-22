from .config import Config
from .text_ui import MealPlanShell

config = Config.load_config()

MealPlanShell().cmdloop()