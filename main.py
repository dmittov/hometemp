# -*- coding: utf-8 -*-
from flask import Flask, request, render_template
from flask import Response, Request
import json
import meteo
import graph

__author__ = 'Dmitry Mittov <mittov@gmail.com>'

app = Flask(__name__)

HTTP_201_CREATED = 201

app.jinja_env.globals.update(format_temp=meteo.format_temp)
app.jinja_env.globals.update(format_humid=meteo.format_humid)

@app.route('/')
def hello_world():
    svg_image = graph.plot_data()
    return render_template('graph.html',
                           current_readings=\
                               meteo.MeteoState.current_readings('home_DHT22'),
                           svg_image=svg_image)


@app.route('/sensor/<name>', methods=['POST'])
def add_sensor_data(name):
    meteo.process_state(name, request.get_json())
    return "{'msg': 'ok'}", HTTP_201_CREATED


@app.route('/day/<sensor>')
def get_last_day_data(sensor):
    meteo_list = meteo.MeteoState.day_data(sensor)
    json_data = json.dumps(map(
        lambda state: {'dttm': state.dttm.isoformat(),
                       'temp': '{0:.1f}'.format(state.temp),
                       'humidity': '{0:.1f}'.format(state.humidity)},
        meteo_list))
    response = Response(response=json_data,
                        status=200,
                        mimetype="application/json")
    return response


if __name__ == '__main__':
    app.run(debug=True)
