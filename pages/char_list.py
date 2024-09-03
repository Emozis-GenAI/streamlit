import streamlit as st
from streamlit_image_select import image_select
from streamlit_tags import st_tags

from core.state import *
from core.utils import *
from core.service import my_character_info, convert_tag

from states.char_list import CharListClick
from states.home import HomeClick

from services.converter import converter 
from services.char_list import CharListService 
setting()
#-------------------------------------------------------------------
# Settings
#-------------------------------------------------------------------
# 내 캐릭터 정보 가져오기
data = CharListService.my_character_info()
# print(data)
#-------------------------------------------------------------------
# My Character List
#-------------------------------------------------------------------
# 제목
st.markdown("## 🛠️ 내 캐릭터 관리")
st.markdown("---")

if not data:
    st.markdown("만들어진 캐릭터가 없습니다.")

for key, element in data.items():
    # View
    with st.container(border=True):
        col1, col2, col3 = st.columns(spec=[0.25,0.5,0.25])
        # 캐릭터 프로필
        col1.image(element["profile"])
        # 캐릭터 정보
        with col2:
            st_textbox(element["name"], 0.9)
            vertical_space(1)
            st_textbox(converter.tag(element["personality"]), 0.8)
            st_textbox(element["summary"], 0.8)
        # 채팅하기 버튼
        col3.button(
            label="채팅하기", 
            key=f"mypage_chat{key}",
            type="primary", 
            use_container_width=True, 
            on_click=HomeClick.chatroom,
            args=[data[key]]
        )
        # 수정하기 버튼
        col3.button(
            label="수정하기", 
            key=f"mypage_mod{key}",
            use_container_width=True, 
            on_click=CharListClick.modify_character,
            args=[data[key]]
        )
        # 수정하기 버튼
        col3.button(
            label="삭제하기", 
            key=f"mypage_del{key}",
            use_container_width=True, 
            on_click=CharListClick.delete_character,
            args=[data[key]]
        )
    #-------------------------------------------------------------------
    # Script
    if st.session_state["delete_character"]:
        CharListService.del_character(st.session_state["character_data"])
        st.session_state["delete_character"] = False
        st.switch_page("pages/char_list.py")

    if st.session_state["mypage_view"] == "modify":
        st.switch_page("pages/modify_char.py")
