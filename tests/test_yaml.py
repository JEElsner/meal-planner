import pytest

import yaml
from yaml import Loader, Dumper
from meal_planner import Recipe, Plan

def test_save_recipe():
    r = Recipe('Aloo Faliyan', 4, ['Green Beans', 'Shallots', 'Cherry Tomatoes', 'Cilantro'], 'A tasty Indian dish!')
    output = yaml.dump(r)
    assert output == '!Recipe\ndescription: A tasty Indian dish!\ningredients:\n- Green Beans\n- Shallots\n- Cherry Tomatoes\n- Cilantro\nname: Aloo Faliyan\nservings: 4\n'
    assert yaml.load(output, Loader) == r
    
def test_save_plan():
    r = Recipe('Aloo Faliyan', 4, ['Green Beans', 'Shallots', 'Cherry Tomatoes', 'Cilantro'], 'A tasty Indian dish!')
    p = Plan.create_empty_plan(['Tuesday', 'Wednesday', 'Thursday'])
    p.set_meal('Tuesday', 'Breakfast', r)

    output = yaml.dump(p)
    assert output == '!MealPlan\ndays:\n- Tuesday\n- Wednesday\n- Thursday\nmeals:\n- Breakfast\n- Lunch\n- Dinner\nschedule:\n  Thursday:\n    Breakfast: null\n    Dinner: null\n    Lunch: null\n  Tuesday:\n    Breakfast: !Recipe\n      description: A tasty Indian dish!\n      ingredients:\n      - Green Beans\n      - Shallots\n      - Cherry Tomatoes\n      - Cilantro\n      name: Aloo Faliyan\n      servings: 4\n    Dinner: null\n    Lunch: null\n  Wednesday:\n    Breakfast: null\n    Dinner: null\n    Lunch: null\n'
    assert yaml.load(output, Loader) == p
    