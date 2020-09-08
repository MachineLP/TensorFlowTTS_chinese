export PYTHONPATH=${PYTHONPATH}:../generate_tts_data/
python examples/run_normalize.py --rootdir ./dump --outdir ./dump --config data/baker_preprocess.yaml --dataset baker

# python examples/run_normalize.py --rootdir ./dump_ali --outdir ./dump_ali --config data/baker_preprocess.yaml --dataset baker