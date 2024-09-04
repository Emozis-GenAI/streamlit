# python -m streamlit run Home.py
import streamlit as st
from st_pages import get_nav_from_toml

from core.utils import *
from core.state import *
from core.config import configs

from states.login import LoginClick

setting()

st.logo(
    image="https://i.postimg.cc/9FwDHFdd/emogi-logo.png"
)
#-------------------------------------------------------------------
# Settings
#-------------------------------------------------------------------
initialize()
if controller.get('user'):
    st.session_state["user"] = controller.get('user')
    st.session_state["login"] = True
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
        st.switch_page("pages/home.py")   
    #-------------------------------------------------------------------
    # 로그인 되어 있을 때
    if st.session_state["login"]:
        # 내 캐릭터 관리 버튼(View)
        st.button(
            label="내 캐릭터 관리",
            use_container_width=True,
            key="mypage_btn",
            on_click=LoginClick.mypage
        )
        # 내 캐릭터 관리 버튼(View)
        if st.session_state["mypage_btn"]:
            st.switch_page("pages/char_list.py")
    #-------------------------------------------------------------------
        # 로그아웃 버튼(View)
        st.button(
            label="로그아웃",
            use_container_width=True,
            key="logout_btn",
            on_click=LoginClick.logout
        )
        # 로그아웃 버튼(Script)
        if st.session_state["logout_btn"]:
            controller.remove('user')
            st.session_state["user"] = None
            st.session_state["login"] = False
            st.switch_page("pages/home.py")
    #-------------------------------------------------------------------
    # 로그인 안되어 있을 때 
    else:
        # 로그인 버튼(View)
        st.button(
            label="로그인",
            use_container_width=True,
            key="login_btn",
            on_click=LoginClick.login_window,
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
