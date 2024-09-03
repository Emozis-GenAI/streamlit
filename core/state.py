import streamlit as st 

from core.config import configs
from core.service import *
#-------------------------------------------------------------------
# Settings
#-------------------------------------------------------------------
# 초기 변수 세팅
def initialize():
    for key, value in configs.dictionary.items():
        if key not in st.session_state:
            if value == "None":
                st.session_state[key] = None
            else:
                st.session_state[key] = value

# 재 초기화
# def re_initialize(states):
#     for state in states:
#         st.session_state[state] = configs.dictionary[state]
def custom_init(keys):
    if st.session_state["transition"]:
        for key in keys:
            st.session_state[key] = configs.dictionary[key]
    st.session_state["transition"] = False

#-------------------------------------------------------------------
# Main

    


## 내 채팅 목록에 있는 채팅하기 클릭
def chatting(data):
    chat_reset_api()
    st.session_state["chat_history"] = ChatService.get_chat_history()
    st.session_state["chatroom_data"] = data
    st.session_state["chatroom_title"] = data["name"]
    st.session_state["character_data"] = data["character"]
    st.session_state["chatroom_id"] = data["_id"]
    st.session_state["start_chat"] = True
    st.session_state["new_chat"] = False
    

#-------------------------------------------------------------------
# Create Character
## 프로필 사진 클릭
def change_img(data):
    idx = st.session_state["char_img"]
    st.session_state["select_img"] = data[idx]
#-------------------------------------------------------------------
# Modify Character
## 수정하기 버튼
def modify_character(data):
    st.session_state["modify_data"] = data
    st.session_state["select_img"] = data["profile"]
    st.session_state["mypage_view"] = "modify"