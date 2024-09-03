import streamlit as st
import requests 
import json 

from core.logger import logger
from core.config import configs

class ChatRoomService:
    @staticmethod
    # @st.cache_data
    def get_chatting_info():
        result = {}
        response = requests.get(
            url=f"{configs.API_URL}/chatroom/user",
            json=st.session_state["user"]
        )
        if response.status_code == 200:
            response_json = json.loads(response.text)
            if response_json["status"] == "success":
                data = response_json["data"]
                ordered_data = sorted(data, key=lambda x: x["createDate"], reverse=True)
                result = {i:x for i, x in enumerate(ordered_data)}
                logger.success(response_json["message"])
            else:
                logger.warning(response_json["message"])

        return result
    
    @staticmethod
    def del_chatroom(data):
        result = False

        response = requests.delete(
            url=f"{configs.API_URL}/chatroom/{data['_id']}"
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