import streamlit as st
import requests 
import json 

from core.logger import logger
from core.config import configs
from core.utils import *

class ModifyCharService:
    @staticmethod 
    def update_char_api(data):
        response = requests.put(
            url=f"{configs.API_URL}/character",
            json=data
        )
        if response.status_code == 200:
            response_json = json.loads(response.text)
            if response_json["status"] == "success":
                logger.success(response_json["message"])
                return True
            else:
                logger.warning(response_json["message"])
                
        else:
            logger.warning("🚨 API 연결에 실패했습니다.")

        return False