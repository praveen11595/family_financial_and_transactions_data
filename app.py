from flask import Flask, request, jsonify
import pandas as pd
import numpy as np

app = Flask(__name__)

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

@app.route('/')
def home():
    return "Welcome to the Family Financial Health API. Use /get_financial_score to get the financial score."

@app.route('/get_financial_score', methods=['POST'])
def get_financial_score():
    family_data = request.json
    df = pd.DataFrame([family_data])
    score = calculate_financial_score(df)
    insights = {
        "score": score,
        "insights": [
            {"Savings": f"Savings are {'below' if df['Savings'][0] < 5000 else 'above'} the recommended levels."},
            {"Spending": f"Reduce discretionary spending by 10% to improve your score by {0.2 * score:.2f} points."}
        ]
    }

    return jsonify(insights)


if __name__ == "__main__":
    app.run(debug=True)
