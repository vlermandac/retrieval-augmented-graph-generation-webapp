import yaml
import os
from typing import Union
from dotenv import load_dotenv
from core_classes import Config


class ConfigVariables:
    def __init__(self, root):
        self.root = root
        self.config = {}
        self.config_1d = {}
        self.parse_config_file()

    def parse_config_file(self):
        with open(f'{self.root}config.yml', 'r') as ymlfile:
            cfg = yaml.safe_load(ymlfile)
        self.config = cfg
        for key, val in cfg.items():
            if isinstance(val, dict):
                for k, v in val.items():
                    self.config_1d[k] = v

    def update_config(self, new_config: Config):
        self.config['preprocess'] = new_config.preprocess.dict()
        self.config['llm'] = new_config.llm.dict()
        self.config['rag'] = new_config.rag.dict()
        with open(f'{self.root}config.yml', 'w') as ymlfile:
            yaml.dump(self.config, ymlfile)
        self.parse_config_file()

    def update_config_option(self, option: str, value: Union[str, int, float]):
        if (option in self.config['preprocess']):
            self.config['preprocess'][option] = value
        if (option in self.config['llm']):
            self.config['llm'][option] = value
        if (option in self.config['rag']):
            self.config['rag'][option] = value
        with open(f'{self.root}config.yml', 'w') as ymlfile:
            yaml.dump(self.config, ymlfile)
        self.parse_config_file()

    def env_vars(self, *args):
        load_dotenv()
        return {arg: str(os.getenv(arg)) for arg in args}

    def __call__(self, *args):
        sub_dict = {}
        for arg in args:
            if arg in self.config_1d:
                sub_dict[arg] = self.config_1d[arg]
            else:
                print(f"Warning: '{arg}' not found in the configuration.")
        return sub_dict
