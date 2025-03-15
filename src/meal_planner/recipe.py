from typing import List

class Recipe:
    def __init__(self, name: str, servings: int, ingredients: List[str]=list(), description: str=None):
        self.name = name
        self.servings = servings
        self.ingredients = ingredients
        self.description = description

    def __str__(self) -> str:
        return self.name
    
    def __format__(self, format_spec):
        return self.name.__format__(format_spec)