import streamlit as st

from core.utils import *
from core.state import *

from states.login import LoginClick
from services.login import LoginService

setting()
#-------------------------------------------------------------------
# Form
#-------------------------------------------------------------------
# 로그인 화면 
if st.session_state["login_window"] == "login":
    columns = st.columns(spec=[0.2,0.6,0.2])
    with columns[1]:
        # View
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
            on_click=LoginClick.login_window, 
            args=["register"],
            key="register"
        )
        # 비밀번호 리셋 버튼(deprecated)
        # st.button(
        #     label="비밀번호 리셋",
        #     use_container_width=True, 
        #     on_click=login_window, 
        #     args=["reset"],
        #     key="reset"
        # )
        #-------------------------------------------------------------------
        # Script
        if login_btn:
            data = {
                "username": username, 
                "password": password,
            }
            # 데이터 검증
            val_data = LoginClick.validate_login(data)
            if isinstance(val_data, str):
                st.error(val_data)
            # 데이터 전송
            else:
                response = LoginService.login_api(data)
                if response:
                    st.session_state["user"] = response
                    st.session_state["login"] = True
                    st.session_state["transition"] = True
                    st.switch_page("pages/home.py")
#-------------------------------------------------------------------
# 회원가입 화면
elif st.session_state["login_window"] == "register":
    columns = st.columns(spec=[0.2,0.6,0.2])
    with columns[1]:
        # View
        with st.form(key="register_form"):
            # 제목
            st.markdown("회원가입")
            # 입력 창
            username = st.text_input(label="ID", max_chars=15)
            nickname = st.text_input(label="닉네임", max_chars=15)
            password = st.text_input(label="비밀번호", max_chars=15, type="password")
            check_password = st.text_input(label="비밀번호 확인", max_chars=15, type="password")
            # 회원가입 버튼
            register_btn = st.form_submit_button(
                label="회원가입",
                use_container_width=True, 
                type="primary"
            )
            # 주의사항
            st_textbox("ID는 영문, 숫자만 가능하며, 4자 이상 입력하세요.", fontsize=0.7, style="list")
            st_textbox("닉네임은 영문, 한글, 숫자만 가능하며, 1자 이상 입력하세요.", fontsize=0.7, style="list")
            st_textbox("비밀번호는 영문, 숫자, 특수문자만 가능하며, 4자 이상 입력하세요.", fontsize=0.7, style="list")
            vertical_space(2)
        #-------------------------------------------------------------------
        # Script
        if register_btn:
            data = {
                "username": username, 
                "nickname": nickname,
                "password": password,
            }
            # 데이터 검증
            val_data = LoginClick.validate_login(data)
            if password != check_password:
                st.error("비밀번호와 확인 비밀번호가 일치하지 않습니다.", icon="🚨")
            elif isinstance(val_data, str):
                st.error(val_data)
            # 데이터 전송
            else:
                response = LoginService.register_api(data)
                if response:
                    LoginClick.login_window("login")
                    st.session_state["transition"] = True
                    st.switch_page("pages/login.py")
#-------------------------------------------------------------------
# 비밀번호 변경 화면(deprecated)
# elif st.session_state["login_window"] == "reset":
#     columns = st.columns(spec=[0.2,0.6,0.2])
#     with columns[1]:
#         with st.form(key="login"):
#             # 제목
#             st.markdown("비밀번호 변경")
#             # 입력 창
#             username = st.text_input(label="ID", max_chars=15)
#             nickname = st.text_input(label="닉네임", max_chars=15)
#             password = st.text_input(label="비밀번호", max_chars=15, type="password")
#             re_password = st.text_input(label="비밀번호 확인", max_chars=15, type="password")
#             # 비밀번호 변경 버튼
#             reset_btn = st.form_submit_button(
#                 label="비밀번호 변경", 
#                 use_container_width=True, 
#                 type="primary"
#             )
#             # 주의사항
#             st_textbox("비밀번호는 영문, 숫자, 특수문자만 가능하며, 4자 이상 입력하세요.", fontsize=0.7, style="list")
#             vertical_space(2)


            