# Social Media Intelligence Platform

A Python data pipeline that collects, processes, and visualizes
data from YouTube and global news sources.

## Features
- Collects structured JSON via YouTube Data API v3 and NewsAPI
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