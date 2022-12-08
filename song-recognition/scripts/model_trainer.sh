# setup environment
bash scripts/setup_env.sh

# download dataset
bash scripts/download_dataset.sh

# train model
# Usage: model_trainer.py <number of epochs>
if(($#==1)); then # if num args is 1, use num epochs passed, use that.
    python3 scripts/model_trainer.sh $1
else
    # 100 epocs default
    python3 scripts/model_trainer.sh 100
fi