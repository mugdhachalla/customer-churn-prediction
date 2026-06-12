import streamlit as st
import pickle
import pandas as pd




st.set_page_config(
    page_title="Customer Churn Predictor",
    page_icon="📉",
    layout="wide",
    initial_sidebar_state="collapsed"
)



model = pickle.load(open("model.pkl", "rb"))
scaler = pickle.load(open("scaler.pkl", "rb"))



st.title("Customer Churn Prediction")

st.write(
    "Predict whether a customer is likely to leave the bank."
)



st.subheader("Customer Information")

# Row 1

col1, col2, col3 = st.columns(3)

with col1:
    credit_score = st.number_input(
        "Credit Score",
        min_value=300,
        max_value=900,
        value=650
    )

with col2:
    age = st.number_input(
        "Age",
        min_value=18,
        max_value=100,
        value=35
    )

with col3:
    tenure = st.number_input(
        "Tenure",
        min_value=0,
        max_value=10,
        value=5
    )

# Row 2

col1, col2, col3 = st.columns(3)

with col1:
    balance = st.number_input(
        "Balance",
        min_value=0.0,
        value=50000.0
    )

with col2:
    products = st.number_input(
        "Number of Products",
        min_value=1,
        max_value=4,
        value=1
    )

with col3:
    salary = st.number_input(
        "Estimated Salary",
        min_value=0.0,
        value=50000.0
    )

# Row 3

col1, col2, col3, col4 = st.columns(4)

with col1:
    gender = st.selectbox(
        "Gender",
        ["Male", "Female"]
    )

with col2:
    has_card = st.selectbox(
        "Has Credit Card",
        ["Yes", "No"]
    )

with col3:
    active_member = st.selectbox(
        "Active Member",
        ["Yes", "No"]
    )

with col4:
    country = st.selectbox(
        "Country",
        ["France", "Germany", "Spain"]
    )



gender = 1 if gender == "Female" else 0

has_card = 1 if has_card == "Yes" else 0

active_member = 1 if active_member == "Yes" else 0

geo_germany = 1 if country == "Germany" else 0

geo_spain = 1 if country == "Spain" else 0


if st.button("Predict Churn"):

    features = [[
        credit_score,
        gender,
        age,
        tenure,
        balance,
        products,
        has_card,
        active_member,
        salary,
        geo_germany,
        geo_spain
    ]]

    features = scaler.transform(features)

    prediction = model.predict(features)

    probability = model.predict_proba(features)

    churn_prob = probability[0][1]

    st.subheader("Prediction Result")

    if churn_prob >= 0.70:

        st.error(
            f"🔴 High Churn Risk\n\nProbability: {churn_prob:.2%}"
        )

    elif churn_prob >= 0.40:

        st.warning(
            f"🟡 Medium Churn Risk\n\nProbability: {churn_prob:.2%}"
        )

    else:

        st.success(
            f"🟢 Low Churn Risk\n\nProbability: {churn_prob:.2%}"
        )

    st.progress(float(churn_prob))

    st.write(
        f"Predicted Churn Probability: **{churn_prob:.2%}**"
    )

importance = pd.read_csv(
    "feature_importance.csv"
)

st.subheader("Feature Importance")

st.bar_chart(
    importance.set_index("Feature")
)

st.markdown("### Example High Risk Customer")

st.code("""
Age: 55
Balance: 120000
Active Member: No
Country: Germany
""")