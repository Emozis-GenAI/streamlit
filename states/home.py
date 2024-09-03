import streamlit as st 

from services.converter import converter
from services.home import HomeService 
from services.chatting import ChatService

class HomePopup:
    ## 로그인 팝업창
    @staticmethod
    @st.dialog("⚠ 로그인")
    def login_popup():
        st.markdown("로그인 해야 할 수 있는 기능입니다.")
        _, col = st.columns(spec=[0.7, 0.3])
        login_btn = col.button("로그인", use_container_width=True)
        if login_btn:
            st.session_state["transition"] = True
            st.switch_page("pages/login.py")

    # 채팅방 생성 팝업창
    @staticmethod
    @st.dialog("⭐ 채팅방 생성")
    def chatroom_popup():
        st.text_input(
            label="채팅방 이름", 
            max_chars=15, 
            placeholder="채팅방 이름을 입력하세요(15자 이내)",
            key="chatroom_name"
        )
        st.session_state["chatroom_title"] = st.session_state["chatroom_name"]

        # 데이터 불러오기
        data = st.session_state["character_data"]
        converter.make_form(data)

        # 채팅 시작하기 버튼
        st.button(
            label="채팅 시작하기",
            use_container_width=True,
            type="primary",
            key="start_chat_btn"
        )

        # Script
        if st.session_state["start_chat_btn"]:
            if not len(st.session_state["chatroom_name"]):
                st.error("🚨 채팅방 이름을 1자 이상 입력해야 합니다.")
            else:
                insert_data = {
                    "name": st.session_state["chatroom_name"],
                    "character": data,
                    "user": st.session_state["user"]
                }
                # 로그인 되어 있을 때만 데이터 전송
                if st.session_state["login"]:
                    chatroom_id = HomeService.create_chatroom_api(insert_data)
                    if chatroom_id:
                        st.session_state["chatroom_data"] = {
                            "_id": chatroom_id,
                            "name": st.session_state["chatroom_name"]
                        }
                ChatService.chat_reset_api()

                # 캐릭터 조회 수 반영
                insert_data = {
                    "id": data["_id"],
                    "userCount": data["userCount"] + 1
                }
                HomeService.update_usercount_api(insert_data)
                

                # 화면 전환
                st.session_state["character_data"] = data
                st.session_state["transition"] = True 
                st.session_state["new_chat"] = True 
                st.session_state["chat_history"] = []      
                st.switch_page("pages/chatting.py")


class HomeClick:
    ## 랭킹에 있는 채팅하기 클릭
    @staticmethod
    def chatroom(data):
        st.session_state["character_data"] = data
        HomePopup.chatroom_popup()
