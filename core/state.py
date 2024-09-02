import streamlit as st 

from core.config import configs
from core.service import convert_tag, create_chatroom_api, make_form
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
def re_initialize(states):
    for state in states:
        st.session_state[state] = configs.dictionary[state]

#-------------------------------------------------------------------
# On Click Event
#-------------------------------------------------------------------
# Sidebar
## 내 캐릭터 관리 클릭
def mypage():
    st.session_state["mypage_view"] = "mypage"

# 로그아웃 클릭
def logout():
    st.session_state["user"] = None

## 로그인 클릭
def login_window(window):
    st.session_state["login_window"] = window
#-------------------------------------------------------------------
# Main
## 로그인 팝업창
@st.dialog("⚠ 로그인")
def login_popup():
    st.markdown("로그인 해야 할 수 있는 기능입니다.")
    _, col = st.columns(spec=[0.7, 0.3])
    login_btn = col.button("로그인", use_container_width=True)
    if login_btn:
        st.switch_page("pages/login.py")

## 채팅방 생성 팝업창
@st.dialog("⭐ 채팅방 생성")
def chatroom_popup():
    st.text_input(
        label="채팅방 이름", 
        max_chars=15, 
        placeholder="채팅방 이름을 입력하세요(15자 이내)",
        key="chatroom_name"
    )
    st.session_state["chatroom_title"] = st.session_state["chatroom_name"]
    data = st.session_state["character_data"]
    make_form(data)

    st.button(
        label="채팅 시작하기",
        use_container_width=True,
        type="primary",
        key="start_chat_btn"
    )

    if st.session_state["start_chat_btn"]:
        insert_data = {
            "name": st.session_state["chatroom_name"],
            "character": data,
            "user": st.session_state["user"]
        }
        # 로그인 되어 있을 때만 데이터 전송
        if st.session_state["login"]:
            response = create_chatroom_api(insert_data)
            if response["status"] == "success":
                st.session_state["chatroom_id"] = response["data"]
                st.switch_page("pages/chatting.py")
            else:
                st.error(response["message"])
        else:
            st.switch_page("pages/chatting.py")
        
    
## 랭킹에 있는 채팅하기 클릭
def chatroom(data):
    st.session_state["character_data"] = data
    chatroom_popup()

## 내 채팅 목록에 있는 채팅하기 클릭
def chatting(data):
    st.session_state["character_data"] = data
    st.session_state["start_chat"] = True

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