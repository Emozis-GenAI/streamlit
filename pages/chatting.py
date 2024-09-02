import streamlit as st
import asyncio

from core.state import *
from core.utils import *
from core.service import make_form, send_recieve_chat, print_and_save_chat

setting()
#-------------------------------------------------------------------
# Setting
#-------------------------------------------------------------------
# 채팅목록에서 페이지 채팅방으로 자동으로 넘어가는거 방지
st.session_state["start_chat"] = False

# 데이터 불러오기
data = st.session_state["character_data"]
profile = data["profile"]
#-------------------------------------------------------------------
# Sidebar
#-------------------------------------------------------------------
with st.sidebar:
    # 사이드바 정보 출력
    st.markdown("---")
    st_textbox(st.session_state["chatroom_title"], align="center")
    make_form(data)
#-------------------------------------------------------------------
# Chatting
#-------------------------------------------------------------------
# 뒤로 가기 버튼
st.button(
    label="뒤로가기", 
    key=f"back_btn",
)

# 로그인 안했을 때
if not st.session_state["login"]:
    st_textbox("⚠ 로그인을 하지 않으면 대화 내용은 저장되지 않습니다.")

vertical_space(1)
print("HISTORY", st.session_state["chat_history"])
# 채팅 첫 시작일 때
if not len(st.session_state["chat_history"]):
    greeting = data["greeting"]
    print_and_save_chat(role="assistant", content=greeting)
    # st.chat_message("assistant",avatar=profile).markdown(greeting)
    # st.session_state["chat_history"].append(
    #     {"role":"assistant", "content": greeting}
    # )
# 채팅 기록이 있을 때
else:
    for chat in st.session_state["chat_history"]:
        if chat["role"] == "assistant":
            profile = st.session_state["character_data"]["profile"]
        else:
            profile = st.session_state["myprofile"]
        st.chat_message(chat["role"], avatar=profile).markdown(chat["content"])

# 채팅창 입력
request = st.chat_input(placeholder="Message...")

# 입력 받으면 전송
if request:
    # 입력된 채팅 출력 및 저장
    print_and_save_chat(role="user", content=request)
    # st.chat_message("user").markdown(request)
    # st.session_state["chat_history"].append(
    #     {"role":"user", "content":request}
    # )

    async def main():
        with st.chat_message("assistant"):
            container = st.empty()
            data = {
                "user": st.session_state["user"],
                "character": st.session_state["character_data"],
                "request": request
            }
            response = await send_recieve_chat(data, container)
            # print("RESPONSE", response)

        st.session_state["chat_history"].append(
            {"role":"assistant", "content":response}
        )
    
    asyncio.run(main())
#-------------------------------------------------------------------
# Script
#-------------------------------------------------------------------
if st.session_state["back_btn"]:
    re_initialize(["chat_history"])
    if st.session_state["login"]:
        st.switch_page("pages/chat_list.py")
    else:
        st.switch_page("pages/main.py")
