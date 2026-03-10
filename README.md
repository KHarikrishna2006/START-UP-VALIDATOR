# AI Startup Idea Validator

A Flask-based web application that helps validate startup ideas with a feasibility score, SWOT analysis, score charts, and improvement tips.

## Features
- Real authentication flow (register + login) with hashed passwords
- Role capture at signup (`founder`, `student`, `analyst`)
- Startup idea submission
- Automated score generation:
  - Market score
  - Competition score
  - Trend score
  - Feasibility score
- Hybrid scoring using both heuristic AI logic and live public web signals
- SWOT analysis, data-source transparency, and improvement tips
- SQLite-backed persistence with idea history

## Live data sources used
The validator attempts to pull web signals from public sources (no API keys required):
- Hacker News Algolia API (trend/activity signal)
- GitHub Search API (competition/ecosystem signal)
- DuckDuckGo Instant Answer API (market breadth signal)

If any source is unavailable, the system gracefully falls back to heuristic scoring.

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

## Proper usage flow
1. Register a new account from `/register`.
2. Log in with your registered credentials.
3. Submit startup idea title + description.
4. Review feasibility chart, SWOT, and live data source signals.

## Project structure
- `app.py` – Flask app and routes
- `validator.py` – scoring and SWOT generation logic
- `data_sources.py` – live web data signal collectors
- `templates/` – Flask HTML templates
- `static/` – CSS
- `docs/project_overview.md` – abstract, methodology, objective, and stack overview
