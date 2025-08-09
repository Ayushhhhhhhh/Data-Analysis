import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
import numpy as np

# --- Page Configuration ---
st.set_page_config(
    page_title="ChurnGuard Telecom Dashboard",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Helper Functions ---
@st.cache_data
def load_data(path):
    """Loads the telecom churn data for visualization."""
    try:
        df = pd.read_csv(path)
        # The TotalCharges column might have spaces, convert to numeric, and fill NaNs
        df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
        df['TotalCharges'].fillna(df['TotalCharges'].median(), inplace=True)
        return df
    except FileNotFoundError:
        st.error(f"Error: The data file was not found at {path}.")
        st.info("Please ensure you have the 'telecom_churn_data.csv' file in a 'data' subfolder.")
        return None

@st.cache_resource
def load_model(model_path, columns_path):
    """Loads the trained model and the feature columns."""
    try:
        model = joblib.load(model_path)
        model_columns = joblib.load(columns_path)
        return model, model_columns
    except FileNotFoundError:
        st.error("Model files not found. Please ensure 'churn_model.joblib' and 'model_columns.joblib' are in the 'src/assets/' directory.")
        return None, None

# --- Load Model and Data ---
model, model_columns = load_model('src/assets/churn_model.joblib', 'src/assets/model_columns.joblib')
# This path assumes you have a 'data' folder in the same directory as app.py
df = load_data('data/telecom_churn_data.csv') 

# --- UI Layout ---
st.title("📡 ChurnGuard: Telecom Customer Churn Dashboard")
st.markdown("A Data Science Project by **Ayush Singhal**")

# --- Key Metrics ---
if df is not None:
    total_customers = df.shape[0]
    churned_customers = df[df['Churn'] == 'Yes'].shape[0]
    churn_rate = (churned_customers / total_customers) * 100 if total_customers > 0 else 0
    avg_tenure = df['tenure'].mean()

    st.markdown("### Key Metrics")
    kpi1, kpi2, kpi3 = st.columns(3)

    with kpi1:
        st.metric(
            label="Total Customers",
            value=f"{total_customers:,}"
        )

    with kpi2:
        st.metric(
            label="Churn Rate",
            value=f"{churn_rate:.2f}%"
        )

    with kpi3:
        st.metric(
            label="Average Tenure (Months)",
            value=f"{avg_tenure:.1f}"
        )
    
    st.markdown("<hr/>", unsafe_allow_html=True)


# --- Sidebar for Prediction ---
st.sidebar.header("Churn Predictor")
st.sidebar.markdown("Input customer details to predict churn probability.")

if model is not None and model_columns is not None:
    # Input fields
    tenure = st.sidebar.slider("Tenure (Months)", 0, 72, 24)
    monthly_charges = st.sidebar.slider("Monthly Charges ($)", 0.0, 120.0, 55.0, 0.01)
    total_charges = st.sidebar.slider("Total Charges ($)", 0.0, 9000.0, 1500.0, 0.01)
    contract = st.sidebar.selectbox("Contract Type", ['Month-to-month', 'One year', 'Two year'])
    payment_method = st.sidebar.selectbox("Payment Method", ['Electronic check', 'Mailed check', 'Bank transfer (automatic)', 'Credit card (automatic)'])
    internet_service = st.sidebar.selectbox("Internet Service", ['DSL', 'Fiber optic', 'No'])
    
    # Additional binary features for simplicity
    online_security = st.sidebar.radio("Online Security", ['Yes', 'No', 'No internet service'])
    tech_support = st.sidebar.radio("Tech Support", ['Yes', 'No', 'No internet service'])
    paperless_billing = st.sidebar.radio("Paperless Billing", ['Yes', 'No'])

    # Prediction logic
    if st.sidebar.button("Predict Churn", type="primary"):
        with st.spinner('Analyzing...'):
            # Create a dictionary from the inputs
            input_dict = {
                'SeniorCitizen': 0, # Assuming non-senior for simplicity
                'tenure': tenure,
                'MonthlyCharges': monthly_charges,
                'TotalCharges': total_charges,
                'gender': 'Male', # Assuming Male, as it has minor impact
                'Partner': 'Yes',
                'Dependents': 'No',
                'PhoneService': 'Yes',
                'MultipleLines': 'No',
                'InternetService': internet_service,
                'OnlineSecurity': online_security,
                'OnlineBackup': 'No',
                'DeviceProtection': 'No',
                'TechSupport': tech_support, 'StreamingTV': 'No', 'StreamingMovies': 'No',
                'Contract': contract, 'PaperlessBilling': paperless_billing, 'PaymentMethod': payment_method,
            }
            
            # Create a DataFrame from the dictionary
            input_df = pd.DataFrame([input_dict])
            
            # One-hot encode the input DataFrame and align columns with the training data
            input_encoded = pd.get_dummies(input_df).reindex(columns=model_columns, fill_value=0)
            
            # Make prediction
            prediction_proba = model.predict_proba(input_encoded)[0][1]

            st.subheader("Prediction Result")
            # Use a progress bar to visually represent the churn probability
            st.progress(prediction_proba)

            if prediction_proba > 0.5:
                st.error(f"High Risk: There is a {prediction_proba:.1%} probability of churn.", icon="🚨")
            elif prediction_proba > 0.25:
                st.warning(f"Moderate Risk: There is a {prediction_proba:.1%} probability of churn.", icon="⚠️")
            else:
                st.success(f"Low Risk: There is a {prediction_proba:.1%} probability of churn.", icon="✅")
else:
    st.sidebar.warning("Prediction model is not available. Please check file paths and ensure the model is trained.")


# --- Main Dashboard Visualizations ---
if df is not None:
    st.header("Exploratory Data Analysis")
    
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Churn Rate by Contract Type")
        fig_contract = px.pie(df, names='Contract', title='Contract Type Distribution', hole=0.3)
        st.plotly_chart(fig_contract, use_container_width=True)

    with col2:
        st.subheader("Churn Rate by Internet Service")
        fig_internet = px.sunburst(df, path=['InternetService', 'Churn'], title='Churn by Internet Service')
        st.plotly_chart(fig_internet, use_container_width=True)

    st.subheader("Tenure vs. Monthly Charges")
    fig_scatter = px.scatter(df, x='tenure', y='MonthlyCharges', color='Churn', 
                             title='Customer Churn by Tenure and Monthly Charges',
                             labels={'tenure': 'Tenure (Months)', 'MonthlyCharges': 'Monthly Charges ($)'},
                             hover_data=['Contract', 'PaymentMethod'])
    st.plotly_chart(fig_scatter, use_container_width=True)

else:
    st.info("Data for visualizations is not available.")
