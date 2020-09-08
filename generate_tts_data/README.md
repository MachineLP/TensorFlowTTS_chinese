
## 拉取samrt call 文本数据
./bin/get_samrt_call_data.sh


## 将文本专为拼音
./bin/gen_tts_pinyin.sh


## 基于阿里云TTS生成TensorflowTTS训练音频
./bin/gen_tts_audio.sh


## 训练前的preprocess
./bin/gen_tts_train_data_preprocess.sh


## 训练前的normalize
./bin/gen_tts_train_data_normalize.sh


/home/suser/machinelp/TensorflowTTS/examples/tacotron2/exp/train.tacotron2.baker.v1/checkpoints/model-25000.h5