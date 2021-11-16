import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import seaborn as sns
from input import scenarios, detailed, stock, order, colors_attributes, subsidies, color_policies, scenarios_table
from utils import make_dash_table


pd.options.plotting.backend = 'plotly'

app = dash.Dash(__name__, meta_tags=[{'name': 'viewport', 'content': 'width=device-width'}])

app.title = 'Res-IRF User Interface'
server = app.server

with open('assets/description.md', 'r') as f:
    description = f.read()

with open('assets/contacts.md', 'r') as f:
    contacts = f.read()

app.layout = \
    html.Div(
        style={'height': '100%'},  # , 'background': 'white'
        children=[
            # Banner display
            html.Div(
                [
                    html.H2(
                        app.title,
                        id='title',
                        className='eight columns',
                        style={'margin-left': '3%'},
                    )
                ],
                className='banner row',
            ),

            # Description
            html.Div(
                className='container',
                style={'margin-top': '0px', 'margin-bottom': '0px'},
                children=[
                    # html.P(markdown.markdown(description))
                    dcc.Markdown(description)
                ]),

            # Aggregated output - Dropdown buttons and graph
            html.Div(
                className='container',
                # style={'padding': '35px 25px'},
                style={'margin-bottom': '0px'},
                children=[
                    html.H4(
                        'Aggregated output',
                        className='twelve columns',
                        style={'font-weight': 'bold',
                               'margin-left': '2%'}
                    ),
                    html.Div(
                        children=[



                            html.P(
                                'Outputs to display',
                                style={'font-weight': 'bold', 'margin-bottom': '0px'},
                                className='plot-display-text'
                            ),

                            dcc.Dropdown(
                                id='dropdown_to_show',
                                options=[{'label': x, 'value': x} for x in detailed.keys()],
                                value=['Consumption actual (TWh)'],
                                multi=True,
                                placeholder='Select output to display',
                            )],
                        className='six columns dropdown-box-first'
                    ),
                    html.Div(
                        children=[
                            html.P(
                                'Scenarios to display',
                                style={'font-weight': 'bold', 'margin-bottom': '0px'},
                                className='plot-display-text'),
                            dcc.Dropdown(
                                id='dropdown_scenario',
                                options=[{'label': x, 'value': x} for x in scenarios],
                                value=scenarios[:4],
                                multi=True,
                                placeholder='Select scenario',
                            ),
                        ],
                        className='six columns dropdown-box-first'
                    ),
                    html.Div(
                        dcc.Graph(id='line-chart'),
                        className='twelve columns'
                    )
                ]
            ),

            # Stock by attribute - Dropdown buttons and graph
            html.Div(
                className='container',
                # style={'padding': '35px 25px'},
                style={'margin-bottom': '0px'},
                children=[
                    html.H4(
                        'Stock by attributes',
                        className='twelve columns',
                        style={'font-weight': 'bold',
                               'margin-left': '2%'}
                    ),
                    html.Div(
                        children=[
                            html.P(
                                'Scenarios to display',
                                style={'font-weight': 'bold', 'margin-bottom': '0px'},
                                className='plot-display-text'),
                            dcc.Dropdown(
                                id='dropdown_scenario_stock',
                                options=[{'label': x, 'value': x} for x in scenarios],
                                value=scenarios[0],
                                multi=False,
                                placeholder='Select scenario',
                            ),
                        ],
                        className='six columns dropdown-box-first'
                    ),
                    html.Div(
                        children=[

                            html.P(
                                'Attributes',
                                style={'font-weight': 'bold', 'margin-bottom': '0px'},
                                className='plot-display-text'
                            ),

                            dcc.Dropdown(
                                id='dropdown_attributes',
                                options=[{'label': x, 'value': x} for x in order.keys()],
                                value='Energy performance',
                                multi=False,
                                placeholder='Select attributes',
                            )],
                        className='six columns dropdown-box-first'
                    ),

                    html.Div(
                        dcc.Graph(id='stacked-bar-chart'),
                        className='twelve columns'
                    )
                ]
            ),

            # Subsidies - Dropdown buttons and graph
            html.Div(
                className='container',
                # style={'padding': '35px 25px'},
                style={'margin-bottom': '0px'},
                children=[
                    html.H4(
                        'Policies cost',
                        className='twelve columns',
                        style={'font-weight': 'bold',
                               'margin-left': '2%'}
                    ),
                    html.Div(
                        children=[
                            html.P(
                                'Scenarios to display',
                                style={'font-weight': 'bold', 'margin-bottom': '0px'},
                                className='plot-display-text'),
                            dcc.Dropdown(
                                id='dropdown_scenario_subsidies',
                                options=[{'label': x, 'value': x} for x in subsidies.keys()],
                                value=list(subsidies.keys())[0],
                                multi=False,
                                placeholder='Select scenario',
                            ),
                        ],
                        className='six columns dropdown-box-first'
                    ),
                    html.Div(
                        dcc.Graph(id='area-subsidies-chart'),
                        className='twelve columns'
                    )
                ]
            ),

            html.Div(

                children=[
                    html.H6(
                        ['Detailed scenarios displayed']
                    ),

                    dash_table.DataTable(
                        columns=[{"name": i, "id": i} for i in scenarios_table.columns],
                        data=scenarios_table.to_dict('records'),
                        style_as_list_view=True,
                        style_header={
                            'backgroundColor': 'white',
                            'fontWeight': 'bold'
                        },
                        style_cell={'textAlign': 'left',
                                    'font-size': '1rem',
                                    'font_family': 'sans-serif'
                                    },

                    ),
                    html.Br(),
                    dcc.Markdown(contacts)
                ],
                className='container',

            ),

        ]
    )


@app.callback(
    Output('line-chart', 'figure'),
    [
        Input('dropdown_to_show', 'value'),
        Input('dropdown_scenario', 'value')
    ]
)
def update_line_chart(to_show_list, scenario):

    color = sns.color_palette('husl', len(scenarios))
    colors = {to_show: 'rgb{}'.format(color[k]) for k, to_show in enumerate(to_show_list)}

    line = ['solid', 'dash', 'dot', 'longdash', 'dashdot', 'longdashdot'] * 10
    lines = {scenario: line[k] for k, scenario in enumerate(scenarios)}

    data = []
    for to_show in to_show_list:
        temp = detailed[to_show].loc[:, [c for c in detailed[to_show].columns if c in scenario]]
        temp.columns = ['{} - {}'.format(to_show, c) for c in temp.columns]
        data += [temp]
    data = pd.concat(data, axis=1)
    
    colors = {c: colors[c.split(' - ')[0]] for c in data.columns}
    lines = {c: lines[c.split(' - ')[1]] for c in data.columns}

    fig = data.plot(title=', '.join(to_show_list), template='simple_white',
                    labels=dict(index='Years', value=' '))

    temp = {k: fig.data[k].name for k in range(data.shape[1])}
    for key, item in temp.items():
        fig.data[key].line.dash = lines[item]
        fig.data[key].line.color = colors[item]

    fig.update_layout(legend=dict(yanchor='top', orientation='h', x=0, y=-0.5), legend_title_text='Variable - Scenario')

    return fig


@app.callback(
    Output('stacked-bar-chart', 'figure'),
    [
        Input('dropdown_scenario_stock', 'value'),
        Input('dropdown_attributes', 'value')

    ]
)
def update_stacked_bar_chart(scenario, attribute):
    df = stock[scenario].groupby(attribute).sum().loc[order[attribute], :].T
    fig = df.plot(kind='bar', template='simple_white', color_discrete_map=colors_attributes,
                  labels=dict(index='Years', value=' '), title='Stock by {}'.format(attribute))
    return fig


@app.callback(
    Output('area-subsidies-chart', 'figure'),
    [
        Input('dropdown_scenario_subsidies', 'value')
    ]
)
def update_area_subsidies_chart(scenario):
    df = subsidies[scenario] / 10**6
    fig = df.plot(kind='bar', template='simple_white', color_discrete_map=color_policies,
                  labels=dict(index='Years', value=' '),
                  title='Subsidies amount for {} (Millions euro)'.format(scenario)
                  )
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)

