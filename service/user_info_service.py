#!/usr/bin/env python3
import datetime
import sys
import traceback
import re
import common.constant as co
import repository.user_info_repository as ui_rp
from entity.user_info_entity import UserInfo

# UserInfo
def get_user_info(line_user_id, line_name):
    result_count, result = ui_rp.user_info_select(line_user_id)
    if result_count == 0:
        userInfo = add_new_user(line_user_id, line_name)
        if userInfo == None:
            print('新規ユーザレコード追加失敗 : {} : {}'.format(line_user_id, line_name))
            return None
        else:
            return userInfo
    else:
        userInfo = UserInfo()
        userInfo.setEntityFromRecord(result)
        return userInfo

def add_new_user(line_user_id, line_name):
    userInfo = UserInfo(
        line_user_id = line_user_id,
        line_name = line_name,
        allowed = co.USER_UNREGISTERED,
        registered_datetime = datetime.datetime.now(),
        registered_by = sys._getframe().f_code.co_name,
        updated_datetime = datetime.datetime.now(),
        updated_by = sys._getframe().f_code.co_name
    )
    result_count = ui_rp.userinfo_new_user_insert(userInfo)
    if result_count == 0:
        return None
    else:
        return userInfo

def change_user_allowed(userInfo, new_allowed):
    userInfo.allowed = new_allowed
    userInfo.updated_datetime = datetime.datetime.now(),
    userInfo.updated_by = sys._getframe().f_code.co_name
    result_count = ui_rp.userinfo_update(userInfo, 'allowed')
    if result_count == 0:
        return None
    else:
        return userInfo

def update_user_info(userInfo, target_column, new_value):
    eval('userInfo.{} = {}'.format(target_column, new_value))
    userInfo.updated_datetime = datetime.datetime.now(),
    userInfo.updated_by = sys._getframe().f_code.co_name
    result_count = ui_rp.userinfo_update(userInfo, target_column)
    if result_count == 0:
        return None
    else:
        return userInfo

def display_user_info(userInfo, new_user_flag=False):
    a = 0