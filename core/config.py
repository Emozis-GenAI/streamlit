import os
import yaml
from dotenv import load_dotenv, find_dotenv
from pathlib import Path 

load_dotenv()
class Config:
    """config 폴더의 정보를 불러오는 클래스"""
    def __init__(self):
        self.path = Path(__file__).parents[1] / "configs"
        self.API_URL = os.getenv("API_URL")
        self.SOCKET_URL = os.getenv("SOCKET_URL")
        self._set_attributes()

    def _read_config(self, file):
        with open(file, "r", encoding="utf-8") as yaml_file:
            config = yaml.safe_load(yaml_file)
        
        return config
    
    def _set_attributes(self):
        for file in self.path.iterdir():
            dictionary = self._read_config(file)
            if file.name == "state.yaml":
                self.dictionary = dictionary
                continue

            for key, value in dictionary.items():
                setattr(self, key, value)
            
configs = Config()