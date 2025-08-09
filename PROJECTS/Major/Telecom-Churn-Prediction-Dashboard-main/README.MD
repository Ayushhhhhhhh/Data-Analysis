# ChurnGuard Telecom Customer Churn Prediction Dashboard

A Data Science Project by Ayush Singhal

## 1. Project Overview & Business Problem

In the competitive telecommunications industry, customer retention is a key driver of profitability. Customer Churn, the rate at which customers leave a service, can significantly impact revenue. This project, ChurnGuard, leverages machine learning to proactively identify customers at a high risk of churning.

The goal is to move from a reactive to a proactive retention strategy. By predicting churn, a company can strategically intervene with targeted marketing campaigns, special offers, or customer support outreach to retain valuable customers before they leave. This project demonstrates an end-to-end data science workflow, from raw data exploration to a deployed, interactive web application.

## 2. The Dataset

This project utilizes the well-known Telco Customer Churn dataset from IBM, which contains 7,043 customer records from a fictional telecom company.

Key features include

-   Customer Demographics `gender`, `SeniorCitizen`, `Partner`, `Dependents`
-   Account Information `tenure`, `Contract`, `PaymentMethod`, `MonthlyCharges`, `TotalCharges`
-   Subscribed Services `PhoneService`, `InternetService`, `OnlineSecurity`, `TechSupport`, etc.
-   Target Variable `Churn` (YesNo)

## 3. The Workflow

The project follows a structured data science pipeline

Data Cleaning & Prep - Exploratory Data Analysis (EDA) - Feature Engineering - Predictive Modeling - Interactive Dashboard Deployment

## 4. Key Insights from EDA

-   Contract Type is Critical Customers on a Month-to-Month contract churn at a significantly higher rate than those on one or two-year contracts. This suggests that longer contracts are effective retention tools.
-   Internet Service Matters Customers with Fiber optic internet service have a higher churn rate compared to those with DSL. This could indicate issues with service quality, pricing, or perceived value.
-   Newer Customers are Flight Risks Churn is highest among customers with low tenure. Loyalty increases as the customer relationship lengthens.
-   Billing Preferences Customers using Paperless billing and Electronic check payments have a higher tendency to churn. This might point to issues in the billing process or a demographic that is more willing to switch providers.

## 5. Predictive Modeling

A `RandomForestClassifier` was trained to predict customer churn. This model was chosen for its strong performance and its ability to interpret feature importance.

-   Performance The model achieved an Accuracy of ~79% on the test set. More importantly, it demonstrates a practical ability to identify at-risk customers.
-   Key Predictors The model identified `Contract`, `tenure`, `MonthlyCharges`, and `InternetService` as the most influential factors in predicting churn.

## 6. The Interactive Dashboard

The final output is an interactive web application built with Streamlit. The dashboard allows a user (e.g., a marketing manager) to

-   Visualize key churn drivers through interactive charts.
-   Use the predictive model by inputting a customer's details to get an instant churn risk assessment.

## 7. How to Run This Project

### A. Run via Google Colab (Analysis & App Launch)

1.  Upload the project files to a `ChurnGuard` folder in your Google Drive.
2.  Open the `CustomerChurn.ipynb` notebook in Google Colab.
3.  Run the cells sequentially to install libraries, mount your Drive, and launch the app via ngrok.

### B. Run Locally (Requires Python)

1.  Clone this repository
    ```bash
    git clone [httpsgithub.comyour-usernameData-Analysis.git](httpsgithub.comyour-usernameData-Analysis.git)
    cd Data-Analysis
    ```
2.  Install the required packages
    ```bash
    pip install -r requirements.txt
    ```
3.  Launch the Streamlit dashboard
    ```bash
    streamlit run app.py
    ```
