# -*- coding: utf-8 -*-

from pinyin.parse_text_to_pyin import TTSPinYin
from seg_pause.parse_text_add_pause import TTSSegPause


if __name__ == '__main__':
    ttspy = TTSPinYin()
    tts_pause = TTSSegPause()
    text = '如果打穿地球#3，那么从一头到另一头会发生什么？'
    cotextntent = tts_pause.preprocess(text)
    pyin, txt = ttspy.get_pyin(text)
    print(pyin)


    text = '还不了'
    pyin, txt = ttspy.get_pyin(text)
    print(pyin) 



'''
如果打穿地球，那么从一头到另一头会发生什么？
ru2 guo3 da3 chuan1 di4 qiu2 #3 ， na4 me cong2 yi1 tou2 dao4 ling4 yi1 tou2 kuai4 fa1 sheng1 shen2 me ？
还不了
huan2 bu4 liao3
'''