# -*- coding:utf-8 -*-
'''
-------------------------------------------------
   Description :  models
   Author :       machinelp
   Date :         2020-08-27
-------------------------------------------------

'''

import yaml
import numpy as np
import tensorflow as tf
from conf.config import config
# import IPython.display as ipd
from utils.logging import logging
from tensorflow_tts.inference import AutoConfig
from tensorflow_tts.inference import TFAutoModel
from tensorflow_tts.inference import AutoProcessor
from core.parse_text_add_pause import TTSSegPause
from core.parse_text_to_pyin import TTSPinYin

from tensorflow_tts.configs import Tacotron2Config
from tensorflow_tts.models import TFTacotron2

class TTSModel():

    def __init__(self):
        gpus = tf.config.experimental.list_physical_devices(device_type='GPU')
        tf.config.experimental.set_visible_devices(devices=gpus[0:2], device_type='GPU')
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
        self._converter_model()

    def _converter_model(self):
        with open( config.tacotron2_baker ) as f:
            conf = yaml.load(f, Loader=yaml.Loader)
        conf = Tacotron2Config(**conf["tacotron2_params"])
        self.tacotron2 = TFTacotron2(config=conf, training=False, name="tacotron2", enable_tflite_convertible=True)
        self.tacotron2.setup_window(win_front=5, win_back=5)
        # self.tacotron2.setup_maximum_iterations(1000) # be careful
        self.tacotron2._build()
        self.tacotron2.load_weights(config.tacotron2_pretrained_path)

        self.tacotron2.save('./', save_format='tf')


