from plotly import tools
import plotly.plotly as py
import plotly.graph_objs as go
import pandas as pd

df = pd.read_csv('./location-warehouse.csv')

colors = ["rgb(0,116,217)","rgb(255,65,54)"]
limits = [0, 8, len(df.index)]

cities = []
rows = df.iterrows()

for i in range(len(limits) - 1):
    row = rows.next()
    sub = df[limits[i]:limits[i+1]]

    city = dict(
        type = 'scattergeo',
        locationmode = 'country names',
        lon = sub['lng'],
        lat = sub['lat'],
        text = sub['place'],
        marker = dict(
            size = 10,
            color = colors[i],
            line = dict(width=0.5, color='rgb(40,40,40)'),
            sizemode = 'area'
        ),
        name = sub['courier'].iloc[0] )
    cities.append(city)

layout = dict(
        title = 'Outsourced Logistic Partners',
        showlegend = True,
        geo = dict(
            scope='asia',
            projection=dict( type='mercator' ),
            showland = True,
            landcolor = 'rgb(217, 217, 217)',
            subunitwidth=1,
            countrywidth=1,
            subunitcolor="rgb(255, 255, 255)",
            countrycolor="rgb(255, 255, 255)",
            lonaxis = dict( range= [67.76, 97.73] ),
            lataxis = dict( range= [5.18, 36.11] ),
        ),
    )

fig = dict( data=cities, layout=layout )
url = py.plot( fig, validate=False, filename='outsourced-logistics' )