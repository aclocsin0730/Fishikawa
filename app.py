import streamlit as st
from streamlit.components.v1 import components
from introduction import introduction
from questions import questions
from show_images import show_images
from streamlit_option_menu import option_menu

selected = option_menu(
        menu_title="",
        icons=["1-square-fill", "2-square-fill", "3-square-fill"],
        options=["Introduction", "Questions", "Reaction Test"],
        orientation="horizontal",
        styles={
        "container": {"padding": "0!important", "background-color": "#fafafa"},
        "icon": {"color": "gray", "font-size": "20px"}, 
        "nav-link": {"font-size": "20px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "blue"},
    }
    )

if selected == "Introduction":
    introduction()
    
if selected == "Questions":
    questions()
    
if selected == "Reaction Test":
    show_images()