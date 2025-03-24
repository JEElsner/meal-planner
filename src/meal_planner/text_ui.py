import cmd

from .meal_plan import Recipe
from .meal_plan import Plan as MealPlan
from .config import Config

from typing import List

def parse(s: str) -> List[str]:
    quote = None
    tokens = list()
    curr = ""

    for c in s:
        add_to_curr = True
        if c in ['"', "'"] and (c == quote or quote is None):
            if quote is None:
                quote = c
            else:
                quote = None
                
            add_to_curr = False

        if c in [' ', '\t', '"', "'"] and curr and not quote:
            tokens.append(curr)
            curr = ""
            
            add_to_curr = False
            
        if add_to_curr:
            curr += c
            
    if curr:
        tokens.append(curr)

    return tokens

class MealPlanShell(cmd.Cmd):
    recipes = dict()

    prompt = "(meal planner) "
    
    def __init__(self, config: Config, plan: MealPlan=None, completekey = "tab", stdin = None, stdout = None):
        super().__init__(completekey, stdin, stdout)
        
        self.config = config
        
        if plan is None:
            self.plan = MealPlan.create_empty_plan(config.default_days)
        else:
            self.plan = plan

    def do_newplan(self, args):
        """Create a new meal plan
        
        Args:
            type: The type of meal plan to create. Only 'week' is currently supported.
            begin: The first day of the meal plan.
            end: The last day of the meal plan.
        """
        args = parse(args)
        type_ = args[0]

        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        
        success = False

        if type_.lower() == 'week':
            _, begin, end = args
            begin_idx = days.index(begin)
            end_idx = (days.index(end))

            self.plan = MealPlan.create_empty_plan(days[begin_idx:] + days[:end_idx+1])
            success = True
        elif type_.lower() == 'default':
            self.plan = MealPlan.create_empty_plan(self.config.default_days)
            success = True
        else:
            print('Unknown plan format')

        if success:
            print(self.plan)

    def do_newrecipe(self, args):
        """Add a new recipe."""
        name, servings = parse(args)
        servings = int(servings)
        
        self.recipes[name] = Recipe(name, servings)
        print(f'Created recipe {name}')

    def do_set(self, args):
        """Set the meal a given day and time."""
        day, meal, recipe_str = parse(args)
        
        recipe = self.recipes.get(recipe_str, None)
        
        if recipe is None:
            resp = input(f"Unknown recipe {recipe_str}. Create? (y/N) ")
            if resp.lower().startswith('y'):
                # TODO make number of servings alterable
                self.recipes[recipe_str] = Recipe(recipe_str, 4)
                recipe = self.recipes[recipe_str]
        
        self.plan.set_meal(day, meal, recipe)
        print(self.plan)
    
    def do_check(self, args):
        print("Meals Remaining")
        print("-------------------")

        for meal, servings in self.plan.meals_remaining().items():
            print(f"{meal:<10}: {servings}")

        print()
        if self.plan.validate():
            print('No phantom meals!')
        else:
            print("You're gonna starve!")

    def do_print(self, args):
        """Print the current meal plan."""
        print(self.plan)
        
    def do_quit(self, args):
        """Quit the meal planner."""
        return True
    
    def do_exit(self, args):
        """Quit the meal planner."""
        return True
    
    def do_test(self, arg):
        print(arg)
    