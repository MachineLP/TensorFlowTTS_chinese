# -*- coding:utf-8 -*-
'''
-------------------------------------------------
   Description :  TTSModel
   Author :       machinelp
   Date :         2020-08-27
-------------------------------------------------

'''
import re
import yaml
import numpy as np
import pandas as pd
from pypinyin import Style
from conf.config import config
from tensorflow_tts.inference import AutoProcessor
from core.parse_text_add_pause import TTSSegPause

zh_pattern = re.compile("[\u4e00-\u9fa5]")


def is_zh(word):
    global zh_pattern
    match = zh_pattern.search(word)
    return match is not None



class TTSModel():

    def __init__(self):
        self.__init_model()

    def __init_model(self):
        self.processor = AutoProcessor.from_pretrained(pretrained_path=config.baker_mapper_pretrained_path)

    def get_pyin(self, text):
        pinyin = self.processor.pinyin_parser(text, style=Style.TONE3, errors="ignore")
        new_pinyin = []
        for x in pinyin:
            x = "".join(x)
            if "#" not in x:
                new_pinyin.append(x)
        flag = True
        try:
            flag = self._filter( text, new_pinyin )
        except:
            flag = False
        if flag:
            return " ".join( new_pinyin )
        else:
            return ""
    
    def _filter(self, chn_char, pinyin):
        # we do not need #4, use sil to replace it
        chn_char = chn_char.replace("#4", "")
        char_len = len(chn_char)
        i, j = 0, 0
        result = ["sil"]
        while i < char_len:
            cur_char = chn_char[i]
            if is_zh(cur_char):
                if pinyin[j][:-1] not in self.processor.pinyin_dict:
                    if chn_char[i + 1] != "儿":
                        return False
                    if pinyin[j][-2] == "r":
                        return False
                    tone = pinyin[j][-1]
                    a = pinyin[j][:-2]
                    a1, a2 = self.processor.pinyin_dict[a]
                    result += [a1, a2 + tone, "er5"]
                    if i + 2 < char_len and chn_char[i + 2] != "#":
                        result.append("#0")

                    i += 2
                    j += 1
                else:
                    tone = pinyin[j][-1]
                    a = pinyin[j][:-1]
                    a1, a2 = self.processor.pinyin_dict[a]
                    result += [a1, a2 + tone]

                    if i + 1 < char_len and chn_char[i + 1] != "#":
                        result.append("#0")

                    i += 1
                    j += 1
            elif cur_char == "#":
                result.append(chn_char[i : i + 2])
                i += 2
            else:
                # ignore the unknown char and punctuation
                # result.append(chn_char[i])
                i += 1
        if result[-1] == "#0":
            result = result[:-1]
        result.append("sil")
        if j == len(pinyin):
            return False
        return True
        # return result


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

    



