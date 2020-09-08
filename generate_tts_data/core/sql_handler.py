# -*- coding:utf-8 -*-
'''
-------------------------------------------------
   Description :  SQLHandler
   Author :       machinelp
   Date :         2020-08-10
-------------------------------------------------

'''

import os
import sys
import json
import time 
import argparse
import datetime
import pandas as pd
from config import config
from pandas.core.frame import DataFrame
from utils.quality_check_dao import QualityCheckDao

class SQLHandler(object):
    def __init__(self):
        self.mm_online = QualityCheckDao(config.ONLINE_MYSQL_URL_ONLINE)
    
    def _get_mix_voice_text_data(self):
        dump_sql =  config.GET_VOICE_TEXT_SQL
        data_pd = self.mm_online.query_all(dump_sql)
        return data_pd
   
    def _get_data(self):
        mix_voice_text_data = self._get_mix_voice_text_data() 
        text_list = []
        for per_text_list in list(mix_voice_text_data["mix_voice_text"].values):
            if per_text_list == "" or per_text_list == "null":
                continue
            try :
                per_text_list = eval( per_text_list )
                for per_text in per_text_list:
                    text = per_text["nodeText"]
                    if text != "" or text != "null":
                        print ("text>>>>>", text)
                        for per_r in ["@", "$", "1","2","3","4","5","6","7","8","9","10"]:
                            text = text.replace(per_r, "")
                        
                        text_list.append( text )
            except:
                continue 
        mix_voice_text_list = list( set(text_list) )
        mix_voice_text_index_list = []
        for i in range (len( mix_voice_text_list ) ):
            mix_voice_text_index_list.append( '0' + str(10001+i) )

        res = DataFrame()
        res[config.MIX_VOICE_TEXT_INDEX] = mix_voice_text_index_list
        res[config.MIX_VOICE_TEXT] = mix_voice_text_list
        res[ [config.MIX_VOICE_TEXT_INDEX, config.MIX_VOICE_TEXT] ].to_csv( config.MIX_VOICE_TEXT_DATA_PATH, index=False) 

    def get_all_data(self):
        self._get_data()      # 全量更新

if __name__ == "__main__":
    sql_handler = SQLHandler()
    sql_handler.get_all_data()
