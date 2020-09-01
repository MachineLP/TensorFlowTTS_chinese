# -*- coding:utf-8 -*-
'''
-------------------------------------------------
   Description :  models
   Author :       machinelp
   Date :         2020-08-27
-------------------------------------------------

'''
import yaml
import numpy as np
from pypinyin import Style
from conf.config import config
from tensorflow_tts.inference import AutoProcessor

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
        return " ".join( new_pinyin )
