# -*- coding: utf8 -*-

import soundfile as sf
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest

# 创建AcsClient实例
client = AcsClient(
   "****",
   "****",
   "cn-shanghai"
);

# 创建request，并设置参数。
request = CommonRequest()
request.set_method('POST')
request.set_domain('nls-meta.cn-shanghai.aliyuncs.com')
request.set_version('2019-02-28')
request.set_action_name('CreateToken')
response = client.do_action_with_exception(request)

print(response)

# b'{"RequestId":"E979F086-13F4-4A6D-9582-74F8D88B2C9B","ErrMsg":"","Token":{"UserId":"1460406656678944","Id":"36258e6956724a2dac3dd59e6cd821fa","ExpireTime":1599188650},"NlsRequestId":"d2dab9c604b349b6936069b07f5f2ab6"}'


# -*- coding: utf-8 -*-
import threading
import ali_speech
from ali_speech.callbacks import SpeechSynthesizerCallback
from ali_speech.constant import TTSFormat
from ali_speech.constant import TTSSampleRate
class MyCallback(SpeechSynthesizerCallback):
    # 参数name用于指定保存音频的文件。
    def __init__(self, name):
        self._name = name
        self._fout = open(name, 'wb')
    def on_binary_data_received(self, raw):
        print('MyCallback.on_binary_data_received: %s' % len(raw))
        self._fout.write(raw)
    def on_completed(self, message):
        print('MyCallback.OnRecognitionCompleted: %s' % message)
        self._fout.close()
    def on_task_failed(self, message):
        print('MyCallback.OnRecognitionTaskFailed-task_id:%s, status_text:%s' % (
            message['header']['task_id'], message['header']['status_text']))
        self._fout.close()
    def on_channel_closed(self):
        print('MyCallback.OnRecognitionChannelClosed')
def process(client, appkey, token, text, audio_name):
    callback = MyCallback(audio_name)
    synthesizer = client.create_synthesizer(callback)
    synthesizer.set_appkey(appkey)
    synthesizer.set_token(token)
    synthesizer.set_voice('aijing')
    # synthesizer.set_voice('aiyu')
    synthesizer.set_text(text)
    synthesizer.set_format(TTSFormat.WAV)
    synthesizer.set_sample_rate(TTSSampleRate.SAMPLE_RATE_24K)
    synthesizer.set_volume(50)
    synthesizer.set_speech_rate(0)
    synthesizer.set_pitch_rate(0)
    try:
        ret = synthesizer.start()
        if ret < 0:
            return ret
        synthesizer.wait_completed()
    except Exception as e:
        print(e)
    finally:
        synthesizer.close()
def process_multithread(client, appkey, token, number):
    thread_list = []
    for i in range(0, number):
        text = "这是线程" + str(i) + "的合成。"
        audio_name = "sy_audio_" + str(i) + ".wav"
        thread = threading.Thread(target=process, args=(client, appkey, token, text, audio_name))
        thread_list.append(thread)
        thread.start()
    for thread in thread_list:
        thread.join()

if __name__ == "__main__":
    import time
    start_time = time.time()
    client = ali_speech.NlsClient()
    # 设置输出日志信息的级别：DEBUG、INFO、WARNING、ERROR。
    client.set_log_level('INFO')
    appkey = ''
    token = ''

    '''

    text = "对于#1反对派，我一直觉得他们很肮脏"
    audio_name = './BZNSYP/Wave/009560.wav'
    process(client, appkey, token, text, audio_name)
    # 多线程示例
    # process_multithread(client, appkey, token, 2) 
    print ( "time>>>>>>", time.time()-start_time )

    '''
    f1 = open("./data/000001-010000.txt")
    lines = f1.readlines() 
    for idx in range(0, len(lines), 2):
        utt_id, chn_char = lines[idx].strip().split()
        audio_name = './BZNSYP/Wave/' + str(utt_id) + '.wav' 
        try:
            audio, rate = sf.read(audio_name)
        except:
            print ("utt_id>>>>>", utt_id)
            for per_r in ["#", "1", "2","3","4","5","6","7","8","9","10"]:
                chn_char = chn_char.replace(per_r, "")
            text = chn_char
            #if idx >5:
            #    break
            start_time = time.time()
            process(client, appkey, token, text, audio_name)
            print ( "time>>>>>>", time.time()-start_time )
    


