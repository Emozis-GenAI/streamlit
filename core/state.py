import streamlit as st 

from core.config import configs
from core.service import *
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
# def re_initialize(states):
#     for state in states:
#         st.session_state[state] = configs.dictionary[state]
def custom_init(keys):
    if st.session_state["transition"]:
        for key in keys:
            st.session_state[key] = configs.dictionary[key]
    print("화면전환시 초기화")
    st.session_state["transition"] = False