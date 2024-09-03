import streamlit as st
import websockets
import requests 
import json 
import re

from core.logger import logger
from core.config import configs
from core.utils import *

#-------------------------------------------------------------------
# Main
#-------------------------------------------------------------------
def convert_tag(text):
    text_list = text.split(",")
    add_tag = [f"#{x.strip()}" for x in text_list]
    return " ".join(add_tag)

#-------------------------------------------------------------------
# Create Character
#-------------------------------------------------------------------
def convert_gen(gender, method="en"):
    if method=="en":
        gen_values = {"남": "male", "여": "female", "기타": "other"}
    elif method=="idx":
        gen_values = {"male": 0, "female": 1, "other": 2}

    return gen_values[gender.strip()]


#-------------------------------------------------------------------
# Update Character
#-------------------------------------------------------------------
def update_char_api(data):
    response = requests.put(
        url=f"{configs.API_URL}/character",
        json=data
    )
    response_json = json.loads(response.text)

    return response_json
#-------------------------------------------------------------------
# My Character List
#-------------------------------------------------------------------
def my_character_info():
    result = {}
    response = requests.get(
        url=f"{configs.API_URL}/character/user",
        json=st.session_state["user"]
    )
    if response.status_code == 200:
        data = json.loads(response.text)["data"]
        ordered_data = sorted(data, key=lambda x: x["createDate"], reverse=True)
        result = {i:x for i, x in enumerate(ordered_data)}
    
    return result
#-------------------------------------------------------------------
# Create Chatroom
#-------------------------------------------------------------------
def create_chatroom_api(data):
    response = requests.post(
        url=f"{configs.API_URL}/chatroom",
        json=data
    )
    response_json = json.loads(response.text)

    return response_json
#-------------------------------------------------------------------
# My Chatting List
#-------------------------------------------------------------------
def get_chatting_info():
    result = {}
    response = requests.get(
        url=f"{configs.API_URL}/chatroom/user",
        json=st.session_state["user"]
    )
    if response.status_code == 200:
        data = json.loads(response.text)["data"]
        ordered_data = sorted(data, key=lambda x: x["createDate"], reverse=True)
        result = {i:x for i, x in enumerate(ordered_data)}
    
    return result
#-------------------------------------------------------------------
# Chatting
#-------------------------------------------------------------------
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
        return token 
    
def chat_reset_api():
    response = requests.get(
        url=f"{configs.API_URL}/reset",
        json=st.session_state["user"]
    )


    
def get_chat_history():
    response = requests.get(
        url=f"{configs.API_URL}/chatting/{st.session_state['chatroom_id']}"
    )
    if response.status_code == 200:
        data = json.loads(response.text)["data"]
        ordered_data = sorted(data, key=lambda x: x["createDate"])

    return ordered_data