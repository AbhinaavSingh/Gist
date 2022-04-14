from io import StringIO

import pandas as pd
import streamlit as st

from src import utils


def get_transcript_data(uploaded_file):
    if uploaded_file is not None:
        # To read file as bytes:
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        #  st.write(stringio)
        string_data = stringio.read()
        # st.write(string_data)
        return string_data


def get_sample_data(path):
    with open(path, 'r') as file:
        string_data = file.read()
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
                l_df.append(str(t.split("\r\n")[1].split("-->")[0]).strip())
                l_df.append(str(t.split("\r\n")[1].split("-->")[1]).strip())
                l_df.append(t.split("\r\n")[2].split(":")[0])
                l_df.append(t.split("\r\n")[2].split(":")[1])
                list_df.append(l_df)
        except Exception:
            print(t)
    df = pd.DataFrame(list_df)
    df.columns = ["Start Time", "End Time", "Speaker", "Text"]
    return df


def create_df_from_sample(text):
    text_list = text.strip().split("\n\n")
    list_df = []
    for t in text_list:
        try:
            if ":" in t:
                l_df = []
                l_df.append(str(t.split("\n")[1].split("-->")[0]).strip())
                l_df.append(str(t.split("\n")[1].split("-->")[1]).strip())
                l_df.append(t.split("\n")[2].split(":")[0])
                l_df.append(t.split("\n")[2].split(":")[1])
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
    st.write("Use sample meeting transcript")
    sample_button = st.button("Use Sample Data", help="use a sample data for testing")

    try:
        inp_text = ""
        if uploaded_file is not None or sample_button is True or len(utils.get_call_df()) != 0:
            with st.spinner(text="Loading data..."):
                if uploaded_file is not None:
                    inp_text = get_transcript_data(uploaded_file)
                elif sample_button:
                    inp_text = get_sample_data("resources/eiben.vtt")
                if len(inp_text) > 0:
                    if ("**" not in inp_text):
                        text = inp_text
                        utils.append_text_list(text)
                    else:
                        cleaned_text = clean(inp_text)
                        text = cleaned_text
                        utils.append_text_list(text)
                    if uploaded_file is not None:
                        call_df = create_df(text)
                        utils.append_call_df_list(call_df)
                    else:
                        call_df = create_df_from_sample(text)
                        utils.append_call_df_list(call_df)
                call_df = utils.get_call_df()
                text = utils.get_text()
                st.info("File uploaded successfully")
                if st.checkbox('Show sample transcript'):
                    st.markdown("**Data View**")
                    st.table(call_df[:5])
                    st.write('Only first 20 rows were loaded.')
                    if st.checkbox('Show entire transcript'):
                        slice_index = st.slider(
                            'Select a range of indices',
                            0, len(call_df),
                            (0, 5)
                        )
                        min_range, max_range = slice_index
                        st.table(call_df[min_range:max_range + 1])
                    return call_df, text
    except Exception:
        st.error("File upload failed. \n Check the file format")
        return None
