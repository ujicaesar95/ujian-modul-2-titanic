# import os

import dash
import dash_core_components as dcc 
import dash_html_components as html  
import pandas as pd  
import plotly.graph_objs as go  
from dash.dependencies import Input, Output
import numpy as np
from sqlalchemy import create_engine

engine=create_engine("mysql+mysqlconnector://root:Ujicaesar95@localhost/titanic?host=localhost?port3306")
conn=engine.connect()

results=conn.execute('SELECT * FROM titanic').fetchall()
Titanic=pd.DataFrame(results)
Titanic.columns=results[0].keys()


results=conn.execute('SELECT * FROM titanicoutcalc;').fetchall()
TitanicOutCalc=pd.DataFrame(results)
TitanicOutCalc.columns=results[0].keys()


app = dash.Dash(__name__)
server = app.server 


app.title='Titanic Dashboard by Fauzy Caesarrochim' # set web title

app.layout = html.Div(className='utama',children=[
    dcc.Tabs(id="Tabs",value='tab-1',children=[
        dcc.Tab(label='Ujian Titanic Database', value='tab-1', children=[
            #isi Tab 1
            html.Table(className='ddl-table', children=[
                html.Tr([
                    html.Td([
                        dcc.Dropdown(
                            id='ddl-table',
                            options=[{'label': 'Titanic', 'value': 'Titanic'},
                                    {'label': 'Titanic Outlier Calculation', 'value': 'TitanicOutCalc'}],
                            value='Titanic'
                        )
                    ]),
                ]),
            ]),
            html.Div(id='dataset-container')
        ]),
        dcc.Tab(label='Categorical Plot', value='tab-2', children=[
            html.H1('Categorical Plot Ujian Titanic'),
            html.Table(id='ddl-categorical', children=[
                html.Tr([
                    html.Td([
                        html.P('Jenis :'),
                        dcc.Dropdown(
                            id='ddl-jenis',
                            options=[{'label': 'Bar', 'value': 'bar'},
                                    {'label': 'Violin', 'value': 'violin'},
                                    {'label': 'Box', 'value': 'box'}],
                            value='bar'
                        )
                    ]),
                    html.Td([
                        html.P('X Axis :'),
                        dcc.Dropdown(
                            id='ddl-x',
                            options=[{'label': 'Survived', 'value': 'survived'},
                                    {'label': 'Sex', 'value': 'sex'},
                                    {'label': 'Ticket Class', 'value': 'class'},
                                    {'label': 'Embark Town', 'value': 'embark_town'},
                                    {'label': 'Who', 'value': 'who'},
                                    {'label': 'Outlier', 'value': 'outlier'}],
                            value='sex'
                        )
                    ])
                ])
            ],style={'width':'700px','margin':'0 auto'}),
            dcc.Graph(
                id='categoricalPlot',
                figure={}
            )
        ]),
    ],style={
        'fontFamily':'system-ui'
    },
    content_style={
        'fontFamily':'Arial',
        'borderLeft':'1px solid #d6d6d6',
        'borderRight':'1px solid #d6d6d6',
        'borderBottom':'1px solid #d6d6d6',
        'padding':'44px'
    })
])

@app.callback(
    Output('dataset-container','children'),
    [Input('ddl-table','value')]
)
def table(ddlinput):
    if (ddlinput=='Titanic'):
        data=Titanic
    else:
        data=TitanicOutCalc
    return [
        html.H1('Table '+ ddlinput),
        html.H4('Total Row : '+str(len(data))),
        dcc.Graph(
            id='tableData',
            figure={
                'data':[go.Table(
                    header=dict(
                        values=['<b>' +col.capitalize() + '</b>' for col in data.columns],
                        fill = dict(color='#C2D4FF'),
                        font = dict(size=17),
                        height = 30,
                        align = ['center'] ),
                    cells=dict(
                        values=[data[col] for col in data.columns],
                        fill = dict(color='#F5F8FF'),
                        font = dict(size=15),
                        height = 25,
                        align = ['right'] * 5)
                )],
                'layout': dict(height=500,margin={'l': 40, 'b': 40, 't': 10, 'r': 10})
            }
        )
    ]

@app.callback(
    Output('categoricalPlot','figure'),
    [Input('ddl-jenis','value'),
    Input('ddl-x','value')]
)
def caterPlot(ddlJenis,ddlX):
    listPlot={
        'bar':go.Bar,
        'violin':go.Violin,
        'box':go.Box
    }
    
    return {'data':[listPlot[ddlJenis](
                        x=Titanic[ddlX],
                        y=Titanic['fare'],
                        text=Titanic['deck'],
                        opacity=0.7,
                        name='Fare',
                        marker=dict(color='blue'),
                        legendgroup='fareage'
                    ),
            listPlot[ddlJenis](
                        x=Titanic[ddlX],
                        y=Titanic['age'],
                        text=Titanic['deck'],
                        opacity=0.7,
                        name='Age',
                        marker=dict(color='orange'),
                        legendgroup='fareage'
                    )],
            'layout': go.Layout(
                    xaxis={'title': ddlX.capitalize()}, yaxis={'title': 'Fare (US$), Age (Year)'},
                    margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                    # legend={'x': 0, 'y': 1}, 
                    hovermode='closest',
                    boxmode='group',violinmode='group'
                    # plot_bgcolor= 'black', paper_bgcolor= 'black',
                )
    }
if __name__ == '__main__': 
    #run server on port 1997
    #debug=True for auto restart if code edited
    app.run_server(debug=True, port=1996)
