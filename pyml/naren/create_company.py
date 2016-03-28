import os
import pdb
import utils

import MySQLdb
try:
    conn = utils.persist.connection()
    cur = conn.cursor()
    companysql = 'create table company(id int primary key not null auto_increment, position_id int, unit_id int, \
                position_name varchar(64), new_count int, low_income int, high_income int, \
                bonus varchar(9), pic_id int, last_time varchar(36), trade varchar(9), level varchar(9), \
                strength varchar(5), benefit varchar(255), expdate varchar(36), qualification varchar(36),\
                low_workage varchar(12), high_workage varchar(12), low_age varchar(6), high_age varchar(6), first_language varchar(12), \
                first_language_level int, second_language varchar(6), second_language_level int, sex int, \
                constellation varchar(64), latitude varchar(12), longitude varchar(12), citynum varchar(9), worklocation varchar(26), \
                workingtime varchar(12), publish_time varchar(36), closing_time varchar(36), admin_user_id int, picname varchar(36), \
                state int, autoqa int, bole_user_id int, position_type varchar(12), total_match_count int, school int, education int, \
                position_score int, workproperty varchar(16), description text, position_type1 varchar(36), position_mode int, \
                jiazhiguan varchar(255), zhiyexingge varchar(255), zhiyexingqu varchar(255), basic_score varchar(12), \
                forward_emails varchar(36), applier_trade varchar(64), create_time varchar(36), last_access_time varchar(36), \
                to_handle_count int, edit_time varchar(36), naren_created int, update_flag int, score_setting varchar(36), \
                createtime varchar(36), position_source int, auto_forward_emails varchar(36), dontsendmail int, \
                total_resume_count int)'

    scoretol = cur.execute(companysql)
    conn.commit()
    conn.close()

except Exception as e:

    conn.close()
    print e