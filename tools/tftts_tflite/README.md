
```
export PYTHONPATH=${PYTHONPATH}:../server
CUDA_VISIBLE_DEVICES=0 nohup python -u tensorflow_tts_run.py > run.log 2>&1 &
```

````
export PYTHONPATH=${PYTHONPATH}:../server
python tests/post.py --text "你好"
````


```
export PYTHONPATH=${PYTHONPATH}:../server
CUDA_VISIBLE_DEVICES=1 python tests/test_ttsmodel.py
```


```
TensorFlowTTS==0.8
```
