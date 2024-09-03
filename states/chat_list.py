import streamlit as st 

from services.chatting import ChatService
from services.chat_list import ChatRoomService

class ChatRoomPopup:
    @staticmethod
    @st.dialog("⚠ 삭제")
    def delete():
        st.markdown("채팅 안의 기록이 모두 삭제됩니다. 그래도 삭제하시겠습니까?")
        _, col = st.columns(spec=[0.7, 0.3])
        okay_btn = col.button("OK", use_container_width=True)
        if okay_btn:
            ChatRoomService.del_chatroom(st.session_state["chatroom_data"])
            st.session_state["transition"] = True
            st.switch_page("pages/chat_list.py")

class ChatRoomClick:
    @staticmethod
    def chatting(data):
        ChatService.reset_model_api()
        st.session_state["chatroom_data"] = data
        st.session_state["chat_history"] = ChatService.get_chat_history()
        st.session_state["start_chat"] = True
        st.session_state["new_chat"] = False
    
    @staticmethod
    def delete(data):
        st.session_state["chatroom_data"] = data
        ChatRoomPopup.delete()
        
    
    
