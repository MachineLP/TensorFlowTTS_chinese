# -*- coding: utf-8 -*-

from seg_pause.parse_text_add_pause import TTSSegPause


if __name__ == '__main__':
    tts_pause = TTSSegPause()
    text = '如果打穿地球，那么从一头到另一头会发生什么？'
    content = tts_pause.add_pause(text)
    print(content)


    text = '你好啊'
    content = tts_pause.add_pause(text)
    print(content)


    text = '你好'
    content = tts_pause.add_pause(text)
    print(content)

    text = 'app'
    content = tts_pause.add_pause(text)
    print(content)

    text = '来分期APP'
    content = tts_pause.add_pause(text)
    print(content)

    text = '你的金额是1234.34'
    content = tts_pause.add_pause(text)
    print(content)

    text = '如果今天还不了，那么再见'
    content = tts_pause.add_pause(text)
    print(content)



'''
如果#2打#1穿#1地球#3，那么#2从#1一头#2到#1另一头#2会#1发生#2什么？
你好#2啊
你好
艾普
来分期#2艾普
你#1的#1金额#2是#1一千二百#2三十四点#2三四
'''
