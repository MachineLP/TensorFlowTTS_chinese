
###  该项目是fork：https://github.com/TensorSpeech/TensorFlowTTS ；



中文TTS构建流程：
>（1）文本正则化/Text Normalization(TN) 
>（2）分词/Word Segmentation 
>（3）词性预测/Part-of-speech 
>（4）韵律预测/Prosody 
>（5）注音(多音字)/Polyphone 
>（6）语言学特征生成/Linguistic feature 


正则化方法：
>（1）https://github.com/google/re2 
>（2）https://github.com/speechio/chinese_text_normalization 

注音方法：
> （1）https://github.com/kakaobrain/g2pM
> （2）https://github.com/MachineLP/TensorFlowTTS_chinese/blob/master/generate_tts_data/core/tftts_pinyin.py
