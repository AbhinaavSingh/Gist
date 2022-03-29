import streamlit as st


def app(call_df):
    try:
        st.title('Generating Insights')
        st.write(call_df.head())
        call_df['Speaker'].unique()
        st.write("Number of Participants : {}".format(len(call_df['Speaker'].unique())))
        st.write("Names of the Participants : {}".format(", ".join(list(call_df['Speaker'].unique()))))
    except Exception:
        st.error("Unable to parse the data. \n Reupload the vtt file")
