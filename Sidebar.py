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
# 초기 변수 세팅
def initialize(dictionary):
    for key, value in dictionary.items():
        if key not in st.session_state:
            st.session_state[key] = value

initialize(configs.dictionary)
#-------------------------------------------------------------------
# Sidebar Button(View)
#-------------------------------------------------------------------
with st.sidebar:
    # HOME 버튼
    st.button(
        label="HOME",
        use_container_width=True,
        key="home_btn"
    )
    # 로그인 버튼
    st.button(
        label="로그인",
        use_container_width=True,
        key="login_btn",
        on_click=login_window,
        args=["login"]
    )
#-------------------------------------------------------------------
# Sidebar Button(Script)
#-------------------------------------------------------------------
# Home 버튼 누를 때 
if st.session_state["home_btn"]:
    st.switch_page("pages/main.py")

# 로그인 버튼 누를 때 
if st.session_state["login_btn"]:
    st.switch_page("pages/login.py")
#-------------------------------------------------------------------
# Navication Bar
#-------------------------------------------------------------------
nav = get_nav_from_toml(".streamlit/pages.toml")
pg = st.navigation(nav, position="hidden")
pg.run()
