import pandas as pd
import pickle
from whitenoise import Whitenoise
with open('tables.pickle', 'rb') as handle:
    dfs = pickle.load(handle)

#hide_input
import dash
from dash.dependencies import Input, Output
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
s = 1
app.layout = html.Div([
    html.H1('Dash Tabs component demo'),
    dcc.Tabs(id="tabs-example-graph",
             value='tab-1-example-graph',
             children=[
                 dcc.Tab(label='Season 1', value='tab-1-example-graph'),
                 dcc.Tab(label='Season 2', value='tab-2-example-graph'),
                 dcc.Tab(label='Season 3', value='tab-3-example-graph'),
                 dcc.Tab(label='Season 4', value='tab-4-example-graph'),
                 dcc.Tab(label='Season 5', value='tab-5-example-graph'),
                 dcc.Tab(label='Season 6', value='tab-6-example-graph'),
                 dcc.Tab(label='Season 7', value='tab-7-example-graph'),
                 dcc.Tab(label='Season 8', value='tab-8-example-graph'),
             ]),
    html.Div([
        dash_table.DataTable(
            id='datatable-interactivity',
            columns=[{
                "name": i,
                "id": i,
                "deletable": True,
                "selectable": True
            } for i in dfs[s].columns],
            data=dfs[s].to_dict('records'),
            editable=True,
            filter_action="native",
            sort_action="native",
            sort_mode="multi",
            column_selectable="single",
            row_selectable="multi",
            row_deletable=True,
            selected_columns=[],
            selected_rows=[],
            page_action="native",
            page_current=0,
            page_size=10,
        ),
        html.Div(id='datatable-interactivity-container')
    ])
])


@app.callback(Output('datatable-interactivity', 'data'),
              Input('tabs-example-graph', 'value'))
def render_content(tab):
    s = int(tab.split('-')[1])
    return dfs[s].to_dict('records')


@app.callback(Output('datatable-interactivity', 'style_data_conditional'),
              Input('datatable-interactivity', 'selected_columns'))
def update_styles(selected_columns):
    return [{
        'if': {
            'column_id': i
        },
        'background_color': '#D2F3FF'
    } for i in selected_columns]


@app.callback(Output('datatable-interactivity-container', "children"),
              Input('datatable-interactivity', "derived_virtual_data"),
              Input('datatable-interactivity',
                    "derived_virtual_selected_rows"))
def update_graphs(rows, derived_virtual_selected_rows):
    # When the table is first rendered, `derived_virtual_data` and
    # `derived_virtual_selected_rows` will be `None`. This is due to an
    # idiosyncrasy in Dash (unsupplied properties are always None and Dash
    # calls the dependent callbacks when the component is first rendered).
    # So, if `rows` is `None`, then the component was just rendered
    # and its value will be the same as the component's dataframe.
    # Instead of setting `None` in here, you could also set
    # `derived_virtual_data=df.to_rows('dict')` when you initialize
    # the component.
    if derived_virtual_selected_rows is None:
        derived_virtual_selected_rows = []

    dff = dfs[s] if rows is None else pd.DataFrame(rows)

    colors = [
        '#7FDBFF' if i in derived_virtual_selected_rows else '#0074D9'
        for i in range(len(dff))
    ]

    return [
        dcc.Graph(
            id=column,
            figure={
                "data": [{
                    "x": dff["Character name"],
                    "y": dff[column],
                    "type": "bar",
                    "marker": {
                        "color": colors
                    },
                }],
                "layout": {
                    "xaxis": {
                        "automargin": True
                    },
                    "yaxis": {
                        "automargin": True,
                        "title": {
                            "text": column
                        }
                    },
                    "height": 250,
                    "margin": {
                        "t": 10,
                        "l": 10,
                        "r": 10
                    },
                },
            },
        )
        # check if column exists - user may have deleted it
        # If `column.deletable=False`, then you don't
        # need to do this check.
        for column in ["In degree", "Out degree", "Closeness centrality"]
        if column in dff
    ]


server = app.server
server.wsgi_app = WhiteNoise(server.wsgi_app, root='static/')
