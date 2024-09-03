import streamlit as st 

class CreateCharClick:
    @staticmethod
    ## 프로필 사진 클릭
    def change_img(data):
        idx = st.session_state["char_img"]
        st.session_state["select_img"] = data[idx]