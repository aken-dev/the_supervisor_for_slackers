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
def get_string_from_datetime(dt_instance=None, type='datetime', format=None):
    if dt_instance == None: dt_instance = datetime.datetime.now()
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
def get_users_time_range_of_the_day(registered_users_time_a_day_starts, sample_datetime=None):
    if sample_datetime == None: 
        sample_datetime = datetime.datetime.now()
    start_of_the_day: datetime
    end_of_the_day: datetime
    #ユーザー指定の時刻に達しているのなら
    if sample_datetime.hour >= registered_users_time_a_day_starts:
        start_of_the_day = sample_datetime.replace(hour=registered_users_time_a_day_starts, minute=0, second=0, microsecond=0)
        end_of_the_day = start_of_the_day + datetime.timedelta(days=1) + datetime.timedelta(microseconds=-1)
    #ユーザー指定の時刻に達していないなら
    else:
        start_of_the_day = sample_datetime.replace(
            hour=registered_users_time_a_day_starts, minute=0, second=0, microsecond=0) \
            + datetime.timedelta(days=-1) 
        end_of_the_day = sample_datetime.replace(
            hour=registered_users_time_a_day_starts - 1, minute=59, second=59, microsecond=999999)
    return {
        "start_of_the_day": start_of_the_day,
        "end_of_the_day": end_of_the_day
    }
