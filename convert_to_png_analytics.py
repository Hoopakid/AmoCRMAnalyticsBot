import plotly.graph_objects as go


def create_chart(data, filename='chart.png'):
    successful_calls = [i['success'] for i in data]
    unsuccessful_calls = [i['no_success'] for i in data]
    fig = go.Figure(data=[
        go.Bar(name="Ko'tarilgan qo'ng'iroqlar", x=[i['name'] for i in data], y=successful_calls),
        go.Bar(name="Ko'tarilmagan qo'ng'iroqlar", x=[i['name'] for i in data], y=unsuccessful_calls),
    ])

    fig.update_layout(barmode='group', title="Qo'ng'iroqlar analizi", xaxis_title='Xodim',
                      yaxis_title="Qo'ng'iroqlar Soni")

    fig.write_image(filename)
