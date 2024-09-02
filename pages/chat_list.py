import streamlit as st

from core.state import *
from core.utils import *
from core.service import get_chatting_info, convert_tag
setting()
#-------------------------------------------------------------------
# Settings
#-------------------------------------------------------------------
# 내 캐릭터 정보 가져오기
data = get_chatting_info()
#-------------------------------------------------------------------
# My Character List
#-------------------------------------------------------------------
# 제목
st.markdown("## 💬 내 채팅 목록")

for key, element in data.items():
    char_data = element["character"]
    # View
    with st.container(border=True):
        col1, col2, col3 = st.columns(spec=[0.2,0.6,0.2])
        # 캐릭터 프로필
        col1.image(char_data["profile"])
        # 캐릭터 정보
        with col2:
            st_textbox(char_data["name"], 0.9)
            vertical_space(1)
            st_textbox(convert_tag(char_data["personality"]), 0.9)
            st_textbox(char_data["summary"], 0.9)
        # 채팅하기 버튼
        col3.button(
            label="채팅하기", 
            key=f"mypage_chat{key}",
            type="primary", 
            use_container_width=True, 
            on_click=chatting,
            args=[data[key]["character"]]
        )
    #-------------------------------------------------------------------
    # Script
    if st.session_state["start_chat"]:
        st.switch_page("pages/chatting.py")
    