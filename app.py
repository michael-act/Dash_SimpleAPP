import pandas as pd
import numpy as np

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# ------------------------------------------------------------------------------
# Import a clean data (importing csv into pandas)
df = pd.read_csv('All Gender Survey.csv')

# Update 2018 Data
dct_replace = {'F': 'Female', 'M': 'Male'}
for v in 'FM':
	df['2018'].replace(v, dct_replace[v], inplace=True)


# ------------------------------------------------------------------------------
# App layout
colors = {
		'main-background': '#3a6351', 
		'background': '#9ecca4',
		'background-2': '#f1f1e8', 
		'text': '#1c1427', 
		'text-2': '#cee6b4', 
		'line': '#382933', 
		'chart': ["#413c69","#4a47a3","#709fb0","#a7c5eb"]}

app.layout = html.Div(style={'backgroundColor': colors['main-background']}, children=[
	html.Div(
		id='banner', 
		children=[
			html.Img(
				id='logo', 
				src="https://miro.medium.com/max/392/1*L7lrXBkGa4dsavxds0MjaA.png", 
				style={'margin': 20, 'height': '10%', 'width': '10%'}
				), 
			html.H1(
				id='title', 
				children='Summary of Gender | IT Salary Survey', 
				style={'margin': 20, 'color': colors['text'], 'text-shadow': '1px 1px 2px #382933'}
				)
			],
		className='row',
		style={'height' : '4%', 
				'background-color' : colors['background'], 
				'border-block-end': '1rem solid', 
				'writing-mode': 'horizontal-tb'}
	), 

	dcc.Slider(
        id='slct-year',
        min=2018,
        max=2020,
        value=2019,
        marks={int(f'20{y}'): {'label': f'20{y}', 
        		'style': {
        			'color': colors['background'], 
        			'font-size': 14, 
        			'font-weight': 'bold'}} 
        		for y in range(18, 21)}
    ),

	# dcc.Dropdown(
	# 	id='slct-year', 
	# 	options=[
	# 		{'label': '2018', 'value': '2018'},
	# 		{'label': '2019', 'value': '2019'},
	# 		{'label': '2020', 'value': '2020'}], 
	# 	value='2019',  # Default value
	# 	style={'margin': 20, 'width': '35%'}
	# ), 

	html.Center(
		children=[dcc.Graph(
				id='pie-graph',
				figure={'layout': dict(width=758, height=512)}
				), 
			]
	), 

	html.Div(
		children=[dcc.Graph(
				id='bar-graph',
				figure={}
				)
			], 
		className='row',
		style={'height' : '4%', 'background-color' : colors['background-2']}
	), 
	html.H6(
		children=[dcc.Markdown(
				id='conclusion', 
				children=[]
				)], 
		style={'margin': 20, 'color': colors['text-2']}
	), 
	html.Br()
])


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
	[Output(component_id='pie-graph', component_property='figure'), 
	Output(component_id='bar-graph', component_property='figure'), 
	Output(component_id='conclusion', component_property='children')], 
	[Input(component_id='slct-year', component_property='value')]
	# Input() is Connected to parameter update_graph() function.
	# Output() is Connected to returned value update_graph() function.
)

def update_graph(option_slctd):
	option_slctd = str(option_slctd)
	year = ['2018', '2019', '2020']
	year.remove(option_slctd)

	dfcnt = df[option_slctd].value_counts()

	# Find difference, then give color and status based on value
	diff = {
		year[0]: np.array([
			dfcnt.loc['Male'] - df[year[0]].value_counts().loc['Male'], 
			dfcnt.loc['Female'] - df[year[0]].value_counts().loc['Female']
			]), 
		year[1]: np.array([
			dfcnt.loc['Male'] - df[year[1]].value_counts().loc['Male'], 
			dfcnt.loc['Female'] - df[year[1]].value_counts().loc['Female']
			])
	}

	color_diff = {
		year[0]: np.where(diff[year[0]] < 0, '#aa2b1d', '#1f441e'), 
		year[1]: np.where(diff[year[1]] < 0, '#aa2b1d', '#1f441e')
	}

	status_diff = {
		year[0]: np.where(diff[year[0]] < 0, 'Decreasing', 'Increasing'), 
		year[1]: np.where(diff[year[1]] < 0, 'Decreasing', 'Increasing')
	}

	# Plotly Pie
	figPie = go.Figure()

	figPie.add_trace(go.Pie(
			labels=dfcnt.index, 
			values=dfcnt.values, 
			marker={
				'colors': colors['chart'], 
				'line': {
					'color': colors['line'], 
					'width': 0.5}}
			)
		)

	figPie.update_layout(
					# title=f'Proportional of Gender in {option_slctd}', 
					# title_x=0.5, 
					# title_font_size=28, 
					plot_bgcolor=colors['background'], 
					paper_bgcolor=colors['background'], 
					font_color=colors['text'], 
					uniformtext_minsize=8, 
					uniformtext_mode='hide')


	# Plotly Bar Chart
	figBar = make_subplots(
	    rows=1, cols=2,
	    specs=[[{'type': 'bar'}, {'type': 'bar'}]], 
	    subplot_titles=(f"{year[0]}", f"{year[1]}")
	    )

	figBar.add_trace(
		go.Bar(
			name=year[0],
			x=dfcnt.index, 
			y=diff[year[0]], 
			text=diff[year[0]], 
			textposition='auto',
			marker_color=color_diff[year[0]]
			), 
		row=1, col=1)

	figBar.add_trace(
		go.Bar(
			name=year[1],
			x=dfcnt.index, 
			y=diff[year[1]], 
			text=diff[year[1]], 
			textposition='auto', 
			marker_color=color_diff[year[1]]
			),
		row=1, col=2)

	figBar.update_layout(
					title=f'Difference of Gender by Year', 
					title_x=0.5, 
					title_font_size=28, 
					plot_bgcolor=colors['background'], 
					paper_bgcolor=colors['background'], 
					font_color=colors['text'], 
					showlegend= False)

	# Summary info: Increasing or Decreasing
	conclusion = []
	for y in status_diff:
		for i, g in enumerate(['Male', 'Female']):
			conclusion.append(f'> {option_slctd} vs {y} {g}: **{status_diff[y][i]}**')
	conclusion.insert(2, '---')
	conclusion = '\n\n'.join(conclusion)

	return figPie, figBar, conclusion


# ------------------------------------------------------------------------------
if __name__ == '__main__':
	app.run_server(debug=True)