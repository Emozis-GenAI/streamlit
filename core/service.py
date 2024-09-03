import streamlit as st
import websockets
import requests 
import json 
import re

from core.logger import logger
from core.config import configs
from core.utils import *
#-------------------------------------------------------------------
# Login
#-------------------------------------------------------------------
def validate_login(data):
    length_condition = {"username": 4, "nickname": 1, "password": 4}
    regex_condition = {
        "username": {"regex": r"^[A-Za-z0-9]+$", "description": "영문, 숫자만 가능합니다."},
        "nickname": {"regex": r"^[가-힣A-Za-z0-9]+$", "description": "한글, 영문, 숫자만 가능합니다."},
        "password": {"regex": r"^[A-Za-z0-9!@#$]+$", "description": "영문, 숫자, 특수문자(!,@,#,$)만 가능합니다."}
    }

    for key, value in data.items():
        if len(value) < length_condition[key]:
            return f"{key} Error: {length_condition[key]}자 이상 입력해야 합니다."
        
        if not re.fullmatch(regex_condition[key]["regex"], value):
            return f"{key} Error: {regex_condition[key]['description']}"
        
    return True

def register_api(data):
    response = requests.post(
        url=f"{configs.API_URL}/user/register",
        json=data
    )
    response_json = json.loads(response.text)

    return response_json

def login_api(data):
    response = requests.post(
        url=f"{configs.API_URL}/user/login",
        json=data
    )
    response_json = json.loads(response.text)

    return response_json
#-------------------------------------------------------------------
# Main
#-------------------------------------------------------------------
def get_character_info():
    result = {}
    response = requests.get(f"{configs.API_URL}/character")
    if response.status_code == 200:
        data = json.loads(response.text)["data"]
        ordered_data = sorted(data, key=lambda x: x["userCount"], reverse=True)
        result = {i:x for i, x in enumerate(ordered_data)}
    
    return result

def convert_tag(text):
    text_list = text.split(",")
    add_tag = [f"#{x.strip()}" for x in text_list]
    return " ".join(add_tag)

#-------------------------------------------------------------------
# Create Character
#-------------------------------------------------------------------
def create_char_api(data):
    response = requests.post(
        url=f"{configs.API_URL}/character",
        json=data
    )
    if response.status_code == 200:
        response_json = json.loads(response.text)
    else:
        logger.warning("🚨 API 연결에 실패했습니다.")

    return response_json

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
def make_form(data):
    vertical_space(1)
    columns = st.columns(spec=[0.25,0.5,0.25])
    with columns[1]:
        st.image(data["profile"])
    st.markdown(f"[이름] {data['name']}")
    st.markdown(f"[관계] {convert_tag(data['relationship'])}")
    st.markdown(f"[성격] {convert_tag(data['personality'])}")
    st.markdown(f"[상세설명]<br> {data['summary']}", unsafe_allow_html=True)

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

def print_and_save_chat(role, content):
    if role == "assistant":
        profile = st.session_state["character_data"]["profile"]
    else:
        profile = st.session_state["myprofile"]
    # 출력
    st.chat_message("assistant", avatar=profile).markdown(content)
    # streamlit 메모리 저장
    st.session_state["chat_history"].append(
        {"role": role, "content": content}
    )
    # DB 저장
    if st.session_state["login"]:
        data = {
            "chatroom_id": st.session_state["chatroom_id"],
            "user": st.session_state["user"],
            "role": role,
            "content": content
        }
        response = requests.post(
            url=f"{configs.API_URL}/chatting",
            json=data
        ) 
        response_json = json.loads(response.text)

        return response_json
    
def get_chat_history():
    result = {}
    response = requests.get(
        url=f"{configs.API_URL}/chatting/{st.session_state['chatroom_id']}"
    )
    if response.status_code == 200:
        data = json.loads(response.text)["data"]
        ordered_data = sorted(data, key=lambda x: x["createDate"])
    
    return ordered_data