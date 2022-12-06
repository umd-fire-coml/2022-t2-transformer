python3 -m venv .venv

source .venv/bin/activate

# install requirements (not apple silicon)
pip3 install -U pip uvicorn -r requirements.txt tensorflow

# setup frontend
cd frontend/
npm i
cd ../
