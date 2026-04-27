# Google Places Business Search

**Bulk business discovery and CSV export tool for Istanbul districts**

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Tkinter](https://img.shields.io/badge/Tkinter-GUI-FF6F00?style=for-the-badge&logo=python&logoColor=white)](https://docs.python.org/3/library/tkinter.html)
[![Google Places](https://img.shields.io/badge/Google_Places-API-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://developers.google.com/maps/documentation/places/web-service)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](./LICENSE)

&nbsp;

---

> *Built out of frustration — spending hours manually copying business names, phone numbers, and addresses from Google Maps into a spreadsheet, district by district.*

## The Story

I needed a list of businesses across Istanbul — restaurants, clinics, law firms — for a small outreach project. The manual process was brutal: search a keyword, scroll through results, copy the name, copy the phone number, note the district. Repeat for 39 districts.

After a few hours of this, I stopped and wrote a script instead.

What started as a quick automation turned into a proper desktop application with a live results table, multi-keyword support, and automatic CSV export. It ended up saving days of manual work.

## Overview

Google Places Business Search is a Python desktop application built on top of the Google Places API. Enter your keywords and districts, set a rating filter, and let it do the searching — results appear live in a table and are automatically exported to a timestamped CSV file ready for analysis or outreach.

**What it handles for you:**
- Iterates across all selected Istanbul districts automatically
- Runs multiple keywords in a single session
- Filters out high-rated businesses (noise reduction for outreach lists)
- Handles UTF-8-SIG encoding so Turkish characters display correctly in Excel

## Features

- **District-based search** — Queries run automatically for each selected Istanbul district
- **Multi-keyword support** — Enter multiple search terms at once; each runs across all selected districts
- **Rating filter** — Set a maximum rating threshold to narrow results (e.g. below `4.0` only)
- **Live results table** — Results populate in real-time as each API query completes
- **Auto CSV export** — Each session saves to a uniquely timestamped file; no manual saving needed
- **Search history** — Revisit and re-export results from past sessions within the same run
- **Turkish character support** — UTF-8-SIG encoding ensures clean output in Excel

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.x |
| GUI | Tkinter (built-in) |
| HTTP | Requests |
| Data | Pandas |
| API | Google Places API (Text Search) |
| Output | CSV (UTF-8-SIG) |

## Getting Started

```bash
git clone https://github.com/umitaltinozzz/google-places-search.git
cd google-places-search

# Install dependencies
pip install requests pandas

# Copy environment config
cp .env.example .env
# Paste your Google Places API key into .env

# Run
python google_places_arama.py
```

> **Linux only:** Tkinter is not always bundled — install it with `sudo apt-get install python3-tk`

Get your API key at [Google Cloud Console](https://console.cloud.google.com/). Enable the **Places API** for your project.

### Using the App

| Step | Action |
|---|---|
| 1 | Paste your Google Places API key into the field |
| 2 | Enter keywords, one per line (e.g. `restoran`, `klinik`, `avukat`) |
| 3 | Enter districts, one per line (e.g. `Kadıköy`, `Beşiktaş`, `Şişli`) |
| 4 | Set a maximum rating (e.g. `4.0`) |
| 5 | Click **Start Search** and watch results populate live |

Results are saved automatically to a timestamped CSV in the project folder.

## Project Structure

```
google-places-search/
├── google_places_arama.py   # Main application (GUI + API logic)
├── .env.example             # API key template
├── .gitignore               # Excludes .env and CSV outputs
├── requirements.txt
└── README.md
```

## License

[MIT](./LICENSE)
