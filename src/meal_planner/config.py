import yaml

from dataclasses import dataclass

from typing import Literal

from pathlib import Path

@dataclass
class Config(yaml.YAMLObject):
    yaml_tag = u'!Config'

    plan_directory = Path('./data')
    recipes_directory = Path('./data/recipes')
    default_days = ['Tuesday1', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 'Monday', 'Tuesday2']

    def load_config(create: Literal[False, 'cwd', 'user']='cwd'):
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
