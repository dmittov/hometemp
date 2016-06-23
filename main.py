# -*- coding: utf-8 -*-
from flask import Flask, request, render_template
from flask import Response, Request
import json
import logging
import appcfg
import meteo

__author__ = 'Dmitry Mittov <mittov@gmail.com>'

app = Flask(__name__)

HTTP_201_CREATED = 201

app.jinja_env.globals.update(format_temp=meteo.format_temp)
app.jinja_env.globals.update(format_humid=meteo.format_humid)

@app.route('/')
def main_page():
    current_readings = appcfg.MeteoState.current_readings(appcfg.SENSOR_ID)
    return render_template('graph.html',
                           current_readings=current_readings)


@app.route('/sensor/<name>', methods=['POST'])
def add_sensor_data(name):
    meteo.process_state(name, request.get_json())
    return "{'msg': 'ok'}", HTTP_201_CREATED


def transform_c3(meteo_states):
    temp = ['temp']
    temp += [float(state['temp']) for state in meteo_states]
    humidity = ['humidity']
    humidity += [float(state['humidity']) for state in meteo_states]
    return [temp, humidity]


@app.route('/day/<sensor>')
def get_last_day_data(sensor):
    meteo_states = appcfg.MeteoState.day_data(sensor)
    data = transform_c3(meteo_states)
    response = Response(response=json.dumps(data),
                        status=200,
                        mimetype="application/json")
    return response


if __name__ == '__main__':
    app.run(debug=True)
