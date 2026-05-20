# Tech-Media Trend Analyzer

A Python data pipeline that collects, processes, and visualizes
data from YouTube sources.

## Dashboard Preview
![Media Trend Analyzer Dashboard](https://github.com/rohanrameshbhosale10/Tech_Media_Trend_Analyzer/blob/5bb7d51147e82259bed979656b5691cba6114090/Youtube%20Analytics%20Dashboard.png)

## Features
- Collects structured JSON data via YouTube Data API v3 and NewsAPI
- Cleans and enriches data with Pandas — deduplication, null filtering, schema normalization
- Custom engagement scoring algorithm ranking videos by likes and comment velocity
- Keyword frequency analysis surfacing trending topics (Data Science, AI, Python, Machine Learning)
- 5-panel Matplotlib dashboards covering views, engagement, channels, and keyword presence
- Exports analysis-ready CSV datasets for BI tools and AI/ML model input

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
