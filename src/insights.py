import streamlit as st
import pandas as pd


def app(df):
    try:
        df['Start Time'] = pd.to_datetime(df['Start Time'])
        df['End Time'] = pd.to_datetime(df['End Time'])
        st.title('Generating Insights')

        st.subheader("Data View")
        slice_index = st.slider(
            'Select a range of indices',
            0, len(df),
            (0, 5)
        )
        min_range, max_range = slice_index
        st.table(df[min_range:max_range + 1])

        st.subheader("General Information")
        col1, col2, col3 = st.columns(3)
        col1.metric("Number of Participants", len(df['Speaker'].unique()))
        start_time = df.iloc[[0]]['Start Time'][0]
        end_time = df.iloc[[-1]]['End Time'][len(df) - 1]
        delta = end_time - start_time
        col2.metric("Duration of the Meeting", "{} hrs {} mins".format(delta.components.hours, delta.components.minutes))
        st.write("Names of the Participants : {}".format(", ".join(list(df['Speaker'].unique()))))

    except Exception:
        st.error("Unable to parse the data. \n Reupload the vtt file")
