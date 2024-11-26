import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

def calculate_financial_score(data):
    weights = {
        'Savings_to_Income': 0.3,
        'Expenses_to_Income': 0.2,
        'Loan_to_Income': 0.2,
        'Credit Card Spending': 0.1,
        'Financial Goals Met (%)': 0.1,
        'Category_Spending_Balance': 0.1
    }

    data['Savings_to_Income'] = data['Savings'] / data['Income']
    data['Expenses_to_Income'] = data['Monthly Expenses'] / data['Income'] * 100
    data['Loan_to_Income'] = data['Loan Payments'] / data['Income'] * 100

    data['Savings_to_Income_Score'] = np.clip(data['Savings_to_Income'] * 100, 0, 100)
    data['Expenses_to_Income_Score'] = 100 - data['Expenses_to_Income']
    data['Loan_to_Income_Score'] = 100 - data['Loan_to_Income']
    data['Category_Spending_Balance'] = 100 - (data['Amount'] / data['Income'] * 100)

    data['Financial_Health_Score'] = (
            weights['Savings_to_Income'] * data['Savings_to_Income_Score'] +
            weights['Expenses_to_Income'] * data['Expenses_to_Income_Score'] +
            weights['Loan_to_Income'] * data['Loan_to_Income_Score'] +
            weights['Credit Card Spending'] * (100 - data['Credit Card Spending'] / 100) +
            weights['Financial Goals Met (%)'] * data['Financial Goals Met (%)'] +
            weights['Category_Spending_Balance'] * data['Category_Spending_Balance']
    )

    return data['Financial_Health_Score'].iloc[0]

st.title('Family Financial Health Dashboard')

income = st.number_input("Enter your Family Income", min_value=0, value=70000)
savings = st.number_input("Enter your Savings", min_value=0, value=3000)
monthly_expenses = st.number_input("Enter your Monthly Expenses", min_value=0, value=2000)
loan_payments = st.number_input("Enter your Loan Payments", min_value=0, value=1500)
credit_card_spending = st.number_input("Enter your Credit Card Spending", min_value=0, value=1000)
financial_goals_met = st.number_input("Enter your Financial Goals Met (%)", min_value=0, max_value=100, value=70)

data = {
    "Family ID": [1],
    "Income": [income],
    "Savings": [savings],
    "Monthly Expenses": [monthly_expenses],
    "Loan Payments": [loan_payments],
    "Credit Card Spending": [credit_card_spending],
    "Financial Goals Met (%)": [financial_goals_met],
    "Amount": [1500],
    "Category": ['Living']
}

df = pd.DataFrame(data)

score = calculate_financial_score(df)
st.write(f"Your Financial Health Score: {score:.2f}")

st.write("### Insights")
st.write(f"Savings are {'below' if savings < 5000 else 'above'} the recommended levels.")
st.write(f"Reducing discretionary spending by 10% can improve your score by {0.2 * score:.2f} points.")

category_spending = df.groupby('Category')['Amount'].sum().reset_index()
fig = px.pie(category_spending, values='Amount', names='Category', title='Spending Distribution by Category')
st.plotly_chart(fig)

st.write("### Financial Goal Progress")
st.progress(financial_goals_met)
