from flask import Flask
from flask import request
from flask_cors import CORS
import pandas as pd
import numpy as np

from .data import analysis

app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})

dataframes, datasets = analysis.get_datasets()
slugs = [{'slug': str(key), 'title': datasets[key]['title']} for key in datasets.keys()]

colours = []
for _ in range(1000):
    colour = str(list(np.random.choice(range(256), size=3))).replace("[", "rgb(").replace("]", ")")
    colours.append(colour)


@app.route('/')
def get_available_dataset():
    return {'slugs': slugs}, 200


@app.route('/dataset/<slug>')
def get_dataset(slug):
    return datasets[str(slug)], 200


@app.route('/scatterChartData/<slug>', methods=['PUT'])
def get_scatter_chart(slug):
    for s in slugs:
        if 'year master' in s['title']:
            slug = s['slug']
            break

    df = dataframes[str(slug)]
    df = df.set_index(['year'], append=True)
    df = df.iloc[:, 1:]

    df = df.fillna(0)
    print(df)

    return 'ok'
    # return data_dict


@app.route('/barChartData/<slug>', methods=['PUT'])
def get_bar_chart(slug):
    cols = request.json['cols']
    countries = request.json['countries']
    transpose = request.json['transpose']


    # TODO remove
    for s in slugs:
        if 'Med devices labs' in s['title']:
            slug = s['slug']
            break

    df = dataframes[str(slug)].loc[:, cols]
    df = df.loc[countries]
    df = df.fillna(0)

    if transpose:
        df = df.transpose()

    data_dict = df.to_dict(orient='list')
    datasets = []
    for label, values in data_dict.items():
        datasets.append({
                'label': label,
                'data': values,
            })

    chart_data = {
        'labels': list(df.index),
        'datasets': datasets
    }

    return chart_data, 200

