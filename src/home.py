import streamlit as st


def app():
    

    st.title("Home")
    st.markdown("""
    [![](https://img.shields.io/badge/GitHub-Source-brightgreen)](https://github.com/AbhinaavSingh/Gist)
    """)
    st.subheader("How to use Gist")
    st.markdown("""
    - Upload meeting transcript using the option in the sidebar.
    - Click on Generate Insights to see the most important insights from the meeting.
    - Click on Generate Summary to get a TL;DR of the meeting. 
    """)
    st.markdown("""More than just minutes of the meeting! 🚀""")
    st.markdown("""
    ###### Made with ❤️ and 🦙 by [Abhinaav Singh](https://abhinaav.com) and [Akshay Bahadur](https://akshaybahadur.com)
    """)
