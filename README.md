# AutoEDA

AutoEDA is an automated Exploratory Data Analysis platform that allows users to upload a CSV dataset and receive profiling, data-quality analysis, statistics, and visualizations automatically.

## Features

- Automated dataset profiling
- Automatic data type detection
- Missing-value and duplicate analysis
- Numerical and categorical statistics
- Automatic chart generation
- Interactive Streamlit dashboard
- n8n workflow automation
- FastAPI + Pandas backend

## Tech Stack

- Python
- Pandas
- FastAPI
- n8n
- Streamlit
- Plotly

## Workflow

```text
CSV Upload
    ↓
Streamlit
    ↓
n8n Workflow
    ↓
FastAPI + Pandas
    ↓
Dataset Analysis
    ↓
Automatic Chart Generation
    ↓
Streamlit Dashboard

Tech Stack
Python
Pandas
FastAPI
Streamlit
Plotly
n8n
Requests
Project Structure
AutoEDA/
├── app.py
├── eda_api.py
├── requirements.txt
└── README.md
How It Works
Upload a CSV file through the Streamlit interface.
Streamlit sends the dataset to the n8n webhook.
n8n processes the dataset through the automated workflow.
FastAPI performs profiling, type inference, statistical analysis, and chart generation.
n8n combines the analysis results into a final JSON response.
Streamlit converts the response into an interactive dashboard.
Run Locally

## Install dependencies:

pip install -r requirements.txt

Start the FastAPI server:

uvicorn eda_api:app --reload --port 8000

Start n8n:

n8n start

Run Streamlit:

streamlit run app.py

Make sure the n8n webhook URL in app.py matches your active workflow.

## Purpose

Auto EDA is designed to reduce the repetitive work involved in initial exploratory data analysis by automatically profiling datasets and generating useful statistical insights and visualizations from a single CSV upload.

### Author: Hassam Ali
