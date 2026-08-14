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

