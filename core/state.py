import streamlit as st 

from core.config import configs
print(configs.dictionary)
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
    # states = ["header_btn", "transition", "select_img"]
    for state in states:
        st.session_state[state] = configs.dictionary[state]

# 화면 바뀔때마다 초기화되어야 하는 것들: char_img

#-------------------------------------------------------------------
# On Click Event
#-------------------------------------------------------------------
# 로그인
## 윈도우 화면 전환
def login_window(window):
    st.session_state["login_window"] = window

## 로그아웃
def logout():
    st.session_state["login"] = False
    st.session_state["user"] = None

## 로그인 팝업창
@st.dialog("⚠ 로그인")
def popup():
    st.markdown("로그인 해야 할 수 있는 기능입니다.")
    _, col = st.columns(spec=[0.7, 0.3])
    login_btn = col.button("로그인", use_container_width=True)
    if login_btn:
        st.switch_page("pages/login.py")

# 메인, 채팅 목록, 내 캐릭터 관리
## 채팅창 이동 시 데이터 저장
def start_chat(data):
    st.session_state["character_data"] = data
    st.session_state["chat_start"] = True

# 캐릭터 생성
## 프로필 사진 선택
def change_img(data):
    idx = st.session_state["char_img"]
    st.session_state["select_img"] = data[idx]

# 내 캐릭터 목록
## 수정하기 버튼
def modify_character(data):
    st.session_state["modify_data"] = data
    st.session_state["select_img"] = data["profile"]
    st.session_state["mypage_view"] = "modify"