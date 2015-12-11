import plotly.plotly as py
import plotly.graph_objs as go

# prepare lists of brand names and their purchase frequency
def brand_frequency(gender):
    gender_brands, gender_brands_count = [], []

    with open('%s_brands_filtered.txt' % (gender), 'r') as f:
        gender_data = f.readlines()

    for data in gender_data:
        splited = data.split(' ', 1)
        count, brand = int(splited[0]), splited[1].strip("\n")

        gender_brands.append(brand)
        gender_brands_count.append(count)

    return {'brands': gender_brands, 'count': gender_brands_count}

male_content = brand_frequency('male')
female_content = brand_frequency('female')

trace1 = go.Bar(
    x=male_content['brands'],
    y=male_content['count'],
    name='Male',
    marker=dict(
        color='rgb(55, 83, 109)'
    )
)

trace2 = go.Bar(
    x=female_content['brands'],
    y=female_content['count'],
    name='Female',
    marker=dict(
        color='rgb(26, 118, 255)'
    )
)
data = [trace1, trace2]
layout = go.Layout(
    title='Gender Segmentation of brands',
    xaxis=dict(
        tickfont=dict(
            size=12,
            color='rgb(107, 107, 107)'
        )
    ),
    yaxis=dict(
        title='Orders',
        titlefont=dict(
            size=12,
            color='rgb(107, 107, 107)'
        ),
        tickfont=dict(
            size=12,
            color='rgb(107, 107, 107)'
        )
    ),
    legend=dict(
        x=1.0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15,
    bargroupgap=0.1
)
fig = go.Figure(data=data, layout=layout)
plot_url = py.plot(fig, filename='gender-segmentation-bar')
