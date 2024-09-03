import streamlit as st

from core.state import *
from core.utils import *
from core.service import convert_tag

from services.chat_list import ChatRoomService
from states.chat_list import ChatRoomClick
setting()
#-------------------------------------------------------------------
# Settings
#-------------------------------------------------------------------
# 내 캐릭터 정보 가져오기
data = ChatRoomService.get_chatting_info()
#-------------------------------------------------------------------
# My Character List
#-------------------------------------------------------------------
# 제목
st.markdown("## 💬 내 채팅 목록")
st.markdown("---")

if not data:
    st.markdown("만들어진 채팅이 없습니다.")
else:
    for key, element in data.items():
        char_data = element["character"]
        # View
        with st.container(border=True):
            col1, col2, col3 = st.columns(spec=[0.25,0.5,0.25])
            # 캐릭터 프로필
            col1.image(char_data["profile"])
            # 캐릭터 정보
            with col2:
                # 채팅방 이름
                st_textbox(element["name"])
                vertical_space(1)

                # 캐릭터 정보
                st_textbox(char_data["name"], 0.9)
                st_textbox(convert_tag(char_data["personality"]), 0.8)
                st_textbox(char_data["summary"], 0.8)
            # 채팅하기 버튼
            col3.button(
                label="채팅하기", 
                key=f"mypage_chat{key}",
                type="primary", 
                use_container_width=True, 
                on_click=ChatRoomClick.chatting,
                args=[data[key]]
            )
            # 삭제하기 버튼
            col3.button(
                label="삭제하기", 
                key=f"del_chat{key}",
                use_container_width=True, 
                on_click=ChatRoomClick.delete,
                args=[data[key]]
            )
        #-------------------------------------------------------------------
        # Script
        if st.session_state["start_chat"]:
            st.session_state["transition"] = True
            st.switch_page("pages/chatting.py")

        
        