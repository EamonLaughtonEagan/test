import json
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import networkx as nx
import dash
import dash_cytoscape as cyto
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

#style settings
styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}


# SCHEMA: CASE_ID, LINKED_CASES, REPORT_DATE, LOCATION, PERSONAL_INFORMATION
# LINKED_CASES: CASE 1, ..., CASE N
# PERSONAL_INFORMATION: FIRST_NAME, LAST_NAME
with open('Singapore_Data.json') as f:
    data = json.load(f)

df = pd.json_normalize(data['DATA'])
df_cluster = pd.json_normalize(data['CLUSTER'])
clusters = []
for i in range(len(df_cluster)):
    clusters.append(df_cluster['LOCATION'][i])
#print(df_cluster['CASE_IDS'], df_cluster['LOCATION'])

#################################################################################
#create a column in the data frame for the length each linked case for each case#
len_linked_cases = []
for i in range(len(df)):
    length = 0
    for j in range(len(df['LINKED_CASES'][i])):
        length += 1
    len_linked_cases.append(length)
df['LEN_LINKED_CASES'] = len_linked_cases
#################################################################################


fig = go.Figure()
fig.update_layout(
    autosize=False,
    hovermode='closest',
    margin=dict(b=5, l=40, r=5, t=50),
    annotations=[dict(showarrow=False, xref="paper", yref="paper",x=0.005, y=- 0.002)])



app.layout = html.Div([
    html.H1('Singapore Data Visualization'),
    html.P('Graph indicating unique cases and their respective connections throughout the begining months of the COVID-19 pandemic in 2020.'),
    dcc.Graph(id='graph'),
    html.P('Selected Date(s)'),
    dcc.RangeSlider(
        id='range-slider',
        min=0, max=len(df), step=1,
        marks={
          0: str(df['REPORT_DATE.MONTH'][0]) + ' ' + str(df['REPORT_DATE.DAY'][0]),
          len(df)/2: str(df['REPORT_DATE.MONTH'][(len(df)-1)/2]) + ' ' + str(df['REPORT_DATE.DAY'][(len(df)-1)/2]),
          len(df): str(df['REPORT_DATE.MONTH'][len(df)-1]) + ' ' + str(df['REPORT_DATE.DAY'][len(df)-1])},
        #marks={x: str(x) for x in df['CASE_ID']},
        value=[0, 101] 
    ),
    html.Div(children=[
        html.H2('Current range of Dates'),
        html.H3(id='range-of-dates')
    ]),
    html.Div(children=[
        html.H4('Cluster Data'),
        html.H5(id='hover-data', style=styles['pre'])
    ]),
])

@app.callback(
    Output('graph', 'figure'),
    Input('range-slider', 'value'))
def update_node_graph(slider_range):
    dff = df
    low, high = slider_range
    mask = (dff['CASE_ID'] > low) & (dff['CASE_ID'] < high)
    fig = px.scatter(
        dff[mask], x='CASE_ID', y = 'LEN_LINKED_CASES', custom_data=['CASE_ID', 'LINKED_CASES', 'EXPOSURE', 'LOCATION'],
        color='LOCATION', size='LEN_LINKED_CASES', height=500, width=1500,
        hover_data=['LINKED_CASES'])
    fig.update_traces(
    hovertemplate='<br>'.join([
        'Case ID: %{customdata[0]}',
        'Linked Cases: %{customdata[1]}',
        'Exposure: %{customdata[2]}',
        'Location: %{customdata[3]}'
    ]))
    fig.update_layout(
        yaxis=dict(
            title='Number of Linked Cases',
            showgrid=False,
            gridwidth=1,
            zeroline=False,
            color='black',
            linecolor='black',
            mirror=True),
            
        xaxis=dict(
            title='Case Number',
            showgrid=False,
            gridwidth=1,
            #gridcolor='black',
            zeroline=False,
            color='black',
            linecolor='black',
            mirror=True),
        
        legend=dict(
            x=1, y=1, title_text='Locations', bordercolor='black', borderwidth=1,
        ),

        clickmode='event+select',
    )
    return fig

@app.callback(
    Output('range-of-dates', 'children'),
    Input('range-slider', 'value'))
def update_dates(slider_range):
    low, high = slider_range
    container =  df['REPORT_DATE.MONTH'][low] + ' ' + str(df['REPORT_DATE.DAY'][low]) + ' - ' + df['REPORT_DATE.MONTH'][high] + ' ' + str(df['REPORT_DATE.DAY'][high])
    return container

@app.callback(
    Output('hover-data', 'children'),
    Input('graph', 'hoverData'))
def show_cluster(clicked_case):
    try:
        is_cluster = clicked_case['points'][0]['customdata'][3]
        if is_cluster in clusters:
            return json.dumps(is_cluster, indent=2)
        #elif is cluster in clusters and 
        else:
            return 'Case is not part of a cluster'
    except TypeError:
        pass

app.run_server(debug=True)
