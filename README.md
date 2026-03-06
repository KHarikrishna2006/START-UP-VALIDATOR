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

## Run locally
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Then open: `http://localhost:5000`

## Project structure
- `app.py` – Flask app and routes
- `validator.py` – scoring and SWOT generation logic
- `templates/` – Flask HTML templates
- `static/` – CSS
- `docs/project_overview.md` – abstract, methodology, objective, and stack overview
