from typing import List

import yaml

class Recipe(yaml.YAMLObject):
    yaml_tag = u'!Recipe'
    
    def __init__(self, name: str, servings: int, ingredients: List[str]=list(), description: str=None):
        self.name = name
        self.servings = servings
        self.ingredients = ingredients
        self.description = description

    def __str__(self) -> str:
        return self.name
    
    def __format__(self, format_spec):
        return self.name.__format__(format_spec)
    
    def __repr__(self):
        return f"{self!s}(name={self.name!r}, servings={self.servings!r}, ingredients={self.ingredients!r}, description={self.description!r})"
    
    def __eq__(self, value):
        if not isinstance(value, self.__class__):
            return False
        
        return self.name == value.name and self.servings == value.servings and self.ingredients == value.ingredients and self.description == value.description
    
    def __hash__(self):
        return hash((self.name, self.servings, tuple(self.ingredients), self.description))