# -*- coding: utf-8 -*-
from matplotlib import pyplot as plt
from matplotlib import dates
import StringIO
import meteo
from datetime import timedelta, datetime
import numpy as np

__author__ = 'Dmitry Mittov <mittov@gmail.com>'


def parse_data(data):
    dttm_data = map(lambda state: state.dttm, data)
    temp_data = map(lambda state: state.temp, data)
    humidity_data = map(lambda state: state.humidity, data)
    return dttm_data, temp_data, humidity_data


def day_limits(dttm):
    max_dttm, min_dttm = max(dttm), min(dttm)
    left_bound = datetime.combine(min_dttm.date(), datetime.min.time())
    right_bound = datetime.combine(max_dttm.date(), datetime.min.time()) + \
        timedelta(days=1)
    return {'left': left_bound, 'right': right_bound}


def plot_data():
    (left_bound, right_bound), day_data = \
        meteo.MeteoState.last_day('home_DHT22')
    dttm, temp, humidity = parse_data(day_data)
    rv = StringIO.StringIO()

    try:
        fig, ax1 = plt.subplots()
        fig.suptitle('SVG')

        graph1 = ax1.plot(dttm, temp, 'orange')
        ax1.set_ylabel('Temperature, C')
        ax1.set_ylim([15, 40])

        ax2 = ax1.twinx()
        graph2 = ax2.plot(dttm, humidity, 'blue')
        ax2.set_ylabel('Humidity, %')
        ax2.set_ylim([0, 100])

        ax1.set_xlabel('Time')
        ax1.set_xlim(left_bound, right_bound)
        ax1.xaxis.set_ticklabels([])

        fig.savefig(rv, format="svg")
    finally:
        plt.clf()

    return rv.getvalue()
