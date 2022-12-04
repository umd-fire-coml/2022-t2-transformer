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
   pip install -U pip uvicorn tensorflow-macos -r requirements.txt
   ```

   For other computers

   ```bash
   pip install -U pip uvicorn tensorflow -r requirements.txt
   ```

1. Start dev server
   ```bash
   python3 -m uvicorn main:app --reload
   ```
