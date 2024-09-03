import streamlit as st
import requests 
import json 

from core.logger import logger
from core.config import configs

class HomeService:
    # 모든 캐릭터를 사용 카운트 수로 정렬하여 조회
    @staticmethod
    # @st.cache_data
    def get_character_info():
        result = {}
        response = requests.get(f"{configs.API_URL}/character")
        if response.status_code == 200:
            response_json = json.loads(response.text)
            if response_json["status"] == "success":
                data = response_json["data"]
                ordered_data = sorted(data, key=lambda x: x["userCount"], reverse=True)
                result = {i:x for i, x in enumerate(ordered_data)}
                logger.success(response_json["message"])
            else:
                logger.warning(response_json["message"])

        return result
    
    @staticmethod
    def create_chatroom_api(data):
        response = requests.post(
            url=f"{configs.API_URL}/chatroom",
            json=data
        )
        if response.status_code == 200:
            response_json = json.loads(response.text)
            if response_json["status"] == "success":
                logger.success(response_json["message"])

                return response_json["data"]
            else:
                logger.warning(response_json["message"])
        else:
            logger.warning("🚨 API 연결에 실패했습니다.")
        
        return None
    
    @staticmethod
    def update_usercount_api(data):
        response = requests.put(
            url=f"{configs.API_URL}/character/count",
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

