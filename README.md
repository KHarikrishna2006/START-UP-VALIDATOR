# AI Startup Idea Validator

A Flask-based web application that helps validate startup ideas with a feasibility score, SWOT analysis, score charts, and improvement tips.

## Features
- Demo login/signup flow
- Startup idea submission
- Automated score generation:
  - Market score
  - Competition score
  - Trend score
  - Feasibility score
- SWOT analysis and improvement tips
- SQLite-backed persistence with idea history

## Run from GitHub

### 1) Clone repository
```bash
git clone <your-github-repo-url>
cd START-UP-VALIDATOR
```

### 2) Create virtual environment
```bash
python -m venv .venv
```

### 3) Activate virtual environment

#### Windows PowerShell
```powershell
.\.venv\Scripts\Activate.ps1
```

> If script execution is blocked, run this once in the same PowerShell window and retry activation:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

#### Windows CMD
```cmd
.venv\Scripts\activate.bat
```

#### Git Bash / Linux / macOS
```bash
source .venv/bin/activate
```

### 4) Install dependencies
```bash
pip install -r requirements.txt
```

### 5) Run application
```bash
python app.py
```

### 6) Open in browser
`http://localhost:5000`

## Quick run (PowerShell)
Run these commands line-by-line (not as one line with `\n` characters):
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

## Project structure
- `app.py` – Flask app and routes
- `validator.py` – scoring and SWOT generation logic
- `templates/` – Flask HTML templates
- `static/` – CSS
- `docs/project_overview.md` – abstract, methodology, objective, and stack overview
