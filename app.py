import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import random
import time
import json

# Google Sheets authentication
creds_json = st.secrets['secrets']["gcp_service_account"]
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(creds_json, scope)
client = gspread.authorize(creds)
sheet = client.open("fishikawa_data").sheet1

# Function to save data to Google Sheets
def save_to_sheets(data):
    sheet.append_row(data)

# First page: Introduction
def introduction():
    st.title("Study Introduction")
    st.write("Hi! We are ajkldjaslallj blob blob fish fishikawa")
    if st.button("Take the test!"):
        st.session_state.page = 2

# Second page: Questions
def questions():
    st.title("Questionnaire")
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=0)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    if st.button("Submit"):
        st.session_state.user_data = [name, age, gender]
        st.session_state.page = 3

# Third page: Reaction Time Test
def reaction_test():
    st.title("Reaction Time Test")
    st.write("Next part will be recording the time it takes for you to click the correct answer for each image.")
    if st.button("Start"):
        st.session_state.page = 4

def show_images():
    st.title("Reaction Time Test")
    
    # Load images and correct answers from CSV
    df = pd.read_csv("Fishikawa\images.csv")
    images_set1 = df[:len(df)//2].values.tolist()  
    images_set2 = df[len(df)//2:].values.tolist()  
    
    random.shuffle(images_set1)
    random.shuffle(images_set2)

    all_images = images_set1 + images_set2

    # Ensure the image index and reaction times are in the session state
    if 'image_index' not in st.session_state:
        st.session_state.image_index = 0
    if 'reaction_times' not in st.session_state:
        st.session_state.reaction_times = []

    # Get the current image and correct answer
    current_image, correct_answer = all_images[st.session_state.image_index]

    st.image(current_image)
    options = ["Option 1", "Option 2", "Option 3", "Option 4"]
    
    if correct_answer not in options:
        options[0] = correct_answer  # Ensure the correct answer is included

    random.shuffle(options)  # Randomize the options

    start_time = time.time()
    answer = st.radio("Select the correct answer", options, key=f"radio_{st.session_state.image_index}")  # Unique key for radio buttons
    if st.button("Submit", key=f"submit_button_{st.session_state.image_index}"):  # Unique key for submit button
        end_time = time.time()
        if answer == correct_answer:
            st.session_state.reaction_times.append(end_time - start_time)
        else:
            st.session_state.reaction_times.append(0)
        
        # Move to the next image
        st.session_state.image_index += 1

        # Check if there are more images
        if st.session_state.image_index < len(all_images):
            st.experimental_rerun()
        else:
            save_to_sheets(st.session_state.user_data + st.session_state.reaction_times)
            st.write("Thank you for participating!")

# Navigation
if 'page' not in st.session_state:
    st.session_state.page = 1

if st.session_state.page == 1:
    introduction()
elif st.session_state.page == 2:
    questions()
elif st.session_state.page == 3:
    reaction_test()
elif st.session_state.page == 4:
    show_images()
