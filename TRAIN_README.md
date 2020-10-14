
# train tacotron2
CUDA_VISIBLE_DEVICES=0 nohup python -u  examples/tacotron2/train_tacotron2.py \
  --train-dir ./dump_ali/train/ \
  --dev-dir ./dump_ali/valid/ \
  --outdir ./examples/tacotron2/exp/train.tacotron2.baker.v1/ \
  --config ./examples/tacotron2/conf/tacotron2.baker.v1.yaml \
  --use-norm 1 \
  --mixed_precision 0 \
  --resume "./examples/tacotron2/exp/train.tacotron2.baker.v1/checkpoints/ckpt-50000" > train_tacotron2.log 2>&1 &
#   --pretrained "./tftts_serving_flask/data/model/tacotron2-100k.h5" > train_tacotron2.log 2>&1 &



# train multiband_melgan
## training generator with only stft loss
CUDA_VISIBLE_DEVICES=3 nohup python -u examples/multiband_melgan/train_multiband_melgan.py \
  --train-dir ./dump_ali/train/ \
  --dev-dir ./dump_ali/valid/ \
  --outdir ./examples/multiband_melgan/exp/train.multiband_melgan.bakerpp.v1/ \
  --config ./examples/multiband_melgan/conf/multiband_melgan.bakerpp.v1.yaml \
  --use-norm 1 \
  --generator_mixed_precision 1 \
  --resume "./examples/multiband_melgan/exp/train.multiband_melgan.bakerpp.v1/checkpoints/ckpt-100000" > train_multiband_melgan_pp.log 2>&1 &
#  --pretrained "./tftts_serving_flask/data/model/mb.melgan-920k.h5"  > train_multiband_melgan.log 2>&1 &

## training generator + discriminator:
CUDA_VISIBLE_DEVICES=3 nohup python -u examples/multiband_melgan/train_multiband_melgan.py \
  --train-dir ./dump/train/ \
  --dev-dir ./dump/valid/ \
  --outdir ./examples/multiband_melgan/exp/train.multiband_melgan.bakerpp.v1/ \
  --config ./examples/multiband_melgan/conf/multiband_melgan.bakerpp.v1.yaml \
  --use-norm 1 \
  --resume ./examples/multiband_melgan/exp/train.multiband_melgan.bakerpp.v1/checkpoints/ckpt-420000 > train_multiband_melgan_all.log 2>&1 &

