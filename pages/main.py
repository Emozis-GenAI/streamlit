import streamlit as st
import requests
import json
from streamlit_image_select import image_select

from core.config import configs
from core.state import *
from core.service import get_character_info, convert_tag
from core.utils import *

setting()
#-------------------------------------------------------------------
# Settings
#-------------------------------------------------------------------
# 캐릭터 정보 가져오기
data = get_character_info()
#-------------------------------------------------------------------
# Header(View)
#-------------------------------------------------------------------
# 내 채팅 목록, 캐릭터 생성 버튼
columns = st.columns(spec=[0.1,0.8,0.1])
with columns[1]:
    image_select(
        label="", 
        images=[configs.CHATLIST_IMG_URL, configs.CREATECHAR_IMG_URL], 
        use_container_width=True,
        captions=["내 채팅 목록", "캐릭터 생성"],
        return_value="index", 
        key="header_btn")
#-------------------------------------------------------------------
# Header(Script)
#-------------------------------------------------------------------
# 내 채팅 목록 화면 전환
if st.session_state["header_btn"] == 0:
    if st.session_state["login"]:
        st.switch_page("pages/chat_list.py")
    else:
        login_popup()
        
# 캐릭터 생성 화면 전환
elif st.session_state["header_btn"] == 1:
    if st.session_state["login"]:
        st.session_state["transition"] = True
        st.switch_page("pages/create_char.py")
    else:
        login_popup()
#-------------------------------------------------------------------
# Rangking
#-------------------------------------------------------------------
# 제목
st.markdown("---")
st.markdown("## 👑 랭킹순")

cols = st.columns(3)

# 각 열에 버튼 추가
for key, element in data.items():
    col = cols[key % 3]  
    with col:
        with st.container(border=True, height=350):
            # 이미지 삽입
            st.image(element["profile"])
            # 내용 설명
            st_textbox(element["name"], fontsize=0.9)
            st_textbox(convert_tag(element["personality"]), fontsize=0.9)
            vertical_space(2)
            # 채팅하기 버튼
            st.button(
                label="채팅하기", 
                key=f"rank{key}", 
                use_container_width=True, 
                on_click=chatroom,
                args=[data[key]])

# if st.session_state["chat_start"]:
    # st.switch_page("pages/chatting.py")

