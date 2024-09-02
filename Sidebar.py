# python -m streamlit run Home.py
import streamlit as st
from st_pages import get_nav_from_toml

from core.utils import *
from core.state import *
from core.config import configs

setting()
#-------------------------------------------------------------------
# Settings
#-------------------------------------------------------------------
initialize()
if st.session_state["transition"]:
    re_initialize()
print(st.session_state)
#-------------------------------------------------------------------
# Sidebar Button(View)
#-------------------------------------------------------------------
with st.sidebar:
    # 유저명 출력
    if st.session_state["user"]:
        user = st.session_state["user"]
        st.markdown(f"{user['username']}({user['nickname']})")
    #-----------------------------------------------------)--------------
    # HOME 버튼(View)
    st.button(
        label="HOME",
        use_container_width=True,
        key="home_btn"
    )
    # Home 버튼(Script)
    if st.session_state["home_btn"]:
        st.switch_page("pages/main.py")   
    #-------------------------------------------------------------------
    # 로그인 되어 있을 때
    if st.session_state["login"]:
        # 내 캐릭터 관리 버튼(View)
        st.button(
            label="내 캐릭터 관리",
            use_container_width=True,
            key="mypage_btn"
        )
        # 내 캐릭터 관리 버튼(View)
        if st.session_state["mypage_btn"]:
            st.session_state["mypage_view"] = "mypage"
            st.switch_page("pages/char_list.py")
    #-------------------------------------------------------------------
        # 로그아웃 버튼(View)
        st.button(
            label="로그아웃",
            use_container_width=True,
            key="logout_btn",
            on_click=logout
        )
        # 로그아웃 버튼(Script)
        if st.session_state["logout_btn"]:
            st.switch_page("pages/main.py")
    #-------------------------------------------------------------------
    # 로그인 안되어 있을 때 
    else:
        # 로그인 버튼(View)
        st.button(
            label="로그인",
            use_container_width=True,
            key="login_btn",
            on_click=login_window,
            args=["login"]
        )
        # 로그인 버튼(Script)
        if st.session_state["login_btn"]:
            st.switch_page("pages/login.py")

#-------------------------------------------------------------------
# Navication Bar
#-------------------------------------------------------------------
nav = get_nav_from_toml(".streamlit/pages.toml")
pg = st.navigation(nav, position="hidden")
pg.run()
