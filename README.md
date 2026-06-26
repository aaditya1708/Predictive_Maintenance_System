# Predictive Maintenance System using Machine Learning

## Overview

This project develops a Predictive Maintenance System that predicts whether an industrial machine is likely to fail within the next 24 hours using machine telemetry, maintenance history, and error logs.

The objective is to help organizations reduce downtime, prevent unexpected breakdowns, and schedule maintenance proactively.

---

## Problem Statement

Machine failures can lead to production delays, increased maintenance costs, and operational losses. Traditional reactive maintenance strategies only address issues after failures occur.

This project uses Machine Learning to identify potential failures before they happen, enabling predictive maintenance.

---

## Dataset

The project uses the Microsoft Azure Predictive Maintenance dataset consisting of:

### Telemetry Data

Contains hourly sensor readings:

* Voltage (volt)
* Rotation Speed (rotate)
* Pressure
* Vibration

### Machine Data

Contains:

* Machine Model
* Machine Age

### Error Data

Contains machine-generated error events.

### Maintenance Data

Contains component replacement and maintenance history.

### Failure Data

Contains component failure records used to create the prediction target.

---

## Feature Engineering

The following features were used:

### Numerical Features

* Voltage
* Rotation Speed
* Pressure
* Vibration
* Machine Age
* Error Count (Last 24 Hours)
* Maintenance Count (Last 30 Days)

### Categorical Features

* Machine Model

### Target Variable

A binary target was created:

* 1 → Machine failure expected within the next 24 hours
* 0 → No failure expected within the next 24 hours

---

## Data Preprocessing

* Missing Value Analysis
* Duplicate Check
* Datetime Processing
* Feature Engineering
* One-Hot Encoding for categorical variables
* Standard Scaling for numerical variables
* ColumnTransformer Pipeline

---

## Machine Learning Models

The following models were trained and evaluated:

1. Logistic Regression
2. Random Forest Classifier
3. XGBoost Classifier

---

## Model Performance

| Model               | Accuracy |
| ------------------- | -------- |
| Logistic Regression | 93.57%   |
| Random Forest       | 98.86%   |
| XGBoost             | 98.78%   |

Since the dataset is highly imbalanced, model selection was based on Recall and F1-Score for failure prediction.

### Best Model: Random Forest

Performance for Failure Class:

* Precision: 0.55
* Recall: 0.80
* F1 Score: 0.66

The Random Forest model achieved the highest recall, successfully identifying 80% of machine failures.

---

## Technologies Used

* Python
* Pandas
* NumPy
* Scikit-Learn
* XGBoost
* Streamlit
* Matplotlib

---

## Project Workflow

1. Data Understanding
2. Data Cleaning
3. Exploratory Data Analysis
4. Feature Engineering
5. Target Variable Creation
6. Data Preprocessing Pipeline
7. Model Training
8. Model Evaluation
9. Model Selection
10. Streamlit Deployment

---

## Streamlit Application

The application allows users to:

* Enter machine sensor values
* Provide maintenance and error information
* Predict machine failure probability
* Receive maintenance risk alerts

---

## Future Improvements

* Hyperparameter Tuning
* SHAP Explainability
* Real-Time Sensor Integration
* Advanced Time-Series Features
* Cloud Deployment

---

## Author

Aaditya Hole

B.Tech Computer Engineering

Data Science & Machine Learning Enthusiast
