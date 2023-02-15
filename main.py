import base64

import pandas as pd
import plotly.express as px
import streamlit as st

# Load the CSV data
df = pd.read_csv('csv_files/eplmatches.csv')

def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

# create a new page
st.sidebar.markdown('## Navigation')
page = st.sidebar.radio('Go to', ['Home', 'DataManipulation'])
if page == 'Home':
    #make a home page for streamlit
    st.markdown('## Home')
    st.markdown('Welcome to the EPL Data App')
    st.markdown('This app is a work in progress')
    st.markdown('## Data')
    st.markdown('The data is from the 1993-94 season to the 2019-20 season')
    #show the data in a table format on the home page for the user to see what they are working with
    st.dataframe(df)
    st.markdown('## Download')
    #add a download button for the user to download the data
    csv = convert_df(df)
    file_name = 'file.csv'
    st.download_button(
        "Press to Download",
        csv,
        file_name,
        "text/csv",
        key='download-csv'
    )

if page == 'DataManipulation':
    st.markdown('## Data')

    # add a selectbox to manipulate the df before downloading for filtering per season on a multi-select
    season = st.selectbox('Select a season?', (df['Season_End_Year'].unique()))
    df = df[df['Season_End_Year'] == season]
    # add a multi-select to manipulate the df before downloading for filtering per team
    team = st.multiselect('Select a team?', (df['Home'].unique()))
    # filter the df based on the team selected check if the team is in the home or away column and then filter the df
    if team:
        df = df[(df['Home'].isin(team)) | (df['Away'].isin(team))]

    #filter Wk like numbers not 1,10,..
    df['Wk'] = df['Wk'].astype(str).str.replace(r'\D', '').astype(int)
    df = df.sort_values(by=['Wk'], ascending=True)

    # add a multi-select to manipulate the df before downloading for filtering per week
    week = st.multiselect('Select a week?', (df['Wk'].unique()))
    # filter the df based on the week selected
    if week:
        df = df[df['Wk'].isin(week)]

    with st.container():

        if team:
            st.header("Pie chart goals scored home and away")
            home_goals = df[df['Home'].isin(team)]['HomeGoals'].sum()
            away_goals = df[df['Away'].isin(team)]['AwayGoals'].sum()
            fig = px.pie(df, values=[home_goals, away_goals], names=['Goals Scored Home', 'Goals Scored Away'])
            st.plotly_chart(fig)

        if team:
            st.header("Pie chart goals conceded home and away")
            home_goals = df[df['Home'].isin(team)]['AwayGoals'].sum()
            away_goals = df[df['Away'].isin(team)]['HomeGoals'].sum()
            fig = px.pie(df, values=[home_goals, away_goals], names=['Goals Conceded Home', 'Goals Conceded Away'])
            st.plotly_chart(fig)
    st.markdown('## Download')

    csv = convert_df(df)
    file_name = f'file_{season}.csv'
    st.download_button(
        "Press to Download",
        csv,
        file_name,
        "text/csv",
        key='download-csv'
    )


