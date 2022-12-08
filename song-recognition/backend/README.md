## Usage

**From the root directory**

1. Setup environment
   ```bash
   bash scripts/setup_env.sh
   ```
1. Run server
   ```bash
   cd backend
   uvicorn main:app --reload
   ```

## Development

**First, make sure you are in the `backend/` directory**

1. Create and activate virtual env
   - Create
     ```bash
     python3 -m venv .venv
     ```
   - Activate
     ```bash
     source .venv/bin/activate
     ```
1. Install dependencies
   If on apple silicon chip:

   ```bash
   pip install -U pip uvicorn -r requirements.txt tensorflow-macos
   ```

   For other computers

   ```bash
   pip install -U pip uvicorn -r requirements.txt tensorflow
   ```

1. Start dev server
   ```bash
   python3 -m uvicorn main:app --reload
   ```
