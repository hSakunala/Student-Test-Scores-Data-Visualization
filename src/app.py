import dash
from dash import dcc, html, Input,Output
import seaborn as sns
import plotly.express as px
from dash.exceptions import PreventUpdate
import pandas as pd


student_df=pd.read_csv('study_performance.csv')

# Get the categorical columns
categorical_columns = student_df.select_dtypes(include=['object']).columns.tolist()

# Get the numeric columns
numeric_columns = student_df.select_dtypes(include=['number']).columns.tolist()

#graph1 components
dropdown1=html.Div(className="child1_1_1",children=[dcc.Dropdown(id='x-axis-dropdown',options=categorical_columns, value=categorical_columns[0])])
dropdown2=html.Div(className="child1_1_2",children=[dcc.Dropdown(id='y-axis-dropdown',options=numeric_columns, value=numeric_columns[0])])

#graph2 components
radio1=html.Div(className="child1_1_1",children=[dcc.RadioItems(id='radio', options=numeric_columns, value=numeric_columns[0], inline=True)])

#graph3 components
dropdown3=html.Div(className="child1_1_1",children=[dcc.Dropdown(id='x-axis-dropdown1',options=numeric_columns, value=numeric_columns[0])])
dropdown4=html.Div(className="child1_1_2",children=[dcc.Dropdown(id='y-axis-dropdown1',options=categorical_columns, value=categorical_columns[0])])
slider1= html.Div(className="child1_1_2",children=[dcc.Slider(id='slider1', min=0, max=100, step=1, value=50, marks={i: str(i) for i in range(0,101,10)})])

#graph4 components
checklist1=html.Div(className="child1_1_1",children=[dcc.Checklist(id='checklist1', options=numeric_columns, value=numeric_columns[0:], inline=True)])

app = dash.Dash(__name__)

server = app.server

app.layout = html.Div(className="parent", children=[
    html.Div(className="child1",children=[html.Div([dropdown1, dropdown2], className="child1_1"),
                                          html.Div(dcc.Graph(id='graph1'), className="child1_2"),
                                          html.Div([dropdown3,dropdown4,slider1], className="child1_1"),
                                          html.Div(dcc.Graph(id='graph3'), className="child1_2" )]),
    html.Div(className="child2",children=[html.Div(radio1, className="child2_1"),
                                          html.Div(dcc.Graph(id='graph2'), className="child2_2"),
                                          html.Div(checklist1, className="child1_1"),
                                          html.Div(dcc.Graph(id='graph4'), className="child2_2")])
])

# Define callback function for graph1
@app.callback(Output('graph1', 'figure'), [Input('x-axis-dropdown', 'value'),Input('y-axis-dropdown', 'value')])
def update_graph(x_axis_column, y_axis_column):
    avg_y = student_df.groupby(x_axis_column)[y_axis_column].mean().reset_index()
    figure = px.bar(avg_y, x=x_axis_column, y=y_axis_column,text_auto=True)
    figure.update_layout(plot_bgcolor="#f7f7f7")
    figure.update_yaxes(title_text=y_axis_column+' (average)')
    figure.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)', marker_line_width=1.5, opacity=0.6)
    return figure


#Define callback function for graph 2
@app.callback(Output('graph2', 'figure'),Input('radio', 'value'))
def update_graph(selected_value):
    figure = px.histogram(student_df, x=selected_value, labels={'x': selected_value, 'y': 'Score' }, title='Student Scores')
    figure.update_layout(plot_bgcolor="#f7f7f7")
    figure.update_traces(marker_line_width=1,marker_line_color="white")
    figure.update_yaxes(title_text='Score')
    return figure

#Define callback function for graph 3
@app.callback(Output('graph3', 'figure'), [Input('x-axis-dropdown1', 'value'),Input('y-axis-dropdown1', 'value'),Input('slider1', 'value')])
def update_graph(x_axis_column, y_axis_column, slider_value):
    filtered_df = student_df[student_df[x_axis_column] <= slider_value]
    figure = px.strip(filtered_df, x=x_axis_column, y=y_axis_column, color=y_axis_column, title='Student Scores equal to or below ' +  str(slider_value))
    figure.update_layout(plot_bgcolor="#f7f7f7")
    figure.update_traces(marker_line_width=0.8, opacity=0.9)
    return figure

#Define callback function for graph 4
@app.callback(Output('graph4', 'figure'),Input('checklist1', 'value'))
def update_graph(selected_values):
    avg_scores = student_df[selected_values].mean().reset_index()
    figure = px.pie(avg_scores, values=avg_scores[0], names='index', title='Average Scores comparison for columns: '+ ', '.join(selected_values), 
                    hole=0.3, color_discrete_sequence=px.colors.sequential.RdBu)
    figure.update_layout(plot_bgcolor="#f7f7f7")
    return figure 


                    


if __name__ == '__main__':
    app.run_server(debug=True)

