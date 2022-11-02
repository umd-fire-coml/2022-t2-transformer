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
   ```bash
   pip install -U pip uvicorn -r requirements.txt
   ```
1. Start dev server
   ```bash
   python3 -m uvicorn main:app --reload
   ```
