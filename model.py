import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

file_path = r"C:\Users\yprav\Downloads\family_financial_and_transactions_data.xlsx"
data = pd.read_excel(file_path, sheet_name='final_family_financial_and_tran')
data['Transaction Date'] = pd.to_datetime(data['Transaction Date'])
data.fillna(0,inplace=True)
data['Savings_to_Income'] = data['Savings']/data['Income']
data['Expenses_to_Income'] = data['Monthly Expenses']/data['Income']*100
data['Loan_to_Income'] = data['Loan Payments']/data['Income']*100
family_spending = data.groupby(['Family ID','Category'])['Amount'].sum().unstack()
print(family_spending)
correlation_data = data[['Income','Savings','Monthly Expenses','Loan Payments','Credit Card Spending']].corr()
sns.heatmap(correlation_data,annot=True,cmap='coolwarm')
plt.title('Correlation Between Finanical Metrics')
plt.show()
weights ={'Savings_to_Income':0.3,'Expenses_to_Income':0.2,'Loan_to_Income':0.2,'Credit Card Spending':0.1,'Financial Goals Met (%)':0.1,'Category_Spending_Balance':0.1}
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
import plotly.express as px

category_spending = data.groupby('Category')['Amount'].sum().reset_index()
fig = px.pie(category_spending, values='Amount', names='Category', title='Spending Distribution by Category')
fig.show()

family_scores = data.groupby('Family ID')['Financial_Health_Score'].mean().reset_index()
fig = px.bar(family_scores, x='Family ID', y='Financial_Health_Score', title='Family Financial Scores')
fig.show()

member_spending = data.groupby(['Member ID', 'Transaction Date'])['Amount'].sum().reset_index()
fig = px.line(member_spending, x='Transaction Date', y='Amount', color='Member ID', title='Member Spending Trends')
fig.show()