from __future__ import annotations

import yaml

from typing import Literal

from pathlib import Path

class Config(yaml.YAMLObject):
    yaml_tag = u'!Config'

    def __init__(self, plan_directory=Path('./data'),
                  recipe_directory=Path('./data/recipes'),
                  default_days=None):
        self.plan_directory = plan_directory
        self.recipes_directory = recipe_directory
        
        if default_days is None:
            self.default_days = ['Tuesday1', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 'Monday', 'Tuesday2']
        else:
            self.default_days = default_days

    def load_config(create: Literal[False, 'cwd', 'user']='cwd') -> Config:
        """Attempt to locate and load the planner configuration."""

        config_name = 'meal-planner-config.yml'
        user_cfg = Path.home() / config_name
        cwd_cfg = Path.cwd() / config_name

        config = Config()

        if user_cfg.exists():
            with user_cfg.open('r') as f:
                config = yaml.load(f.read(), yaml.Loader)
        elif cwd_cfg.exists():
            with cwd_cfg.open('r') as f:
                config = yaml.load(f.read(), yaml.Loader)
        elif create == 'user':
            with user_cfg.open('w') as f:
                yaml.dump(config, f)
        elif create == 'cwd':
            with cwd_cfg.open('w') as f:
                yaml.dump(config, f)

        return config
    
    def __str__(self) -> str:
        return self.__repr__()
    
    def __repr__(self) -> str:
        return f"Config(plan_directory={self.plan_directory!r}, recipes_directory={self.recipes_directory!r}, default_days={self.default_days!r})"
