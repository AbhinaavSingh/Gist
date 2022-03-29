from io import StringIO

import pandas as pd
import streamlit as st


def get_transcript_data(uploaded_file):
    if uploaded_file is not None:
        # To read file as bytes:
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        #  st.write(stringio)
        string_data = stringio.read()
        # st.write(string_data)
        return string_data


def clean(text):
    sample = text.split('**')
    sample.pop(0)
    clean_text = ""
    i = 0
    for t in sample:
        if i % 2 != 0:
            clean_text += str(t)
        i += 1
        # print ("Clean Text: ", clean_text)
    return clean_text

def create_df(text):
    text_list = text.strip().split("\n\r")
    list_df = []
    for t in text_list:
        try:
            if ":" in t:
                l_df = []
                l_df.append(t.split("\r\n")[1].split("-->")[0])
                l_df.append(t.split("\r\n")[1].split("-->")[1])
                l_df.append(t.split("\r\n")[2].split(":")[0])
                l_df.append(t.split("\r\n")[2].split(":")[1])
                list_df.append(l_df)
        except Exception:
            print(t)
    df = pd.DataFrame(list_df)
    df.columns = ["Start Time", "End Time", "Speaker", "Text"]
    return df

def app():
    st.title("Upload Meeting Transcript")
    uploaded_file = st.file_uploader(
        "Choose a transcript file", type=["vtt"]
    )
    try:
        if uploaded_file is not None:
            inp_text = get_transcript_data(uploaded_file)
            if ("**" not in inp_text):
                text = inp_text
            else:
                cleaned_text = clean(inp_text)
                text = cleaned_text
            call_df = create_df(text)
            st.info("File uploaded successfully")
            st.markdown("**Data View**")
            st.write(call_df.head())
            return call_df, text
    except Exception:
        st.error("File upload failed. \n Check the file format")
        return None
