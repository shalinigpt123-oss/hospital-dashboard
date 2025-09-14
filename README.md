# RapidClaims Dashboard

A Streamlit-based dashboard prototype for hospital revenue cycle management.

## Features

### Financial Health Page
- **Claims Resolution Timeline**: Interactive pie chart showing how quickly claims are resolved
- **Payment Tracker**: Comprehensive table with claim details and payment information
- **Filtering Options**: View data by Overall, Payer, or Department
- **Key Metrics**: Avg. Number of days for Claim resolution, Total Raised, Total Received, Collection Rate

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Run the Streamlit app:
```bash
streamlit run app.py
```

## Usage

The dashboard will open in your default web browser. Navigate through the different views using the sidebar and filter options to analyze your hospital's revenue cycle performance.

## Sample Data

The app includes generated sample data for demonstration purposes, including:
- 200+ sample claims
- Multiple payers (Medicare, Medicaid, Blue Cross, etc.)
- Various departments (Cardiology, Orthopedics, Emergency, etc.)
- Realistic payment amounts and resolution timelines
