import streamlit as st
from streamlit_image_select import image_select
from streamlit_tags import st_tags

from core.state import *
from core.utils import *
from core.service import my_character_info, convert_tag
setting()
#-------------------------------------------------------------------
# Settings
#-------------------------------------------------------------------
# 내 캐릭터 정보 가져오기
data = my_character_info()
# print(data)
#-------------------------------------------------------------------
# My Character List
#-------------------------------------------------------------------
# 제목
st.markdown("## 🛠️ 내 캐릭터 관리")

for key, element in data.items():
    # View
    with st.container(border=True):
        col1, col2, col3 = st.columns(spec=[0.2,0.6,0.2])
        # 캐릭터 프로필
        col1.image(element["profile"])
        # 캐릭터 정보
        with col2:
            st_textbox(element["name"], 0.9)
            vertical_space(1)
            st_textbox(convert_tag(element["personality"]), 0.9)
            st_textbox(element["summary"], 0.9)
        # 수정하기 버튼
        col3.button(
            label="수정하기", 
            key=f"mypage_mod{key}",
            use_container_width=True, 
            on_click=modify_character,
            args=[data[key]]
        )
        # 채팅하기 버튼
        col3.button(
            label="채팅하기", 
            key=f"mypage_chat{key}",
            type="primary", 
            use_container_width=True, 
            on_click=chatroom,
            args=[data[key]]
        )
    #-------------------------------------------------------------------
    # Script
    if st.session_state["mypage_view"] == "modify":
        st.switch_page("pages/modify_char.py")
# def start_chat(data):
#     st.session_state["chat_character"] = data
#     st.session_state["chat_start"] = True

#     try:
#         del st.session_state["demo_chain"]
#         del st.session_state["demo_memory"]
#         del st.session_state["demo_history"]
#     except:
#         pass

# if "chat_start" not in st.session_state:
#     st.session_state["chat_start"] = False
# elif st.session_state["chat_start"]:
#     st.switch_page("pages/page4.py")

# img_url1 = "https://i.postimg.cc/XJ9gFk48/openart-image-CKz-Cdiz-L-1724052914963-raw.jpg"
# img_url2 = "https://i.postimg.cc/nLp3chKc/2-1.png"
# #-------------------------------------------------------------------
# # 내 채팅목록
# #-------------------------------------------------------------------
# st.markdown("### 내 캐릭터 관리")

# import requests 
# import json 
# from core.database import mongo
# data = {}
# url = "http://172.16.2.10:8000/character"
# response = requests.get(url)
# if response.status_code == 200:
#     data = {i:x for i, x in enumerate(json.loads(response.text)["data"],1)}
# # else:        
# # collection = mongo.connect_collection("character")
# # data = {}
# # for i, element in enumerate(collection.find(),1):
# #     element["_id"] = str(element["_id"])
# #     data[i] = element

# for key, element in data.items():
#     with st.container(border=True):
#         col1, col2, col3 = st.columns(spec=[0.2,0.6,0.2])
#         col1.image(element["profile"])
#         with col2:
#             custom_text(element["name"], 0.9)
#             custom_text(element["personality"], 0.9)
#         col3.button(
#             label="수정하기", 
#             key=f"mypage-mod{key}",
#             use_container_width=True, 
#             args=[data[key]]
#         )
#         col3.button(
#             label="채팅하기", 
#             key=f"mypage-chat{key}",
#             type="primary", 
#             use_container_width=True, 
#             on_click=start_chat,
#             args=[data[key]]
#         )