import plotly.plotly as py
import plotly.graph_objs as go

trace1 = go.Bar(
    y=['Courier Share'],
    x=[8893],
    name='Myntra Logistics',
    orientation = 'h',
    marker = dict(
        color = 'rgba(55, 128, 191, 0.6)',
        line = dict(
            color = 'rgba(55, 128, 191, 1.0)',
            width = 1,
        )
    )
)
trace2 = go.Bar(
    y=['Courier Share'],
    x=[1523],
    name='EKart Logistics',
    orientation = 'h',
    marker = dict(
        color = 'rgba(255, 153, 51, 0.6)',
        line = dict(
            color = 'rgba(255, 153, 51, 1.0)',
            width = 1,
        )
    )
)
trace3 = go.Bar(
    y=['Courier Share'],
    x=[468],
    name='Delhivery',
    orientation = 'h',
    marker = dict(
        color = 'rgba(155, 253, 51, 0.6)',
        line = dict(
            color = 'rgba(155, 253, 51, 1.0)',
            width = 1,
        )
    )
)
trace4 = go.Bar(
    y=['Courier Share'],
    x=[261],
    name='Blue Dart',
    orientation = 'h',
    marker = dict(
        color = 'rgba(45, 153, 51, 0.6)',
        line = dict(
            color = 'rgba(45, 153, 51, 1.0)',
            width = 1,
        )
    )
)
trace5 = go.Bar(
    y=['Courier Share'],
    x=[256],
    name='EE',
    orientation = 'h',
    marker = dict(
        color = 'rgba(15, 53, 151, 0.6)',
        line = dict(
            color = 'rgba(15, 53, 151, 1.0)',
            width = 1,
        )
    )
)
trace6 = go.Bar(
    y=['Courier Share'],
    x=[208],
    name='FD',
    orientation = 'h',
    marker = dict(
        color = 'rgba(145, 33, 51, 0.6)',
        line = dict(
            color = 'rgba(145, 33, 51, 1.0)',
            width = 1,
        )
    )
)
trace7 = go.Bar(
    y=['Courier Share'],
    x=[154],
    name='IP',
    orientation = 'h',
    marker = dict(
        color = 'rgba(34, 143, 116, 0.6)',
        line = dict(
            color = 'rgba(34, 143, 116, 1.0)',
            width = 1,
        )
    )
)
trace8 = go.Bar(
    y=['Courier Share'],
    x=[118],
    name='RE',
    orientation = 'h',
    marker = dict(
        color = 'rgba(121, 40, 51, 0.6)',
        line = dict(
            color = 'rgba(121, 40, 51, 1.0)',
            width = 1,
        )
    )
)
trace9 = go.Bar(
    y=['Courier Share'],
    x=[56],
    name='DTDC',
    orientation = 'h',
    marker = dict(
        color = 'rgba(96, 60, 94, 0.6)',
        line = dict(
            color = 'rgba(96, 60, 94, 1.0)',
            width = 1,
        )
    )
)
trace10 = go.Bar(
    y=['Courier Share'],
    x=[55],
    name='DE',
    orientation = 'h',
    marker = dict(
        color = 'rgba(158, 62, 73, 0.6)',
        line = dict(
            color = 'rgba(158, 62, 73, 1.0)',
            width = 1,
        )
    )
)
trace11 = go.Bar(
    y=['Courier Share'],
    x=[13],
    name='DD',
    orientation = 'h',
    marker = dict(
        color = 'rgba(223, 123, 40, 0.6)',
        line = dict(
            color = 'rgba(223, 123, 40, 1.0)',
            width = 1,
        )
    )
)
trace12 = go.Bar(
    y=['Courier Share'],
    x=[3],
    name='SS',
    orientation = 'h',
    marker = dict(
        color = 'rgba(31, 221, 64, 0.6)',
        line = dict(
            color = 'rgba(31, 221, 64, 1.0)',
            width = 1,
        )
    )
)
data = [trace1, trace2, trace3, trace4, trace5, trace6, trace7, trace8, trace9, trace10, trace11, trace12]
layout = go.Layout(
    barmode='stack'
)
fig = go.Figure(data=data, layout=layout)
plot_url = py.plot(fig, filename='logistics-share')