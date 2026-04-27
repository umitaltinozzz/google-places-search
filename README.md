<div align="center">

# Google Places Business Search

**Bulk business search and CSV export tool for Istanbul districts**

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](./LICENSE)

</div>

---

## Overview

A Python desktop application that searches for businesses across Istanbul districts using the Google Places API, with multi-keyword support and automatic CSV export per search session.

## Features

- Search across multiple Istanbul districts simultaneously
- Multi-keyword search in a single run
- Maximum rating filter
- Results displayed in a live table
- Auto-exports each search to a uniquely timestamped CSV file
- Search history with ability to revisit past results
- UTF-8-SIG encoding for Turkish character support

## Requirements

`ash
pip install requests pandas
`

> Tkinter is included with Python. On Linux: sudo apt-get install python3-tk

## Usage

`ash
python google_places_arama.py
`

1. Enter your Google Places API key
2. Enter keywords (one per line)
3. Enter districts (one per line)
4. Set a maximum rating (e.g. 4.0)
5. Click **Start Search**

Results appear in the table and are saved to a timestamped CSV file automatically.

Get an API key at [Google Cloud Console](https://console.cloud.google.com/).

## License

MIT
