# -*- coding: utf-8 -*-
from google.appengine.ext import ndb
import json
from datetime import date, timedelta, datetime
from collections import namedtuple

__author__ = 'Dmitry Mittov <mittov@gmail.com>'


def format_temp(temp):
    return u'{0:.1f}{1}'.format(temp, u'°C')


def format_humid(humidity):
    return u'{0:.1f}{1}'.format(humidity, u'%')


class MeteoState(ndb.Model):
    sensor = ndb.StringProperty(required=True)
    dttm = ndb.DateTimeProperty(auto_now=True, required=True)
    temp = ndb.FloatProperty()
    humidity = ndb.FloatProperty()

    @classmethod
    def current_readings(cls, sensor):
        query = cls.query(cls.sensor == sensor).order(-cls.dttm)
        return query.fetch(1)[0]

    @classmethod
    def day_data(cls, sensor):
        (_, _), data = cls.last_day(sensor)
        return data[::60]

    @classmethod
    def last_day(cls, sensor):
        right_bound = datetime.now()
        left_bound = right_bound - timedelta(days=1)
        query = cls.query(ndb.AND(cls.dttm <= right_bound,
                          cls.dttm > left_bound,
                          cls.sensor == sensor)).order(cls.dttm)
        return (left_bound, right_bound), query.fetch()

    @classmethod
    def today(cls, sensor):
        today = datetime.combine(date.today(), datetime.min.time())
        query = cls.query(ndb.AND(cls.dttm >= today,
                                  cls.dttm < today + timedelta(days=1),
                                  cls.sensor == sensor))
        return query.fetch()


class MeteoStateStub(MeteoState):

    from collections import namedtuple

    @classmethod
    def day_data(cls, sensor):
        with open('stubs/day_data.json') as fh:
            raw_content = fh.read()
        content = json.loads(raw_content)
        return [namedtuple('GenericDict', item.keys())(**item)
                for item in content]

    @classmethod
    def current_readings(cls, sensor):
        state = MeteoStateStub()
        state.temp = 25.0
        state.humidity = 50.0
        return state


def process_state(sensor, state):
    meteo_state = MeteoState()
    meteo_state.sensor = sensor
    meteo_state.temp = state['temp']
    meteo_state.humidity = state['humidity']
    meteo_state.put()
