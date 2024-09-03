import streamlit as st 

class CharListClick:
    @staticmethod
    def modify_character(data):
        st.session_state["modify_data"] = data
        st.session_state["select_img"] = data["profile"]
        st.session_state["mypage_view"] = "modify"
    
    @staticmethod
    def delete_character(data):
        st.session_state["delete_character"] = True
        st.session_state["character_data"] = data