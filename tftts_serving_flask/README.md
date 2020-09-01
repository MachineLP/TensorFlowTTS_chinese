
```
export PYTHONPATH=${PYTHONPATH}:../tftts_serving_flask
CUDA_VISIBLE_DEVICES=0 nohup python -u tensorflow_tts_run.py > run.log 2>&1 &
```

````
export PYTHONPATH=${PYTHONPATH}:../tftts_serving_flask
python tests/post.py --text "你好"
````


```
export PYTHONPATH=${PYTHONPATH}:../tftts_serving_flask
CUDA_VISIBLE_DEVICES=1 python tests/test_ttsmodel.py
```


```
TensorFlowTTS==0.8
```

模型权重看这里下载，需要翻墙哦
https://colab.research.google.com/drive/1YpSHRBRPBI7cnTkQn1UcVTWEQVbsUm1S?usp=sharing#scrollTo=hKTW94-bWK8O

