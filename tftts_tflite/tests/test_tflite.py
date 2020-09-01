import numpy as np
import soundfile as sf
import yaml
import tensorflow as tf

import librosa
from conf.config import config as config_lp

from tensorflow_tts.processor import LJSpeechProcessor

from tensorflow_tts.configs import Tacotron2Config
from tensorflow_tts.configs import MelGANGeneratorConfig

from tensorflow_tts.models import TFTacotron2
from tensorflow_tts.models import TFMelGANGenerator
from tensorflow_tts.inference import AutoProcessor
from core.parse_text_add_pause import TTSSegPause

from IPython.display import Audio
print(tf.__version__)


# initialize melgan model
with open( config_lp.multiband_melgan_baker ) as f:
    melgan_config = yaml.load(f, Loader=yaml.Loader)
melgan_config = MelGANGeneratorConfig(**melgan_config["multiband_melgan_generator_params"])
melgan = TFMelGANGenerator(config=melgan_config, name='mb_melgan')
melgan._build()
melgan.load_weights( config_lp.multiband_melgan_pretrained_path )



# initialize Tacotron2 model.
with open( config_lp.tacotron2_baker ) as f:
    config = yaml.load(f, Loader=yaml.Loader)
config = Tacotron2Config(**config["tacotron2_params"])
tacotron2 = TFTacotron2(config=config, training=False, name="tacotron2v2",
                        enable_tflite_convertible=True)

# Newly added :
tacotron2.setup_window(win_front=6, win_back=6)
tacotron2.setup_maximum_iterations(3000)

tacotron2._build()
tacotron2.load_weights( config_lp.tacotron2_pretrained_path )
tacotron2.summary()



# Concrete Function
tacotron2_concrete_function = tacotron2.inference_tflite.get_concrete_function()



converter = tf.lite.TFLiteConverter.from_concrete_functions(
    [tacotron2_concrete_function]
)
converter.optimizations = [tf.lite.Optimize.DEFAULT]
converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS,
                                       tf.lite.OpsSet.SELECT_TF_OPS]
tflite_model = converter.convert()




# Save the TF Lite model.
with open('tacotron2.tflite', 'wb') as f:
  f.write(tflite_model)

print('Model size is %f MBs.' % (len(tflite_model) / 1024 / 1024.0) )



import numpy as np
import tensorflow as tf

# Load the TFLite model and allocate tensors.
interpreter = tf.lite.Interpreter(model_path='tacotron2.tflite')
interpreter.allocate_tensors()

# Get input and output tensors.
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Prepare input data.
def prepare_input(input_ids):
  return (tf.expand_dims(tf.convert_to_tensor(input_ids, dtype=tf.int32), 0),
          tf.convert_to_tensor([len(input_ids)], tf.int32),
          tf.convert_to_tensor([0], dtype=tf.int32))
  
tts_pause = TTSSegPause()
# Test the model on random input data.
def infer(input_text):
  processor = AutoProcessor.from_pretrained(pretrained_path=config_lp.baker_mapper_pretrained_path)
  input_text = tts_pause.add_pause(input_text)
  # logging.info( "[TTSModel] [do_synthesis] input_text:{}".format( input_text ) )
  input_ids = processor.text_to_sequence(input_text, inference=True) 
        
  # input_ids = np.concatenate([input_ids, [len(symbols) - 1]], -1)  # eos.
  interpreter.resize_tensor_input(input_details[0]['index'],  [1, len(input_ids)])

  interpreter.allocate_tensors()
  input_data = prepare_input(input_ids)
  for i, detail in enumerate(input_details):
    print(detail)
    input_shape = detail['shape']
    interpreter.set_tensor(detail['index'], input_data[i])

  interpreter.invoke()

  # The function `get_tensor()` returns a copy of the tensor data.
  # Use `tensor()` in order to get a pointer to the tensor.
  return (interpreter.get_tensor(output_details[0]['index']),
          interpreter.get_tensor(output_details[1]['index']))


input_text = " 你好呀 "

decoder_output_tflite, mel_output_tflite = infer(input_text)
audio_before_tflite = melgan(decoder_output_tflite)[0, :, 0]
audio_after_tflite = melgan(mel_output_tflite)[0, :, 0]

librosa.output.write_wav("output_seq.wav", audio_after_tflite.numpy(), 24000)


