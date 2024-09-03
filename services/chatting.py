import streamlit as st
import websockets
import requests 
import json

from core.logger import logger
from core.config import configs

class ChatService:
    @staticmethod
    # @st.cache_data
    def get_chat_history():

        chatroom_data = st.session_state["chatroom_data"]
        sub_data = {
            "id": chatroom_data["_id"],
            "name": chatroom_data["name"] 
        }
        response = requests.get(
            url=f"{configs.API_URL}/chatting/chatroom",
            json=sub_data
        )
        if response.status_code == 200:
            response_json = json.loads(response.text)
            if response_json["status"] == "success":
                data = json.loads(response.text)["data"]
                ordered_data = sorted(data, key=lambda x: x["createDate"])
                logger.success(response_json["message"])

                return ordered_data
            else:
                logger.warning(response_json["message"])
        else:
            logger.warning("🚨 API 연결에 실패했습니다.")
        
        return []
    
    @staticmethod
    def send_chat_api(role, content):
        result = False 

        chatroom_data = st.session_state["chatroom_data"]

        sub_data = {
            "id": chatroom_data["_id"],
            "name": chatroom_data["name"] 
        }
        data = {
            "chatroom": sub_data,
            "role": role,
            "content": content,
        }

        response = requests.post(
            url=f"{configs.API_URL}/chatting",
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


    @staticmethod 
    async def send_recieve_chat(data, container):
        async with websockets.connect(configs.SOCKET_URL) as websocket:
            send_data = json.dumps(data)
            await websocket.send(send_data)
            token = ""
            while True:
                response = await websocket.recv()

                if response == "[EOS]":
                    break
            
                token += response 
                container.markdown(token)
            logger.success("✅ Success Response AI Message")
            return token 

    @staticmethod
    def chat_reset_api():
        response = requests.get(
            url=f"{configs.API_URL}/reset",
            json=st.session_state["user"]
        )
        if response.status_code == 200:
            response_json = json.loads(response.text)
            if response_json["status"] == "success":
                logger.success(f"{response_json['message']}")
            else:
                logger.warning(response_json["message"])