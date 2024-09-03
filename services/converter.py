import streamlit as st

from core.utils import vertical_space

class Converter:
    @staticmethod
    def gender(gender, method="value"):
        if method=="value":
            gen_values = {"남": "male", "여": "female", "기타": "other"}
        elif method=="idx":
            gen_values = {"male": 0, "female": 1, "other": 2}

        return gen_values[gender.strip()]
    
    @staticmethod
    def tag(text):
        text_list = text.split(",")
        add_tag = [f"#{x.strip()}" for x in text_list]
        return " ".join(add_tag)
    
    def make_form(self, data):
        vertical_space(1)
        columns = st.columns(spec=[0.25,0.5,0.25])
        with columns[1]:
            st.image(data["profile"])
        vertical_space(1)
        st.markdown(f"[이름] {data['name']}")
        st.markdown(f"[관계] {self.tag(data['relationship'])}")
        st.markdown(f"[성격] {self.tag(data['personality'])}")
        st.markdown(f"[상세설명]<br> {data['summary']}", unsafe_allow_html=True)

converter = Converter()