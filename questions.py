import streamlit as st
from reaction_test import reaction_test


def questions():
    st.title("Questionnaire")
    age = st.number_input("Age", min_value=0)
    gender = st.selectbox("Sex at Birth", ["Male", "Female", "Other"])
    conf = st.selectbox("How confident are you with recognizing signages?", ["Low", "High"])
    drive = st.selectbox("Do you currently have a Driver's License?", ["Yes", "No"])
    if st.button("Next"):
        st.session_state.user_data = [age, gender, conf, drive,]
        # st.session_state.page = 3