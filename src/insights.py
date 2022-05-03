import re

import pandas as pd
import plotly.express as px
import streamlit as st


def app(df):
    try:
        df_orig = df.copy()
        df['Start Time'] = pd.to_datetime(df['Start Time'])
        df['End Time'] = pd.to_datetime(df['End Time'])
        st.title('Generating Insights')

        st.subheader("Data View")
        n_slice_index = st.slider(
            'Select a range of indices',
            0, len(df),
            (0, 5)
        )
        min_range, max_range = n_slice_index
        st.table(df[min_range:max_range + 1])

        st.subheader("General Information")
        col1, col2, col3 = st.columns(3)
        col1.metric("Number of Participants", len(df['Speaker'].unique()))
        start_time = df.iloc[[0]]['Start Time'][0]
        end_time = df.iloc[[-1]]['End Time'][len(df) - 1]
        delta = end_time - start_time
        col2.metric("Duration of the Meeting",
                    "{} hrs {} mins".format(delta.components.hours, delta.components.minutes))
        st.write("Names of the Participants : {}".format(", ".join(list(df['Speaker'].unique()))))

        grpd_df = df.groupby('Speaker', as_index=False)['Text'].aggregate(lambda x: list(x))

        def f(x):
            text_list = x['Text']
            count = 0
            for t in text_list:
                t = re.sub(r'[^A-Za-z0-9 ]+', '', t)
                count += len(t.split())
            return count

        grpd_df["Number of Words"] = grpd_df.apply(lambda x: f(x), axis=1)
        col3.metric("Total Number of Words",
                    "{} ".format(int(grpd_df["Number of Words"].sum())))
        st.table(grpd_df[['Speaker', 'Number of Words']])
        fig = px.bar(grpd_df, x="Speaker", y="Number of Words", color='Speaker')
        st.plotly_chart(fig, use_container_width=True)

        time_df = df_orig.copy()
        time_df['start_delta'] = pd.to_timedelta(df_orig['Start Time'])
        time_df['end_delta'] = pd.to_timedelta(df_orig['End Time'])
        time_df['delta'] = time_df['end_delta'] - time_df['start_delta']
        grpd_time_df = time_df.groupby('Speaker', as_index=False)['delta'].apply(lambda x: x.sum())

        def f(x):
            delta = x['delta']
            sec = delta.components.seconds
            mins = delta.components.minutes
            return float(mins) + float(sec / 60)

        grpd_time_df["Time in Minutes"] = grpd_time_df.apply(lambda x: f(x), axis=1)
        st.table(grpd_time_df[['Speaker', 'Time in Minutes']])
        fig = px.bar(grpd_time_df, x="Speaker", y="Time in Minutes", color='Speaker')
        st.plotly_chart(fig, use_container_width=True)

        conv_df = df_orig.copy()
        conv_df['start_delta'] = pd.to_timedelta(df_orig['Start Time'])
        conv_df['end_delta'] = pd.to_timedelta(df_orig['End Time'])

        def f(x):
            end = x['end_delta']
            mins = end.components.minutes
            return mins

        conv_df["mins"] = conv_df.apply(lambda x: f(x), axis=1)
        conv_df_grps = conv_df.groupby(['mins', 'Speaker'], as_index=False)['Text'].aggregate(lambda x: list(x))
        def f(x):
            text_list = x['Text']
            count = 0
            for t in text_list:
                t = re.sub(r'[^A-Za-z0-9 ]+', '', t)
                count += len(t.split())
            return count

        conv_df_grps["Number of Words"] = conv_df_grps.apply(lambda x: f(x), axis=1)
        fig = px.line(conv_df_grps, x="mins", y="Number of Words", color='Speaker', markers=True)
        st.plotly_chart(fig, use_container_width=True)

    except Exception:
        st.error("Unable to parse the data. \n Reupload the vtt file")
