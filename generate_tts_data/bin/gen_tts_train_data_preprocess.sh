export PYTHONPATH=${PYTHONPATH}:../generate_tts_data/
python examples/run_preprocess.py --rootdir ./BZNSYP --outdir ./dump --config data/baker_preprocess.yaml --dataset baker

# --rootdir ./BZNSYP_ali --outdir ./dump_ali --config data/baker_preprocess.yaml --dataset baker