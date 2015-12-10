import plotly.plotly as py
import plotly.graph_objs as go

same_day_delivery = go.Scatter(
	x=[0],
	y=[330],
	mode='markers+text',
	text=['Same Day Delivery'],
	textposition='middle right',
	name=''
)

tardy_delivery = go.Scatter(
    x=[108],
    y=[1],
    mode='markers+text',
    text=['Miscommunication showing manual execution'],
    textposition='top left',
    fill='rgba(240,0,0,0.6)',
    name=''
)

general_delivery = go.Scatter(
    x=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 22, 24, 28, 35, 38],
    y=[795, 1062, 1340, 1080, 731, 440, 253, 134, 74, 48, 21, 11, 6, 9, 7, 4, 5, 3, 3, 1, 1, 1, 1, 1, 1],
    mode='markers+line',
    name=''
)
data = [same_day_delivery, general_delivery, tardy_delivery]
layout = go.Layout(
	title='How long does it takes to deliver the orders?',
	xaxis=dict(
        title="Delivery Duration (Days)"
    ),
    yaxis=dict(
        title="Orders"
    ),
    shapes = [
        {
            'type': 'rect',
            'xref': 'x',
            'yref': 'paper',
            'x0': 0,
            'y0': 0,
            'x1': 5,
            'y1': 1,
            'fillcolor': '#d3d3d3',
            'opacity': 0.2,
            'line': {
                'width': 0,
            }
        },
        {
            'type': 'rect',
            'xref': 'x',
            'yref': 'paper',
            'x0': 16,
            'y0': 0,
            'x1': 38,
            'y1': 1,
            'fillcolor': '#f3abab',
            'opacity': 0.2,
            'line': {
                'width': 0,
            }
        }
    ],
    showlegend=False
)

fig = go.Figure(data=data, layout=layout)
py.plot(fig, filename='delivery-time')