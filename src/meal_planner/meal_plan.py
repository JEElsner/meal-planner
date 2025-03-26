from __future__ import annotations
from typing import Iterable, Dict, Set, Any

from .recipe import Recipe

import yaml

class Plan(yaml.YAMLObject):
    yaml_tag = u'!MealPlan'

    def __init__(self, days:Iterable[Any]=None, meals: Iterable[Any]=None, schedule: Dict[Any, Dict[Any, Recipe]]=None):
        self.days = days
        self.meals = meals
        self.schedule = schedule
    
    @classmethod
    def create_empty_plan(cls, days:Iterable[Any]=None, meals: Iterable[Any]=None) -> Plan:
        if days is None:
            days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 'Monday']
            
        if meals is None:
            meals = ['Breakfast', 'Lunch', 'Dinner']
            
        return Plan(days, meals, {day: {meal: None for meal in meals} for day in days}) 
        

    @property
    def recipes(self) -> Set[Recipe]:
        recipes = set()

        for day_meals in self.schedule.values():
            recipes.update(day_meals)

        return recipes
    
    def set_meal(self, day, meal, recipe: Recipe) -> None:
        self.schedule[day][meal] = recipe
        
    def meals_remaining(self) -> Dict[Recipe, int]:
        serving_counts = dict()

        for day in self.schedule.values():
            for meal in day.values():
                if meal is None:
                    continue
                
                serving_counts[meal] = serving_counts.get(meal, meal.servings) - 1
                
        return serving_counts

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
    
    def __repr__(self) -> str:
        return f"{self!s}(days={self.days!r}, meals={self.meals!r}, schedule={self.schedule!r})"

    def __eq__(self, value):
        if not isinstance(value, self.__class__):
            return False
        
        return self.days == value.days and self.meals == value.meals and self.schedule == value.schedule
