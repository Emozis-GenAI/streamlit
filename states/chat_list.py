import streamlit as st 

from services.chatting import ChatService

class ChatRoomClick:
    @staticmethod
    def chatting(data):
        ChatService.chat_reset_api()
        st.session_state["chatroom_data"] = data
        st.session_state["chat_history"] = ChatService.get_chat_history()
        st.session_state["start_chat"] = True
        st.session_state["new_chat"] = False