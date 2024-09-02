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
        st.switch_page("pages/create_char.py")
    else:
        popup()
        
# 캐릭터 생성 화면 전환
elif st.session_state["header_btn"] == 1:
    if st.session_state["login"]:
        st.switch_page("pages/create_char.py")
    else:
        popup()
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
                on_click=start_chat,
                args=[data[key]])

# #-------------------------------------------------------------------
# # Settings
# #-------------------------------------------------------------------
# def start_chat(data):
#     st.session_state["chat_character"] = data
#     st.session_state["chat_start"] = True

#     try:
#         del st.session_state["demo_chain"]
#         del st.session_state["demo_memory"]
#         del st.session_state["demo_history"]
#     except:
#         pass

# @st.dialog("⚠ 로그인")
# def popup():
#     st.markdown("로그인 해야 할 수 있는 기능입니다.")
#     _, col = st.columns(spec=[0.7, 0.3])
#     login_btn = col.button("로그인", use_container_width=True)
#     if login_btn:
#         st.switch_page("pages/login.py")

# if "chat_start" not in st.session_state:
#     st.session_state["chat_start"] = False
# elif st.session_state["chat_start"]:
#     st.switch_page("pages/page4.py")

# try:
#     if st.session_state["header_btn"] == 0:
#         if st.session_state["user"] == "":
#             popup()
#         else:
#             st.switch_page("pages/page2.py")
#     elif st.session_state["header_btn"] == 1:
#         if st.session_state["user"] == "":
#             popup()
#         else:
#             st.switch_page("pages/page3.py")
# except Exception as e:
#     print(e)
#     st.session_state["header_btn"] = None

# img_url1 = "https://i.postimg.cc/XJ9gFk48/openart-image-CKz-Cdiz-L-1724052914963-raw.jpg"
# img_url2 = "https://i.postimg.cc/nLp3chKc/2-1.png"

# #-------------------------------------------------------------------
# # Header
# #-------------------------------------------------------------------
# st.markdown("### 메인 페이지")

# columns = st.columns(spec=[0.1,0.8,0.1])
# with columns[1]:
#     image_select(
#         label="", 
#         images=[img_url1, img_url2], 
#         captions=["내 채팅 목록", "캐릭터 생성"],
#         return_value="index", 
#         key="header_btn")
# # columns = st.columns(spec=[0.1,0.4,0.4,0.1])
# # with columns[1]:
# #     chat_list_btn = image_select(
# #         label="채팅 목록", 
# #         images=[img_url1], 
# #         return_value="index", 
# #         key="chat_list_btn"
# #     )
# # with columns[2]:
# #     create_chat_btn = image_select(
# #         label="캐릭터 생성", 
# #         images=[img_url2], 
# #         return_value="index", 
# #         key="create_chat_btn"
# #     )

# #-------------------------------------------------------------------
# # Ranking
# #-------------------------------------------------------------------
# st.markdown("### 랭킹")

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

# # 2행의 열 구성: 각 행에 4개의 열을 생성
# cols = st.columns(3)

# # 각 열에 버튼 추가
# for key, element in data.items():
#     # i % 4는 현재 버튼이 어떤 열에 속하는지를 결정합니다 (0부터 3까지의 인덱스)
#     col = cols[key % 3]
    
#     with col:
#         with st.container(border=True, height=340):
#             st.image(element["profile"])
#             custom_text(element["name"], 0.9)
#             custom_text(element["personality"], 0.9)
#             st.button(
#                 label="채팅하기", 
#                 key=f"rank{key}", 
#                 use_container_width=True, 
#                 on_click=start_chat,
#                 args=[data[key]])
