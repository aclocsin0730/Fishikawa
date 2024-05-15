import streamlit as st
import pandas as pd
import random
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Google Sheets authentication
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("paper-423314-05d2c7e30259.json", scope)
client = gspread.authorize(creds)
sheet = client.open("fishikawa_data").sheet1

def save_to_sheets(data):
    sheet.append_row(data)

def show_images():
    st.title("Reaction Time Test")

    if 'test_started' not in st.session_state:
        st.session_state.test_started = False

    if not st.session_state.test_started:
        if st.button("Start Test"):
            st.session_state.test_started = True
            st.session_state.image_index = 0
            st.session_state.reaction_times = []
            st.session_state.start_time = int(time.time() * 1000)  # Start time in milliseconds

    if st.session_state.test_started:
        # Load images and correct answers from CSV
        df = pd.read_csv("images.csv")
        images_set1 = df[:len(df)//2].values.tolist()  
        images_set2 = df[len(df)//2:].values.tolist() 

        all_images = images_set1 + images_set2

        # Ensure the image index and reaction times are in the session state
        if 'image_index' not in st.session_state:
            st.session_state.image_index = 0
        if 'reaction_times' not in st.session_state:
            st.session_state.reaction_times = []

        # Get the current image and correct answer
        current_image, correct_answer = all_images[st.session_state.image_index]

        st.image(current_image)
        
        # Generate wrong options
        wrong_options = [option for _, option in all_images if option != correct_answer]

        # Include correct answer in options
        options = random.sample(wrong_options, 3) + [correct_answer]

        answer = st.radio("Select the correct answer", options, key=f"radio_{st.session_state.image_index}", index=None)  # Unique key for radio buttons
        if answer:  # Check if an answer is selected
            if 'start_time' in st.session_state:
                end_time = int(time.time() * 1000)  # End time in milliseconds
                reaction_time = end_time - st.session_state.start_time
                if answer == correct_answer:
                    st.session_state.reaction_times.append(reaction_time)
                else:
                    st.session_state.reaction_times.append(0)
                st.session_state.start_time = int(time.time() * 1000)  # Start time for the next image

                # Move to the next image
                st.session_state.image_index += 1

                # Check if there are more images
                if st.session_state.image_index < len(all_images):
                    st.experimental_rerun()
                else:
                    save_to_sheets(st.session_state.reaction_times)
                    st.write("Thank you for participating!")
