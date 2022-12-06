# setup environment
bash scripts/setup_env.sh

# download dataset
bash scripts/download_dataset.sh

# train model
# Usage: model_tester.py <path to weights> [path to embeddings]
python3 scripts/model_tester.sh $1 $2