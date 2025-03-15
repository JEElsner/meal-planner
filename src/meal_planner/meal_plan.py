from typing import Iterable, Dict, Set, Any

from .recipe import Recipe

class Plan:
    def __init__(self, days:Iterable[Any]=None, meals: Iterable[Any]=None):
        if days is None:
            days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 'Monday']
            
        if meals is None:
            meals = ['Breakfast', 'Lunch', 'Dinner']
        
        self.days: Dict[Any, Dict[Any, Recipe]] = days
        self.meals = meals

        self.schedule = {day: {meal: None for meal in meals} for day in days}

    @property
    def recipes(self) -> Set[Recipe]:
        recipes = set()

        for day_meals in self.schedule.values():
            recipes.update(day_meals)

        return recipes
    
    def set_meal(self, day, meal, recipe: Recipe) -> None:
        self.schedule[day][meal] = recipe
        
    def meals_remaining(self) -> Dict[Recipe, int]:
        recipes = dict()

        for day in self.schedule.values():
            for meal in day.values():
                if meal is None:
                    continue
                
                recipes[meal] = recipes.get(meal, meal.servings) - 1
                
        return recipes

    def validate(self):
        return all(map(lambda x: x >= 0, self.meals_remaining().values()))
    
    def __str__(self) -> str:
        # longest_day = max(map(len, map(str, self.days))) + 1
        # longest_recipe = max(map(len, map(str, self.recipes)))
        # longest_meal_name = max(map(len, map(str, self.meals)))
        # longest_col_name = max(longest_recipe, longest_meal_name) + 1
        
        longest_day = 10
        longest_col_name = 10

        hbar = "+" + "-"*longest_day + "+" + ("-" * longest_col_name + "+") * len(self.meals) + "\n"

        s = ""
        s += hbar
        s += "|" + (' ' * longest_day) + "|"
        for meal_name in self.meals:
            s += f"{meal_name:<10}|"
        s += "\n" + hbar
        for day in self.days:
            s += f"|{day:<10}|"
            for meal in self.meals:
                s += f"{self.schedule[day][meal] or '':<10}|"
            s += "\n" + hbar

        return s
