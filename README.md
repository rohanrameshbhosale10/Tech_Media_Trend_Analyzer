# Tech-Media Trend Analyzer

A Python data pipeline that collects, processes, and visualizes
data from YouTube sources.

## Features
- Collects structured JSON via YouTube Data API v3
- Cleans and enriches data using Pandas (deduplication, engagement scoring, keyword tagging)
- Generates analytics dashboards with Matplotlib
- Exports analysis-ready CSV datasets

## Tech Stack
`Python` `Pandas` `Matplotlib` `YouTube Data API v3` `NewsAPI` `JSON` `REST APIs`

## How to Run
pip install -r requirements.txt
python collector.py
python processor.py
python dashboard.py

## Project Structure 
Tech-media-trend-analyzer/
├── collector.py        ← fetches data from YouTube & NewsAPI
├── processor.py        ← cleans, enriches, exports CSV
├── dashboard.py        ← generates analytics charts
├── requirements.txt    ← dependencies
├── .env.example        ← API keys
└── screenshots/        ← dashboard preview images
