from .config import Config
from .text_ui import MealPlanShell

config = Config.load_config()
shell = MealPlanShell(config)

try:
    shell.cmdloop()
except KeyboardInterrupt:
    shell.save_recipes()