import requests
import pandas as pd
import json
import time
import numpy as np
import librosa
import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--text', help="update mode", type=str, default="你好")
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = parse_args()
    # text = "我们本次谈话内容录音备案记录，如果您可以在规定时间内下载来分期 艾普 处理逾期账单，我会帮您申请恢复额度，额度恢复以后如果您还有资金需求可以在来分期 艾普 上申请下单，系统审核通过以后，可以再把额度周转出来使用，但若与您协商却无法按时处理，造成的负面影响需自行承担，请提前告知他们有关去电事宜，再见"
    url = "http://127.0.0.1:9959/infer"
    print ( ">>>>>", args.text )
    json_data = json.dumps( {"content": args.text} )
    headers = {'content-type': 'application/json'}
    start_time = time.time()
    respond = requests.request("POST", url, data=json_data, headers=headers)
    print ("time>>>>>>>", time.time() - start_time)
    audios = np.array( respond.json()["data"] )
    librosa.output.write_wav("output_seq.wav", audios, 24000)


# python tests/post.py --text "你好"

