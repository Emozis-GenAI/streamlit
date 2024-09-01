import streamlit as st
import re
from st_pages import get_nav_from_toml

from core.utils import *
from core.state import *

setting()
#-------------------------------------------------------------------
# Settings
#-------------------------------------------------------------------
def validate_length(data):
    length_condition = {"username": 4, "nickname": 1, "password": 4}
    regex_condition = {
        "username": {"regex": r"^[A-Za-z0-9]+$", "description": "영문, 숫자만 가능합니다."},
        "nickname": {"regex": r"^[가-힣A-Za-z0-9]+$", "description": "한글, 영문, 숫자만 가능합니다."},
        "password": {"regex": r"^[A-Za-z0-9!@#$]+$", "description": "영문, 숫자, 특수문자(!,@,#,$)만 가능합니다."}
    }

    for key, value in data.items():
        if len(value) < length_condition[key]:
            return f"{key} Error: {length_condition[key]}자 이상 입력해야 합니다."
        
        if not re.fullmatch(regex_condition[key]["regex"], value):
            return f"{key} Error: {regex_condition[key]['description']}"
        
    return True

#-------------------------------------------------------------------
# View
#-------------------------------------------------------------------
# 로그인 화면 
if st.session_state["login_window"] == "login":
    columns = st.columns(spec=[0.2,0.6,0.2])
    with columns[1]:
        with st.form(key="login_form"):
            # 제목
            st.markdown("로그인")
            # 입력 창
            username = st.text_input(label="ID", max_chars=15)
            password = st.text_input(label="비밀번호", max_chars=15, type="password")
            # 로그인 버튼
            login_btn = st.form_submit_button(
                label="로그인", 
                use_container_width=True, 
                type="primary"
            )
        # 회원가입 버튼
        st.button(
            label="회원가입", 
            use_container_width=True, 
            on_click=login_window, 
            args=["register"],
            key="register"
        )
# 회원가입 화면
elif st.session_state["login_window"] == "register":
    columns = st.columns(spec=[0.2,0.6,0.2])
    with columns[1]:
        with st.form(key="register_form"):
            # 제목
            st.markdown("회원가입")
            # 입력 창
            username = st.text_input(label="ID", max_chars=15)
            nickname = st.text_input(label="닉네임", max_chars=15)
            password = st.text_input(label="비밀번호", max_chars=15, type="password")
            check_password = st.text_input(label="비밀번호 확인", max_chars=15, type="password")
            # 회원가입 버튼
            signup_btn = st.form_submit_button(
                label="회원가입",
                use_container_width=True, 
                type="primary"
            )
            # 주의사항
            st_textbox("ID는 영문, 숫자만 가능하며, 4자 이상 입력하세요.", fontsize=0.7, style="list")
            st_textbox("닉네임은 영문, 한글, 숫자만 가능하며, 1자 이상 입력하세요.", fontsize=0.7, style="list")
            st_textbox("비밀번호는 영문, 숫자, 특수문자만 가능하며, 4자 이상 입력하세요.", fontsize=0.7, style="list")
            vertical_space(2)

# if st.session_state["login_window"] == "login":
#     columns = st.columns(spec=[0.2,0.6,0.2])
#     with columns[1]:
#         with st.form(key="login_form"):
#             st.markdown("로그인")
#             username = st.text_input(label="ID", max_chars=15)
#             password = st.text_input(label="비밀번호", max_chars=15, type="password")

#             login_btn = st.form_submit_button(
#                 label="로그인", 
#                 use_container_width=True, 
#                 type="primary"
#             )

#         if login_btn:
#             data = {
#                 "username": username, 
#                 "password": password,
#             }
#             val_data = validate_length(data)
#             if isinstance(val_data, str):
#                 st.error(val_data)
#             else:
#                 response = requests.post(
#                     url="http://172.16.2.10:8000/user/login",
#                     json=data
#                 )
#                 response_json = json.loads(response.text)
#                 if response_json["status"] == "success":
#                     data = response_json["data"]
#                     st.session_state["user"] = f"{data['username']}({data['nickname']})"
#                     st.session_state["login"] = True
#                     st.switch_page("pages/page1.py")
#                 else:
#                     st.error(response_json["message"])

#         st.button("회원가입", use_container_width=True, on_click=login_window, args=["signup"])
#         # st.button("비밀번호 변경", use_container_width=True, on_click=login_window, args=["reset"])            
            
# elif st.session_state["login_window"] == "register":
#     columns = st.columns(spec=[0.2,0.6,0.2])
#     with columns[1]:
#         with st.form(key="login"):
#             st.markdown("회원가입")
#             username = st.text_input(label="ID", max_chars=15)
#             nickname = st.text_input(label="닉네임", max_chars=15)
#             password = st.text_input(label="비밀번호", max_chars=15, type="password")
#             re_password = st.text_input(label="비밀번호 확인", max_chars=15, type="password")

#             signup_btn = st.form_submit_button(label="회원가입", use_container_width=True, type="primary")
        
#         if signup_btn:
#             data = {
#                 "username": username, 
#                 "nickname": nickname,
#                 "password": password,
#             }
#             val_data = validate_length(data)
#             if password != re_password:
#                 st.error("비밀번호와 확인 비밀번호가 일치하지 않습니다.", icon="🚨")
#             elif isinstance(val_data, str):
#                 st.error(val_data)
#             else:
#                 response = requests.post(
#                     url="http://172.16.2.10:8000/user/signup",
#                     json=data
#                 )
#                 response_json = json.loads(response.text)
#                 if response_json["status"] == "success":
#                     st.switch_page("pages/page1.py")
#                 else:
#                     st.error(response_json["message"])


# elif st.session_state["login_window"] == "reset":
#     columns = st.columns(spec=[0.2,0.6,0.2])
#     with columns[1]:
#         with st.form(key="login"):
#             st.markdown("비밀번호 변경")
#             username = st.text_input(label="ID", max_chars=15)
#             nickname = st.text_input(label="닉네임", max_chars=15)
#             password = st.text_input(label="비밀번호", max_chars=15, type="password")
#             re_password = st.text_input(label="비밀번호 확인", max_chars=15, type="password")

#             reset_btn = st.form_submit_button(label="비밀번호 변경", use_container_width=True, type="primary")

