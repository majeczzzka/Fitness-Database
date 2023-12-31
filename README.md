# Health and Fitness Tracking App

## Overview

The Health and Fitness Tracking App is a comprehensive solution designed to help users monitor and improve their health and fitness. It enables tracking of various health metrics, including workout sessions, nutrition, sleep patterns, and offers personalized fitness recommendations. This application is ideal for individuals looking to achieve fitness goals and maintain a healthy lifestyle.

## Primary Objectives:

Comprehensive Health Monitoring: To provide a platform where users can track a wide range of health and fitness metrics, enabling a complete overview of their well-being.
Goal Setting and Progress Tracking: To assist users in setting realistic health and fitness goals and track their progress over time.
Personalized Recommendations: To offer personalized tips and recommendations based on the user’s unique health data and progress.
Encourage Healthy Habits: To motivate users to adopt and maintain healthy lifestyle habits through regular monitoring and feedback.

## Target Audience:

The app caters to a diverse range of users, including:

Fitness enthusiasts seeking to track their workout and dietary habits.
People with specific health conditions who need to monitor various health metrics regularly.
Anyone interested in maintaining an overall healthy lifestyle and keen on having a data-driven approach to their health.

## Installation

### For macOS:

```bash
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
python3 create.py
python3 insert_data.py
python3 query_data.py
```

### For Windows:

```bash
python3 -m venv venv
venv\Scripts\activate.bat
pip3 install -r requirements.txt
python3 create.py
python3 insert_data.py
python3 query_data.py
```

## Database Schema

The application utilizes a robust SQL database schema, including tables for users, workouts, nutrition, and sleep data. The schema is designed to ensure efficient data management and retrieval.

## Usage

The application allows users to log and track various health metrics. Users can view their progress in different categories and receive personalized recommendations based on their data.

## Queries and Data Analysis

The app includes various SQL queries to analyze data, such as:

- Sleep goal assessments.
- Minimum sleep duration for good sleep quality.
- BMI calculations and categorizations.
- Analysis of workout performances.
- Total Daily Energy Expenditure (TDEE) calculations.

## Libraries Used

- Python 3.8.8
- SQLite 3.35.4
- SQLAlchemy 2.0.3
- Tabulate 0.9.0
- Faker 16.8.1
