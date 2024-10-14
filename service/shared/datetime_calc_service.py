#!/usr/bin/env python3
import datetime
import math

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

# 引数で受け取ったdatetimeの値の日時が含まれる、ユーザーの1日のスタート日時とエンド日時を返却
def get_users_time_range_of_the_day(
        registered_users_time_a_day_starts=0, 
        sample_datetime=datetime.datetime.now()
    ):
    return_datetime_start_of_the_day: datetime
    return_datetime_end_of_the_day: datetime
    #ユーザー指定の時刻に達しているのなら
    if sample_datetime.hour >= registered_users_time_a_day_starts:
        return_datetime_start_of_the_day = sample_datetime.replace(hour=registered_users_time_a_day_starts, minute=0, second=0, microsecond=0)
        return_datetime_end_of_the_day = return_datetime_start_of_the_day + datetime.timedelta(days=1) + datetime.timedelta(microseconds=-1)
    #ユーザー指定の時刻に達していないなら
    else:
        return_datetime_start_of_the_day = sample_datetime.replace(hour=registered_users_time_a_day_starts, minute=0, second=0, microsecond=0) \
                     + datetime.timedelta(days=-1) 
        return_datetime_end_of_the_day = sample_datetime.replace(hour=registered_users_time_a_day_starts - 1, minute=59, second=59, microsecond=999999)
    return return_datetime_start_of_the_day, return_datetime_end_of_the_day
