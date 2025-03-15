import cmd

from .meal_plan import Recipe
from .meal_plan import Plan as MealPlan

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
    plan = None
    recipes = dict()

    prompt = "(meal planner) "

    def do_newplan(self, args):
        """Create a new meal plan
        
        Args:
            type: The type of meal plan to create. Only 'week' is currently supported.
            begin: The first day of the meal plan.
            end: The last day of the meal plan.
        """
        type_, begin, end = parse(args)

        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

        if type_.lower() == 'week':
            begin_idx = days.index(begin)
            end_idx = (days.index(end))

            self.plan = MealPlan(days[begin_idx:] + days[:end_idx+1])
            print(self.plan)
        else:
            print('Unknown plan format')

    def do_newrecipe(self, args):
        """Add a new recipe."""
        name, servings = parse(args)
        servings = int(servings)
        
        self.recipes[name] = Recipe(name, servings)
        print(f'Created recipe {name}')

    def do_set(self, args):
        """Set the meal a given day and time."""
        day, meal, recipe = parse(args)
        
        if recipe is None:
            self.plan.set_meal(day, meal, None)
        else:
            self.plan.set_meal(day, meal, self.recipes[recipe])
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
    
    def do_test(self, arg):
        print(arg)
    