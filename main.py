from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import os

from PIL import Image
import numpy as np
import plotly.express as px



def test():
    # Change working dir to current running script dir:
    print('[change directory]')
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # load the image
    img = np.array(Image.open('photo.jpg'))

    fig = px.imshow(img, color_continuous_scale='gray')
    fig.update_layout(coloraxis_showscale=False)
    fig.update_xaxes(showticklabels=False)
    fig.update_yaxes(showticklabels=False)
    fig.show()


app = Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for your data.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )

    html.Img(src='/photo.jpg')
])

if __name__ == '__main__':
    app.run_server(debug=True)