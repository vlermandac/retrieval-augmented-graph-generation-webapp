import yaml
import os
import sys
from dotenv import load_dotenv

pwd = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(pwd, '../src'))
from core_classes import Config  # noqa: E402


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
