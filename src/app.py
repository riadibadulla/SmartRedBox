import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import util

# Initialize data
data = {
    'Event': ['Event 1', 'Event 2', 'Event 3', 'Event 4'],
    'Start Date': pd.to_datetime(['2022-01-01', '2022-03-01', '2022-04-01', '2022-05-01']),
    'End Date': pd.to_datetime(['2022-02-01', '2022-04-01', '2022-05-01', '2022-06-01'])
}

df = pd.DataFrame(data)

# Initialize data
data = {
    'Headline': ['AI regulation: pro-innovation, responsible growth.', 'Event 1', 'Event 1', 'Event 1'],
    'Sentiment': [1, 1, -1, 3],
    'Date': ['2020-01-01', '2021-03-01', '2022-04-01', '2022-05-01'],
    'Relevance': [0.7, 0.4, 0.8, 0.95],
    'Color': ['blue', 'blue', 'red', 'green'],
    'Topic' :['Submissions', 'Submissions', 'Internal sources', 'Public'],
    'Summary': [
    ' The UK government has proposed a new AI regulatory framework that includes five values-focused cross-sectoral principles to guide regulator responses to AI risks and opportunities. This framework is designed to provide clarity and coherence to the AI regulatory landscape, build the evidence base, and ensure risks are identified and addressed while also supporting innovation. It includes a set of functions to support implementation of the framework, such as monitoring, assessment and feedback, and cross-sectoral risk assessment. The government has opened a consultation to receive feedback from stakeholders, and plans to establish a regulatory sandbox for AI and engage with the public to build trust in the technology.', 
    'something', 'else', 'else']
}
def add_linebreaks(string, every=64):
    lines = []
    for i in range(0, len(string), every):
        lines.append(string[i:i+every])
    return '<br>'.join(lines)




df = pd.DataFrame(data)

# Convert dates to datetime
df['Date'] = pd.to_datetime(df['Date'])


# Create a Plotly figure for the timeline
fig = go.Figure()


# Add static line
fig.add_shape(
    type="line",
    x0=df.Date.min(),
    y0=0,
    x1=df.Date.max(),
    y1=0,
    line=dict(
        color="black",
        width=2,
    ),
)


####


####

# Add vertical lines and markers at the top
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
