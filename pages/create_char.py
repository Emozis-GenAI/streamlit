import streamlit as st
from streamlit_image_select import image_select
from streamlit_tags import st_tags

from core.state import *
from core.utils import *

from states.create_char import CreateCharClick

from services.create_char import CreateCharService
from services.converter import converter

setting()
# 초기화
custom_init(["select_img"])
#-------------------------------------------------------------------
# Form(View)
#-------------------------------------------------------------------
# 첫 인사
st.text_input(
    label="첫 인사",
    value=configs.GREETING,
    key="char_greet",
    placeholder="채팅의 첫 인사말을 작성해주세요"
)
# 정보 입력
col1, col2 = st.columns(spec=[0.3,0.7])
# 프로필
col1.image(st.session_state["select_img"], width=200)
# 이름, 성별
with col2:
    st.text_input(label="캐릭터 이름", key="char_name", max_chars=15)
    st.radio(label="성별", options=["남","여","기타"], key="char_gen")

# 성별에 따라 캐릭터 프로필 목록 가져오기
data = CreateCharService.get_profile(st.session_state["char_gen"])
# popover 선택 인덱스 초기화
st.session_state["char_img"] = 0

# 프로필 선택 창
with st.popover("프로필 선택", use_container_width=True):
    image_select(
        label="", 
        images=list(data.values()),
        return_value="index",
        key="char_img"
    )
    st.button(
        label="적용",
        use_container_width=True, 
        type="primary",
        key="select_btn",
        on_click=CreateCharClick.change_img,
        args=[data]
    )
# 관계
if "char_rel" in st.session_state:
    rel_value = st.session_state["char_rel"]
else:
    rel_value = None
st_tags(
    label="관계",
    value=rel_value,
    text='관계를 입력하고 Enter를 누르세요(최대 5개)',
    suggestions=['애인', '남사친', '여사친', 
                 '전남친', '가족', '직장상사', 
                 '시어머니', '할아버지', '할머니'],
    maxtags = configs.MAX_TAGS,
    key="char_rel")
# 성격
if "char_per" in st.session_state:
    per_value = st.session_state["char_per"]
else:
    per_value = None
st_tags(
    label="성격",
    value=per_value,
    text='성격을 입력하고 Enter를 누르세요(최대 5개)',
    suggestions=['착함', '날카로움', '예민함', 
                 '온화함', '성격급함', '푸근함', 
                 '스윗함', '괴팍함', '인자함'],
    maxtags = configs.MAX_TAGS,
    key="char_per")
# 상세 설명
st.text_area(
    label="상세 설명",
    height=200, 
    key="char_det",
    placeholder="캐릭터에 대해 자세히 설명해주세요"
)

# 채팅 생성 버튼
st.button(
    label="캐릭터 생성", 
    use_container_width=True, 
    type="primary",
    key="create_btn"
)
#-------------------------------------------------------------------
# Form(Script)
#-------------------------------------------------------------------
if st.session_state["create_btn"]:
    character_data = {
        "name": st.session_state["char_name"],
        "profile": st.session_state["select_img"],
        "gender": converter.gender(st.session_state["char_gen"]),
        "relationship": ','.join(st.session_state["char_rel"]),
        "personality": ','.join(st.session_state["char_per"]),
        "greeting": st.session_state["char_greet"],
        "details": st.session_state["char_det"],
        "user": st.session_state["user"]
    }
    # 데이터 전송
    response = CreateCharService.create_char_api(character_data)
    if response:
        st.switch_page("pages/char_list.py")

