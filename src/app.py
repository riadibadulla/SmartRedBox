import streamlit as st
import pandas as pd
import plotly.graph_objs as go
from util import *
import time
from streamlit_option_menu import option_menu
from datetime import datetime


def add_linebreaks(string, every=64):
    lines = []
    for i in range(0, len(string), every):
        lines.append(string[i:i+every])
    return '<br>'.join(lines)


def load_submission(path):
    submission = {'summary': None, 'position': None}
    submission['summary'] = summarise(path)
    submission['position'] = get_position(path)
    return submission

def find_min_max_date(df):
    # Convert the dates to datetime objects
    df['Date'] = pd.to_datetime(df['Date'])
    return df['Date'].min(), df['Date'].max()

def add_timeline(df):
    min_date, max_date = find_min_max_date(df)

    # add timeline
    fig.add_shape(
        type="line",
        x0=min_date,
        y0=0,
        x1=max_date,
        y1=0,
        line=dict(
            color="black",
            width=2,
        ),
    )

    # {
    #     "Type": <type of document, this could be an email, meeting minutes, submission>,
    #     "Title": <title of the document>,
    #     "Topic": <overall topic discussed in the document>,
    #     "Summary": <summary of the document content>,
    #     "Content": null,
    #     "Relevant People": <list of people mentioned in the document, inlcuding sender and recipients, format as: Forname Surname>,
    #     "Director": <director mentioned in the document>,
    #     "Team": <teams mentioned in the document that need to give clearance, where a name is provided>,
    #     "Sentiment": <sentiment analysis of the document, should be a floating point number between -1.00 and 1.00, with -1.00 being negative and 1.00 being positive and 0.00 being neutral, must be filled>,
    #     "Deadline": <deadline of any actions mentioned in the document, format as exactly as shown in the document>,
    #     "Actions": <any follow-up actions mentioned in the document, with added deadline as per "Deadline" field>,
    #     "Notes": <any notes attached to the document>,
    #     "Date": <date of the document in the format: YYYY-MM-DD, if no date is found then null>
    # }

    for i, row in df.iterrows():
        fig.add_shape(
            type="line",
            x0=row['Date'],
            y0=0,
            x1=row['Date'],
            y1=row['Sentiment'],
            yref='y',
            line=dict(
                color="black",
                width=1,
            ),
        )

        summary_with_breaks = add_linebreaks(str(row['Summary']))
        
        fig.add_trace(go.Scatter(
        x=[row['Date']], 
        y=[row['Sentiment']],
        mode='markers',
        marker=dict(size=row['Relevance']*50, color=row['Color']),
        # marker=dict(size=10, color=row['Color']),
        text=['<b>Date:</b> '+str(row['Date']) + '<br><b>Headline:</b> '+str(row['Headline']) + '<br><b>Summary:</b> '+ summary_with_breaks],
        hoverinfo='text',
        name= str(row['Topic'])
    ))

    # Display the figure with Streamlit
    st.plotly_chart(fig)


def display_submission(submission, related_data):
    st.image('./data/profile.jpeg')

    # Streamlit
    st.title('Submission summary')

    summary = submission['summary']
    bordered_text = f'<div style="border:2px solid black; padding:10px">{summary}</div>'

    st.markdown(bordered_text, unsafe_allow_html=True)


    st.title('Current position')
    # st.write(timeline_chart)
    position = submission['position']
    bordered_text = f'<div style="border:2px solid black; padding:10px">{position}</div>'

    st.markdown(bordered_text, unsafe_allow_html=True)

    add_timeline(related_data)


def upload():
    uploaded_file = st.file_uploader("Upload your submission: ", type="pdf")
    show_file = st.empty()
    if uploaded_file is not None:
        show_file.info("File received!")
        submission = load_submission(uploaded_file)
        related_data = get_related_data(uploaded_file)
        display_submission(submission, related_data)

def toolbar():
    with st.sidebar:
        selected = option_menu(
            menu_title= 'Private secretaries',
            options=['Tom Waterhouse', 'Saisakul Chernbumroong', 'Somebody else'],
            icons=['arrow-through-heart', 'house', 'house'],
            menu_icon='cast',
            default_index= 0,
            orientation='vertical',
        )
    if selected == 'Tom Waterhouse':
        st.title(f'Welcome {selected}')


# Create a Plotly figure for the timeline
fig = go.Figure()

st.title('REDUX')

toolbar()
upload()

