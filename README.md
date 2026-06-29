# Split Sheet — Music Royalty Calculator

A web app that calculates how music royalties should be split between
songwriters and publishers, based on industry-standard "Writer's Share" /
"Publisher's Share" structure used by PROs (Performance Rights
Organizations) like ASCAP and BMI.

Built by [Lorie B](https://soundbetter.com/profiles/726133-lorie-b) / AI Girl LLC.

## What it does

- Takes a total royalty amount (e.g. from a streaming payout, sync deal, or
  licensing fee)
- Splits it into a Writer's Share and Publisher's Share (default 50/50,
  but adjustable)
- Lets you add multiple writers and multiple publishers, each with their
  own percentage of their respective share
- Calculates the exact dollar amount and overall percentage each
  contributor receives
- Validates that percentages add up correctly before calculating, so you
  catch split-sheet errors before they go to print

## Why I built this

As an independent songwriter, I deal with split sheets regularly and
wanted a fast way to double-check the math on a deal before signing —
and to have something concrete to show as a coding sample. I built the
calculation logic and the web app myself in Python.

## Tech stack

- **Python 3** — core split calculation logic
- **Flask** — lightweight web framework for the UI
- **HTML / CSS / vanilla JS** — frontend, no frameworks needed
- **pytest-style tests** — covers the calculation logic, including edge
  cases (invalid percentages, custom share splits)

## Running it locally

```bash
# 1. Clone the repo and move into it
git clone <your-repo-url>
cd royalty-calculator

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
python app.py

# 4. Open in your browser
# http://localhost:5000
```

## Running the tests

```bash
python test_royalty_logic.py
```

All 6 tests should pass, covering:
- Even and uneven writer splits
- Custom writer/publisher share percentages (not just 50/50)
- Validation errors when percentages don't add up to 100%
- Rejecting invalid (negative) percentages

## Project structure

```
royalty-calculator/
├── app.py                  # Flask routes — connects the web form to the logic
├── royalty_logic.py         # Pure Python calculation logic (no web code)
├── test_royalty_logic.py    # Tests for the calculation logic
├── templates/
│   └── index.html           # The web page (form + results)
├── static/
│   ├── style.css            # Styling
│   └── script.js             # Adds/removes writer & publisher rows
└── requirements.txt
```

## Possible future additions

- Save/export a split sheet as a PDF
- Support for sync licensing splits (master + publishing separately)
- Multi-song batch calculator
- Account system to save past splits

## Disclaimer

This tool is for estimation purposes only. It is not a substitute for a
signed legal split sheet or professional legal/financial advice. Always
have real split sheets reviewed by an entertainment attorney.
