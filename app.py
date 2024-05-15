import streamlit as st
from streamlit.components.v1 import components
from introduction import introduction
from questions import questions
from show_images import show_images
from streamlit_option_menu import option_menu

# # Define the page titles and corresponding functions
# pages = {
#     "Introduction": introduction,
#     "Questions": questions,
#     "Reaction Test": reaction_test,
#     "Show Images": show_images,
# }

# # Create a top bar for navigation
# current_page = st.sidebar.radio("Navigation", list(pages.keys()))

# # Execute the selected page's function
# pages[current_page]()

selected = option_menu(
        menu_title="",
        icons=["1-square-fill", "2-square-fill", "3-square-fill"],
        options=["Introduction", "Questions", "Reaction Test"],
        orientation="horizontal",
        styles={
        "container": {"padding": "0!important", "background-color": "#fafafa"},
        "icon": {"color": "white", "font-size": "20px"}, 
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


# if 'page' not in st.session_state:
#     st.session_state.page = 1

# if st.session_state.page == 1:
#     introduction()
# elif st.session_state.page == 2:
#     questions()
# elif st.session_state.page == 3:
#     reaction_test()