import streamlit as st
import requests 
import json 
import re

from core.config import configs
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
    print(response.text)
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
def create_api(data):
    response = requests.post(
        url=f"{configs.API_URL}/character",
        json=data
    )
    response_json = json.loads(response.text)

    return response_json

def convert_gen(gender, method="en"):
    if method=="en":
        gen_values = {"남": "male", "여": "female", "기타": "other"}
    elif method=="idx":
        gen_values = {"male": 0, "female": 1, "other": 2}

    return gen_values[gender.strip()]

def get_profile(gender):
    result = {}
    response = requests.get(f"{configs.API_URL}/profile/{convert_gen(gender)}")
    if response.status_code == 200:
        data = json.loads(response.text)["data"]
        ordered_data = sorted(data, key=lambda x: x["age"])
        result = {i:x["img_url"] for i, x in enumerate(ordered_data)}
    
    return result
#-------------------------------------------------------------------
# Update Character
#-------------------------------------------------------------------
def update_api(data):
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