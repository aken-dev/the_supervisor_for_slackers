#!/usr/bin/env python3
import datetime

# LINEの日付文字列をDatetime型各種に変換
def get_datetime_from_string(dt_str, type='datetime', format=None):
    if type == 'dt_with_sec':
        return datetime.datetime.strptime(dt_str, '%Y-%m-%dT%H:%M:%S' if format == None else format)
    elif type == 'datetime':
        return datetime.datetime.strptime(dt_str, '%Y-%m-%dT%H:%M' if format == None else format)
    elif type == 'time':
        return datetime.datetime.strptime('20200101T{}'.format(dt_str), '%Y%m%dT%H:%M' if format == None else format).time()
    elif type == 'date':
        return datetime.datetime.strptime(dt_str, '%Y-%m-%d' if format == None else format).date()
    return None

# Datetime型各種をLINEの日付文字列に変換
def get_string_from_datetime(dt_instance=datetime.datetime.now(), type='datetime', format=None):
    if type == 'dt_with_sec':
        return datetime.datetime.strftime(dt_instance, '%Y-%m-%dT%H:%M:%S' if format == None else format)
    elif type == 'datetime':
        return datetime.datetime.strftime(dt_instance, '%Y-%m-%dT%H:%M' if format == None else format)
    elif type == 'time':
        return datetime.datetime.strftime(dt_instance, '%H:%M' if format == None else format)
    elif type == 'date':
        return datetime.datetime.strftime(dt_instance, '%Y-%m-%d' if format == None else format)
    return None
