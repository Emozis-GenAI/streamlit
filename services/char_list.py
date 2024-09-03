import streamlit as st
import requests 
import json 

from core.logger import logger
from core.config import configs
from core.utils import *

from services.converter import Converter

class CharListService:
    @staticmethod 
    def my_character_info():
        result = {}
        response = requests.get(
            url=f"{configs.API_URL}/character/user",
            json=st.session_state["user"]
        )
        if response.status_code == 200:
            response_json = json.loads(response.text)
            if response_json["status"] == "success":
                data = json.loads(response.text)["data"]
                ordered_data = sorted(data, key=lambda x: x["createDate"], reverse=True)
                result = {i:x for i, x in enumerate(ordered_data)}
                logger.success(response_json["message"])
            else:
                logger.warning(response_json["message"])
        else:
            logger.warning("🚨 API 연결에 실패했습니다.")

        return result
    
    @staticmethod
    def del_character(data):
        result = False

        response = requests.delete(
            url=f"{configs.API_URL}/character/{data['_id']}"
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

        return result