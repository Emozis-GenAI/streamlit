import streamlit as st
import requests 
import json 

from core.logger import logger
from core.config import configs
from core.utils import *

from services.converter import Converter

class CreateCharService:
    # 프로필 가져오는 메서드
    @staticmethod
    @st.cache_data
    def get_profile(gender):
        result = {}
        response = requests.get(
            url=f"{configs.API_URL}/profile/{Converter.gender(gender)}"
        )
        if response.status_code == 200:
            response_json = json.loads(response.text)
            if response_json["status"] == "success":
                data = response_json["data"]
                ordered_data = sorted(data, key=lambda x: x["age"], reverse=True)
                result = {i:x["img_url"] for i, x in enumerate(ordered_data)}
                logger.success(f"{response_json['message']}: {gender}")
            else:
                logger.warning(response_json["message"])
        else:
            logger.warning("🚨 API 연결에 실패했습니다.")
        
        return result
    
    # 캐릭터 생성 API 요청하는 메서드
    @staticmethod
    def create_char_api(data):
        result = False

        response = requests.post(
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

        return result