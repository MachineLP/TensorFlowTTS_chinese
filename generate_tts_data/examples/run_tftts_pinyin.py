# -*- coding:utf-8 -*-

import re
import yaml
import numpy as np
import pandas as pd
from pypinyin import Style
from conf.config import config
from core.parse_text_add_pause import TTSSegPause
from core.tftts_pinyin import TTSModel



if __name__ == "__main__":
    tts_model = TTSModel()
    tts_seg_pause = TTSSegPause()
    data_pd = pd.read_csv(config.MIX_VOICE_TEXT_DATA_PATH, sep=',', encoding='utf-8')
    mix_voice_text_index_list = list( data_pd[config.MIX_VOICE_TEXT_INDEX].values )
    mix_voice_text_list = list( data_pd[config.MIX_VOICE_TEXT].values )

    f2 = "./data/010001-020000.txt"

    f1 = open("./data/000001-010000.txt")
    lines = f1.readlines() 
    with open(f2,"w") as file:
        for idx in range(0, len(lines), 2):
            utt_id, chn_char = lines[idx].strip().split()
            per_text_pinyin = lines[idx + 1].strip().split()
            if "IY1" in per_text_pinyin or "Ｂ" in chn_char:
                print(f"Skip this: {utt_id} {chn_char} {per_text_pinyin}")
                continue
            print ("baker:", per_text_pinyin)
            try:
                per_text_pinyin = tts_model._filter( chn_char, per_text_pinyin )
            except:
                per_text_pinyin = ""
            if per_text_pinyin !="":
                text_str = lines[idx]
                file.write( text_str )
                text_str = lines[idx+1]
                file.write( text_str )

    with open(f2,"a") as file:
        for per_text_index, per_text in zip( mix_voice_text_index_list, mix_voice_text_list ):
            per_text_pinyin = tts_model.get_pyin( per_text )
            if per_text_pinyin !="":
                text_str = str(per_text_index) + '\t' + str(tts_seg_pause.add_pause( per_text )) + '\n'
                file.write( text_str )
                text_str = '\t' + str(per_text_pinyin) + '\n'
                file.write( text_str )
    # write to txt

    



