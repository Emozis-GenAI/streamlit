import streamlit as st 
import re

class LoginClick:
    # 데이터 검증
    @staticmethod 
    def validate_login(data):
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
    
    # 내 캐릭터 관리 클릭
    @staticmethod
    def mypage():
        st.session_state["mypage_view"] = "mypage"

    # 로그아웃 클릭
    @staticmethod
    def logout():
        st.session_state["user"] = None

    ## 로그인 클릭
    @staticmethod
    def login_window(window):
        st.session_state["login_window"] = window