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
        self.tts_pause = TTSSegPause()
        self.tts_py = TTSPinYin()

    def _converter_model(self):
        with open( config.tacotron2_baker ) as f:
            conf = yaml.load(f, Loader=yaml.Loader)
        conf = Tacotron2Config(**conf["tacotron2_params"])
        self.tacotron2 = TFTacotron2(config=conf, training=False, name="tacotron2", enable_tflite_convertible=True)
        self.tacotron2.setup_window(win_front=5, win_back=5)
        self.tacotron2.setup_maximum_iterations(1000) # be careful
        self.tacotron2._build()
        self.tacotron2.load_weights(config.tacotron2_pretrained_path)
        tacotron2_concrete_function = self.tacotron2.inference_tflite.get_concrete_function()
        converter = tf.lite.TFLiteConverter.from_concrete_functions( [tacotron2_concrete_function] )
        converter.optimizations = [tf.lite.Optimize.DEFAULT]
        converter.target_spec.supported_ops = [ tf.lite.OpsSet.TFLITE_BUILTINS, tf.lite.OpsSet.SELECT_TF_OPS ]
        tflite_model = converter.convert()
        with open('tacotron2.tflite', 'wb') as f:
            f.write(tflite_model)
        
        print('Model size is %f MBs.' % (len(tflite_model) / 1024 / 1024.0) )

        #tacotron2_config = AutoConfig.from_pretrained( config.tacotron2_baker )
        #self.tacotron2 = TFAutoModel.from_pretrained( config=tacotron2_config, pretrained_path='tacotron2.tflite', training=False,  name="tacotron2" )
        #self.tacotron2.setup_window(win_front=5, win_back=5)
        self.interpreter = tf.lite.Interpreter(model_path='tacotron2.tflite')
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()

        mb_melgan_config = AutoConfig.from_pretrained( config.multiband_melgan_baker )
        self.mb_melgan = TFAutoModel.from_pretrained( config=mb_melgan_config, pretrained_path=config.multiband_melgan_pretrained_path, name="mb_melgan" )

        self.processor = AutoProcessor.from_pretrained(pretrained_path=config.baker_mapper_pretrained_path)

    def prepare_input(self, input_ids):
        return (tf.expand_dims(tf.convert_to_tensor(input_ids, dtype=tf.int32), 0), tf.convert_to_tensor([len(input_ids)], tf.int32), tf.convert_to_tensor([0], dtype=tf.int32))


    def do_synthesis(self, input_text):
        input_text = self.tts_pause.add_pause(input_text)
        print ("input_text>>>>", input_text)
        logging.info( "[TTSModel] [do_synthesis] input_text:{}".format( input_text ) )
        input_ids = self.processor.text_to_sequence(input_text, inference=True) 
        # nput_ids = np.concatenate([input_ids, [219 - 1]], -1)
        self.interpreter.resize_tensor_input( self.input_details[0]['index'], [1, len(input_ids)] )

        self.interpreter.allocate_tensors()
        input_data = self.prepare_input(input_ids)
        for i, detail in enumerate(self.input_details):
            input_shape = detail['shape']
            self.interpreter.set_tensor(detail['index'], input_data[i])
        # self.interpreter.invoke()
        decoder_output_tflite, mel_outputs = self.interpreter.get_tensor(self.output_details[0]['index']), interpreter.get_tensor(self.output_details[1]['index'])

        remove_end = 1024
        audio = self.mb_melgan.inference(mel_outputs)[0, :-remove_end, 0]
    
        return mel_outputs.numpy(), decoder_output_tflite.numpy(), audio.numpy() 



    '''
    input_text = "如果现在还不了，您可以想办法处理啊，您家人知道您的逾期情况吗？他们能不能帮您周转处理逾期账单？"
    mels, alignment_history, audios = do_synthesis(input_text)
    ipd.Audio(audios, rate=24000)
    '''

