import plotly
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
import dash_table
from dash.dependencies import Input, Output, State

tsa = pd.read_csv('tsa_claims_dashboard_ujian.csv')
external_stylesheets = ['https://codepen.io/chiddyp/pen/bWLwP.css']

app = dash.Dash(__name__, external_stylesheets = external_stylesheets)

def generate_table(dataframe, page_size=10, claimsite_val=''):
    if claimsite_val == '':
        dataframe = dataframe
    else:
        dataframe = dataframe[(dataframe['Claim Site'] == claimsite_val)]

    return dash_table.DataTable(
        id='dataTable',
        columns=[{
            'name' : i,
            'id' : i
        } for i in dataframe.columns],
        data=dataframe.to_dict('records'),
        page_action='native',
        page_current = 0,
        page_size = page_size,
        style_table={'overflowX': 'scroll'}
    )


app.layout = html.Div(children=[
        html.H1('Ujian Modul 2 Dashboard TSA'),

        html.Div(children='''
            Created by: Cornellius 
    '''),
    dcc.Tabs(children = [
        dcc.Tab(value = 'Tab 1', label = 'DataFrame Table', children = [
            html.H1('DATAFRAME TSA'),
            html.Div([
                html.P('Claim Site'),
                dcc.Dropdown(value='',
                            id='filter-claimsite',
                            options=[{'label' : 'Checked Baggage', 'value' : 'Checked Baggage'},
                                    {'label' : 'Checkpoint', 'value' : 'Checkpoint'},
                                    {'label' : 'Other', 'value' : 'Other'},
                                    {'label' : 'Motor Vehicle', 'value' : 'Motor Vehicle'},
                                    {'label' : 'Bus station', 'value' : 'Bus station'},
                                    {'label' : 'All', 'value' : ''}]
                            )
            ], className = 'col-3'),
            html.Div([
                html.P('Max Rows'),
                dcc.Input(id='filter-row', type='number', value=10),
                html.Br(),
                html.Button('Search', id='filter')
            ], className = 'col-3'),
            html.Div(id = 'div-table', children = [generate_table(tsa)])
        ]),
        dcc.Tab(value = 'Tab 2', label = 'Bar-Chart', children = [
            html.Div([
            html.Div([
                html.P('Y1'),
                dcc.Dropdown(value='',
                            id='filter-Y1',
                            options=[{'label' : 'Claim Amount', 'value' : 'Claim Amount'},
                                    {'label' : 'Close Amount', 'value' : 'Close Amount'},
                                    {'label' : 'Day Differences', 'value' : 'Day Differences'},
                                    {'label' : 'Amount Differences', 'value' : 'Amount Differences'}]
                            )
            ], className = 'col-3'),
            html.Div([
                html.P('Y2'),
                dcc.Dropdown(value='',
                            id='filter-Y2',
                            options=[{'label' : 'Claim Amount', 'value' : 'Claim Amount'},
                                    {'label' : 'Close Amount', 'value' : 'Close Amount'},
                                    {'label' : 'Day Differences', 'value' : 'Day Differences'},
                                    {'label' : 'Amount Differences', 'value' : 'Amount Differences'}]
                            )
            ], className = 'col-3'),
            html.Div([
                html.P('X'),
                dcc.Dropdown(value='',
                            id='filter-X',
                            options=[{'label' : 'Claim Type', 'value' : 'Claim Type'},
                                    {'label' : 'Claim Site', 'value' : 'Claim Site'},
                                    {'label' : 'Disposition', 'value' : 'Disposition'}]
                            )
            ], className = 'col-3'),
            ], className = 'row')
        ]),
        dcc.Tab(value = 'Tab 3', label = 'Scatter Chart', children = [
            html.Div(children = dcc.Graph(
                        id = 'graph-scatter',
                        figure = {'data': [
                            go.Scatter(
                                x = tsa[tsa['Claim Type'] == i]['Claim Amount'],
                                y = tsa[tsa['Claim Type'] == i]['Close Amount'],
                                mode = 'markers',
                                name = '{}'.format(i)
                            ) for i in tsa['Claim Type'].unique()
                        ],
                        'layout':go.Layout(
                            xaxis = {'title' : 'Claim Amount'},
                            yaxis = {'title' : 'Close Amount'},
                            hovermode = 'closest'
                        )
                    }
                ), className = 'col-12'),
        ]),
        dcc.Tab(value = 'Tab 4', label = 'Pie-Chart', children = [
            html.Div([
                dcc.Dropdown(value='',
                            id='filter-pie',
                            options=[{'label' : 'Claim Amount', 'value' : 'Claim Amount'},
                                    {'label' : 'Close Amount', 'value' : 'Close Amount'},
                                    {'label' : 'Day Differences', 'value' : 'Day Differences'},
                                    {'label' : 'Amount Differences', 'value' : 'Amount Differences'}]
                            )
            ], className = 'col-3'),
            # html.Div(children = dcc.Graph(
            #             id = 'graph-pie',
            #             figure = {'data': [
            #                 go.Pie(
            #                     values = [tsa[tsa['Claim Type']==i]['Claim Type'].mean() for i in tsa['Claim Type'].unique()],
            #                 )
            #             ],
            #             'layout':go.Layout(
            #                 title = 'Mean Pie Chart',
            #                 hovermode = 'closest'
            #             )
            #         }
            #     ), className = 'col-10')
        ]),
    ])
])

@app.callback(
    Output(component_id = 'div-table', component_property='children'),
    [Input(component_id = 'filter', component_property='n_clicks')],
    [State(component_id = 'filter-claimsite', component_property='value')]
)

def update_table(n_clicks, row, claimsite_val):
    children = [generate_table(tsa, page_size=row, claimsite_val=claimsite_val)]
    return children


if __name__ == '__main__':
    app.run_server(debug=True)

