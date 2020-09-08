
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
CUDA_VISIBLE_DEVICES=3 python tests/test_ttsmodel.py
```


```
TensorFlowTTS==0.8
```

/home/suser/machinelp/TensorflowTTS/examples/multiband_melgan/exp/train.multiband_melgan.baker.v1/checkpoints/generator-200000.h5
