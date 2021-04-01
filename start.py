import json
import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import random
import dash
import dash_core_components as dcc
import dash_html_components as html

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

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
singapore_dict = json.dumps(data, indent=3)

G = nx.Graph()
node_edge_pair = []
for i in range(len(data["DATA"])):

    case_id = data["DATA"][i]["CASE_ID"]
    linked_cases = data["DATA"][i]["LINKED_CASES"]
    location = data["DATA"][i]["LOCATION"]
    report_date = data["DATA"][i]["REPORT_DATE"]
    exposure = data["DATA"][i]["EXPOSURE"]

    x_position = case_id
    if linked_cases == []:
        y_position = 0
    else:
        y_position = len(linked_cases)

    G.add_node(case_id, location=location, report_date=report_date, exposure=exposure, pos=(x_position, y_position))

    # Adding edges to all of the nodes
    if linked_cases != []:
        for j in range(len(linked_cases)):
            if case_id != linked_cases[j]:
                node_edge_pair = (case_id, linked_cases[j])
                G.add_edge(node_edge_pair[0], node_edge_pair[1])

print("Number of NODES: ", G.number_of_nodes())
print("Number of EDGES: ", G.number_of_edges())


def create_network_graph():
    edge_x = []
    edge_y = []
    # rint(G.nodes())
    for edge in G.edges():
        x0, y0 = G.nodes[edge[0]]['pos']
        # print("x0, y0", x0, y0)
        x1, y1 = G.nodes[edge[1]]['pos']
        # print("x1, y1", x1, y1)
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        name='Case Links',
        line=dict(width=0.5, color='#888'),
        hoverinfo='text',
        mode='lines')

    # January Nodes
    jan_node_x = []
    jan_node_y = []
    for jan_node in G.nodes():
        if G.nodes[jan_node]['report_date']['MONTH'] == 'JAN':
            x, y = G.nodes[jan_node]['pos']
            # if G.in_degree(jan_node) and G.out_degree(jan_node) == 0:
            #    y = 0
            jan_node_x.append(x)
            jan_node_y.append(y)

    january_node_trace = go.Scatter(
        x=jan_node_x, y=jan_node_y,
        name='January Cases',
        mode='markers',
        hoverinfo='text',
        marker=dict(size=4))

    # February Nodes
    feb_node_x = []
    feb_node_y = []
    for feb_node in G.nodes():
        if G.nodes[feb_node]['report_date']['MONTH'] == 'FEB':
            x, y = G.nodes[feb_node]['pos']
            # if G.in_degree(feb_node) and G.out_degree(feb_node) == 0:
            #    y = 0
            feb_node_x.append(x)
            feb_node_y.append(y)

    february_node_trace = go.Scatter(
        x=feb_node_x, y=feb_node_y,
        name='February Cases',
        mode='markers',
        hoverinfo='text',
        marker=dict(size=4))

    # March Nodes
    mar_node_x = []
    mar_node_y = []
    for mar_node in G.nodes():
        if G.nodes[mar_node]['report_date']['MONTH'] == 'MAR':
            x, y = G.nodes[mar_node]['pos']
            # if G.in_degree(mar_node) and G.out_degree(mar_node) == 0:
            #    y = 0
            mar_node_x.append(x)
            mar_node_y.append(y)

    march_node_trace = go.Scatter(
        x=mar_node_x, y=mar_node_y,
        name='March Cases',
        mode='markers',
        hoverinfo='text',
        marker=dict(size=4))

    # Color the node points and add hover information
    node_adjacencies = []
    node_text = []
    count = 0
    for node, adjacencies in enumerate(G.adjacency()):
        count += 1  # iterate before indexing since nodes start at 1
        node_adjacencies.append(len(adjacencies[1]))
        node_text.append('Case ID = ' + str(node + 1)
                         + ', Number of linked cases = ' + str(len(adjacencies[1]))
                         + ', Exposure = ' + str(G.nodes[count]['exposure'])
                         + ', Date = ' + str(G.nodes[count]['report_date']['MONTH']) + ', ' + str(
            G.nodes[count]['report_date']['DAY'])
                         + ', Location = ' + str(G.nodes[count]['location']))

    # for node in range(len(node_adjacencies)):

    node_x = []
    node_y = []
    for node in G.nodes():
        x, y = G.nodes[node]['pos']
        # print("x, y", x, y)
        node_x.append(x)
        node_y.append(y)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        name='Cases',
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            # colorscale options
            # 'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
            # 'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
            # 'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
            colorscale='RdBu',
            reversescale=True,
            color=[],
            size=10,
            colorbar=dict(
                thickness=25,
                title='Number of Linked Cases',
                xanchor='center',
                titleside='right'
            ),
            line_width=2))

    # callback function for updating points
    # def update_point(trace, points, selector):

    node_trace.marker.color = node_adjacencies
    node_trace.text = node_text

    fig = go.Figure(data=[edge_trace, node_trace, january_node_trace, february_node_trace, march_node_trace],
                    layout=go.Layout(
                        title='<br> Data Visualization ',
                        titlefont_size=36,
                        showlegend=True,
                        hovermode='closest',
                        margin=dict(b=5, l=40, r=5, t=50),
                        annotations=[dict(
                            showarrow=False,
                            xref="paper", yref="paper",
                            x=0.005, y=- 0.002,
                            text='')],

                        xaxis=dict(title='Case ID', showgrid=True, zeroline=False, showticklabels=True, ticks='outside',
                                   tickson='boundaries', ticklen=10),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))

    app.layout = html.Div([
        html.Div(dcc.Graph(id='Graph', figure=fig))

    ])

    fig.update_layout(legend_title_text='OPTIONS')
    fig.update_layout(legend_bordercolor='black')
    fig.update_layout(legend=dict(
        yanchor='top',
        y=0.99,
        xanchor='left',
        x=0.01
    ))

    fig.update_layout(title=dict(
        yanchor='top',
        y=1.00,
        xanchor='center',
        x=0.45
    ))

    #app.run_server(debug=True)
    # fig.show()


create_network_graph()
