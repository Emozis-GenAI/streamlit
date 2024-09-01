import yaml
from pathlib import Path 

class Config:
    """config 폴더의 정보를 불러오는 클래스"""
    def __init__(self):
        self.path = Path(__file__).parents[1] / "configs"
        self._set_attributes()

    def _read_config(self):
        configs = {}
        for file in self.path.iterdir():
            with open(file, "r", encoding="utf-8") as yaml_file:
                file_text = yaml.safe_load(yaml_file)
                if file_text:
                    configs.update(file_text)
        
        return configs
    
    def _set_attributes(self):
        self.dictionary = self._read_config()
        for key, value in self.dictionary.items():
            setattr(self, key, value)
            
configs = Config()