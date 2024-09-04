import streamlit as st
import asyncio

from core.state import *
from core.utils import st_chat_message

from services.converter import converter
from services.chatting import ChatService


setting()

# 상태 초기화
custom_init(["start_chat"])
#-------------------------------------------------------------------
# Setting
#-------------------------------------------------------------------
# 데이터 불러오기
if st.session_state["new_chat"]:
    char_data = st.session_state["character_data"]

else:
    data = st.session_state["chatroom_data"]
    # print(data.keys())
    char_data = data["character"]

st.session_state["char_profile"] = char_data["profile"]

#-------------------------------------------------------------------
# Sidebar
#-------------------------------------------------------------------
with st.sidebar:
    # 사이드바 정보 출력
    st.markdown("---")
    st_textbox(st.session_state["chatroom_title"], align="center")
    converter.make_form(char_data)
#-------------------------------------------------------------------
# Chatting
#-------------------------------------------------------------------
# 뒤로 가기 버튼
st.button(
    label="뒤로가기", 
    key=f"back_btn",
)

if st.session_state["back_btn"]:
    if st.session_state["login"]:
        st.session_state["transition"] = True
        st.switch_page("pages/chat_list.py")
    else:
        st.session_state["transition"] = True
        st.switch_page("pages/home.py")

# 로그인 안했을 때
if not st.session_state["login"]:
    st_textbox("⚠ 로그인을 하지 않으면 대화 내용은 저장되지 않습니다.")

vertical_space(1)
#-------------------------------------------------------------------
# 새로운 채팅일 때
if len(st.session_state["chat_history"]) == 0:
    st_chat_message("assistant", char_data["greeting"])
    ChatService.send_chat_api("assistant",char_data["greeting"])

# 채팅 기록이 있을 때
else:
    # print(st.session_state["chat_history"])
    for chat in st.session_state["chat_history"]:
        st_chat_message(chat["role"], chat["content"], save=False)
#-------------------------------------------------------------------
# 채팅창 입력
request = st.chat_input(placeholder="Message...")
#-------------------------------------------------------------------
# 입력 받으면 전송
if request:
    # 입력된 채팅 출력 및 저장
    st_chat_message("user", request)
    ChatService.send_chat_api("user", request)

    # 응답 받기
    async def main():
        with st.chat_message("assistant", avatar=st.session_state["char_profile"]):
            container = st.empty()
            data = {
                "user": st.session_state["user"],
                "character": st.session_state["character_data"],
                "request": request
            }
            response = await send_recieve_chat(data, container)

        # 상태 히스토리 저장
        st.session_state["chat_history"].append(
            {
                "role": "assistant",
                "content": response
            }
        )
        # DB 저장 
        ChatService.send_chat_api("assistant", response)
    
    asyncio.run(main())
