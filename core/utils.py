import streamlit as st
from pathlib import Path 
from dotenv import load_dotenv 

def setting():
    load_dotenv()
    read_mdfile("./static/css/css.md")

def read_mdfile(filepath:str) -> st.markdown:
    """markdown 파일을 읽고 markdown으로 작성하는 함수

    Args:
        filepath (str): markdown 파일 경로

    Returns:
        str: markdown 파일에서 추출된 텍스트
    """
    file = Path(filepath)
    
    if not file.is_file():
        file_text = f"[ERROR] 파일 경로를 찾을 수 없습니다.(INPUT PATH: {filepath})"
    else:
        file_text = file.read_text(encoding="utf-8")

    return st.markdown(file_text, unsafe_allow_html=True)

def vertical_space(size:int):
    """Create vertical blank spaces

    Args:
        size (int): height
    """
    st.container(height=size, border=False)

def st_textbox(text, fontsize=1, style=None, align="left"):
    font_css = f"font-size:{fontsize}rem; text-align:{align}"
    if style=="list":
        html = f"<li style='{font_css} margin-left: 2px;'>{text}</li>"
    else:
        html = f"<div style='{font_css}'>{text}</div>"

    return st.markdown(html, unsafe_allow_html=True)

def st_chat_message(role, message, save=True):
    if role == "user":
        avatar = st.session_state["user_profile"]
    else:
        avatar = st.session_state["char_profile"]

    # 상태 저장
    if save:
        st.session_state["chat_history"].append(
            {
                "role": role,
                "content": message
            }
        )
            
    return st.chat_message(role, avatar=avatar).markdown(message)
