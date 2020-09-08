# -*- coding: utf8 -*-

import time
import soundfile as sf
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
from core.tts_audio import process
import ali_speech

# 创建AcsClient实例
client = AcsClient(
   "LTAI4GHMr3H57pxJ4CScsv5G",
   "PkRPqTCFVVliD99z3EfOACF4lH7tQY",
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



if __name__ == "__main__":
    import time
    start_time = time.time()
    client = ali_speech.NlsClient()
    # 设置输出日志信息的级别：DEBUG、INFO、WARNING、ERROR。
    client.set_log_level('INFO')
    appkey = 'uYzyInI9xS3foVHU'
    token = '1fd291b7716c48fd9f4adc2915f7d549'

    

    text = "账单逾期请在今天内下载来分期诶皮皮查看并进行还款，关于您逾期的后果我已经跟您阐述清楚了，另外后续可能会到您当地法院控诉维权，到时给如果您个人生活以及如果您家人或同事查询到，对您声誉产生的所有后果影响由您个人承担，再见。"
    audio_name = './aliyun.wav'
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
    '''

