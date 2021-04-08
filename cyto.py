
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
        marker=dict(size=4),
        visible='legendonly')
        

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
        marker=dict(size=4),
        visible='legendonly')

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
        marker=dict(size=4),
        visible='legendonly')


"""
#for each value on the y-axis will represent a new location for a case (cases will be linked with location)
def calculate_location():
    unique_locations = []
    for i in range(len(data['DATA'])):
        if data['DATA'][i]['LOCATION'] not in unique_locations:
            unique_locations.append(data['DATA'][i]['LOCATION'])
    return unique_locations


G = nx.Graph()
node_edge_pair = []
for i in range(len(data["DATA"])):

    case_id = data["DATA"][i]["CASE_ID"]
    linked_cases = data["DATA"][i]["LINKED_CASES"]
    location = data["DATA"][i]["LOCATION"]
    report_date = data["DATA"][i]["REPORT_DATE"]
    exposure = data["DATA"][i]["EXPOSURE"]
    
    #set the x-position of nodes to the dat of the case
    x_position = case_id
    
    #set the y-position to a unique y-position based on the index of the location in calculate_location()
    if location in calculate_location():
        y_position = calculate_location().index(location)
    elif location == '':
        y_position = 0
    elif exposure == 'IMPORTED' and linked_cases == []:
        y_postion = -1
    

    G.add_node(case_id, location=location, report_date=report_date, exposure=exposure, pos=(x_position, y_position))

    # Adding edges to all of the nodes
    if linked_cases != []:
        for j in range(len(linked_cases)):
            if case_id != linked_cases[j]:
                node_edge_pair = (case_id, linked_cases[j])
                G.add_edge(node_edge_pair[0], node_edge_pair[1])

print("Number of NODES: ", G.number_of_nodes())
print("Number of EDGES: ", G.number_of_edges())




edge_x = []
edge_y = []
for edge in G.edges():
    x0, y0 = G.nodes[edge[0]]['pos']
    x1, y1 = G.nodes[edge[1]]['pos']
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
                        + ', Date = ' + str(G.nodes[count]['report_date']['MONTH']) 
                        + ', ' + str(G.nodes[count]['report_date']['DAY'])
                        + ', Location = ' + str(G.nodes[count]['location']))

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

node_trace.marker.color = node_adjacencies
node_trace.text = node_text






#####################################################################
#                                                                   #
#                 Creating The Initial Figure                       #
#                                                                   #
#####################################################################
fig = go.Figure(data=[edge_trace, node_trace],
    layout=go.Layout(
        titlefont_size=36,
        showlegend=True,
        hovermode='closest',
        margin=dict(b=5, l=40, r=5, t=50),
        annotations=[dict(
            showarrow=False,
            xref="paper", yref="paper",
            x=0.005, y=- 0.002,
            text='')],

        xaxis=dict(title='Date of Identified Case', 
                showgrid=True,
                gridwidth=1,
                gridcolor='black',
                zeroline=False,
                color='black',
                linecolor='black',
                mirror=True,
                
                showticklabels=True,
                tickmode = 'array',
                tickvals = [1, 17, 103], #january, february, march
                ticktext = ['JAN', 'FEB', 'MAR']),
                    
        yaxis=dict(
                showgrid=False,
                zeroline=False,
                color='black',
                linecolor='black',
                mirror=True,

                showticklabels=False
                )))


fig.update_layout(legend_title_text='Months')
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

fig.update_layout(clickmode='event+select')


#calculate the length of the slider given the number of days / months in data
def slider_dates():
    list_of_unique_dates=[]
    for i in range(len(data['DATA'])):
        if data['DATA'][i]['REPORT_DATE'] not in list_of_unique_dates:
            list_of_unique_dates.append(data['DATA'][i]['REPORT_DATE'])
    return list_of_unique_dates
    

#App layout
app.layout = html.Div(children=[
    html.H1('Singapore Data Visualization'),
    html.Div('Network graph indicating unique cases and their respective connections throughout the begining months of the COVID-19 pandemic in 2020.'),
    dcc.Graph(
        id='graph',
        figure=fig
    ),
    dcc.Slider(
        id='date-slider',
        min=1,
        max=len(data['DATA']),
        step=1,
        drag_value=1,
        marks={
            #1: slider_dates()[0]['MONTH'] + ' ' + str(slider_dates()[0]['DAY']),
            #int(len(slider_dates())*0.25): str(slider_dates()[int(len(slider_dates())*0.25)]),
            #int(len(slider_dates())*0.5): str(slider_dates()[int(len(slider_dates())*0.5)]),
            #int(len(slider_dates())*0.75): str(slider_dates()[int(len(slider_dates())*0.75)]),
            #len(slider_dates()): slider_dates()[len(slider_dates())-1]['MONTH'] + ' ' + str(slider_dates()[len(slider_dates())-1]['DAY'])
            #1: data['DATA'][0]['REPORT_DATE'],
            #len(data['DATA']): data['DATA'][len(data['DATA'])-1]['REPORT_DATE']
        }
        
        #marks={i: str(slider_dates()[i]['MONTH']) + str(slider_dates()[i]['DAY']) for i in range(len(slider_dates()))}
    ),
    html.Div(id='slider-date-container'),
    html.Div(children=[
        html.H2('Looking at this node in graph'),
        html.Pre(id='hover-data', style=styles['pre'])
    ])
])



#slider update and display date below slider bar callback function
@app.callback(
Output('slider-date-container', 'children'),
Input('date-slider', 'drag_value'))
def update_date_container(drag_value):
    try:
        container = 'Selected Date: ' + data['DATA'][drag_value-1]['REPORT_DATE']['MONTH'] + ' ' + str(data['DATA'][drag_value-1]['REPORT_DATE']['DAY'])
        return container
    except TypeError:
        pass

@app.callback(
Output('hover-data', 'children'),
Input('graph', 'hoverData'))
def update_hover_data(hover_data):
    try:
        hover_data_content = hover_data['points'][0]['text']
        return json.dumps(hover_data_content, indent=2)
    except TypeError:
        pass

app.run_server(debug=True)





















@app.callback(
Output('graph', 'figure'),
Input('date-slider', 'drag_value'))
def update_figure(drag_value):
    try:
        node_x = []
        node_y = []
        for node in G.nodes():
            if data['DATA'][drag_value-1]['REPORT_DATE'] == G.nodes[drag_value]['report_date']:
                x, y = G.nodes[node]['pos']
                node_x.append(x)
                node_y.append(y)
        print(data['DATA'][drag_value-1]['REPORT_DATE'], G.nodes[drag_value]['report_date']) #now equal the same thing... finally :)

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

        fig = go.Figure(data=[node_trace])
        return fig
    except TypeError:
        pass
"""

