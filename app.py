import streamlit as st
import pandas as pd
import plotly.express as px
from expenses_db import add_income, add_expense, add_savings, get_data
from datetime import datetime, timedelta


st.set_page_config(page_title="Personal Finance Manager",
                   layout="centered",
                   page_icon=":sparkles:",
                   
                  )

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Monitoring", "Data Input"])

if page == "Monitoring":
    st.title("Monitoring Dashboard")
    
    # Date filter
    st.sidebar.header("Filters")
    filter_option = st.sidebar.selectbox("Select Time Period", ["Past Week", "Past Month", "Custom Date Range"])
    
    if filter_option == "Past Week":
        start_date = datetime.today() - timedelta(days=7)
        end_date = datetime.today()
    elif filter_option == "Past Month":
        start_date = datetime.today() - timedelta(days=30)
        end_date = datetime.today()
    elif filter_option == "Custom Date Range":
        start_date = st.sidebar.date_input("Start Date", value=datetime.today() - timedelta(days=30))
        end_date = st.sidebar.date_input("End Date", value=datetime.today())

    # Filter dataframes by the selected date range
    income_df = get_data("Income")
    income_df['date'] = pd.to_datetime(income_df['date'])
    income_df = income_df[(income_df['date'] >= pd.to_datetime(start_date)) & (income_df['date'] <= pd.to_datetime(end_date))]
    
    expenses_df = get_data("Expenses")
    expenses_df['date'] = pd.to_datetime(expenses_df['date'])
    expenses_df = expenses_df[(expenses_df['date'] >= pd.to_datetime(start_date)) & (expenses_df['date'] <= pd.to_datetime(end_date))]
    
    savings_df = get_data("Savings")
    savings_df['date'] = pd.to_datetime(savings_df['date'])
    savings_df = savings_df[(savings_df['date'] >= pd.to_datetime(start_date)) & (savings_df['date'] <= pd.to_datetime(end_date))]

    # Monthly Overview
    st.header("Monthly Overview")
    
    total_income = income_df['amount'].sum()
    total_expenses = expenses_df['amount'].sum()
    total_savings = savings_df['amount'].sum()
    current_balance = total_income - total_expenses

    st.metric("Total Income", f"₦{total_income}")
    st.metric("Total Expenses", f"₦{total_expenses}")
    st.metric("Total Savings", f"₦{total_savings}")
    st.metric("Current Balance", f"₦{current_balance}")

    # Spending Categories
    st.header("Spending Categories")
    if not expenses_df.empty:
        category_sum = expenses_df.groupby("category")["amount"].sum().reset_index()
        fig = px.pie(category_sum, names='category', values='amount', title='Spending by Category')
        st.plotly_chart(fig)

    # Savings Goals
    st.header("Savings Goals")
    fig = px.line(savings_df, x="date", y="amount", title='Savings Over Time')
    st.plotly_chart(fig)

    # Additional Plots

    # Income vs Expenses Over Time
    st.header("Income vs. Expenses Over Time")
    income_vs_expenses_df = pd.concat([
        income_df.assign(Type='Income')[['date', 'amount', 'Type']],
        expenses_df.assign(Type='Expenses')[['date', 'amount', 'Type']]
    ])
    fig = px.line(income_vs_expenses_df, x='date', y='amount', color='Type', title='Income vs. Expenses Over Time')
    st.plotly_chart(fig)

    # Monthly Income and Expenses Comparison
    st.header("Monthly Income and Expenses Comparison")
    income_df['month'] = income_df['date'].dt.to_period('M')
    expenses_df['month'] = expenses_df['date'].dt.to_period('M')
    
    monthly_income = income_df.groupby('month')['amount'].sum().reset_index()
    monthly_expenses = expenses_df.groupby('month')['amount'].sum().reset_index()
    
    monthly_comparison_df = pd.merge(monthly_income, monthly_expenses, on='month', suffixes=('_Income', '_Expenses'))
    st.write(monthly_comparison_df.head())
    monthly_comparison_df['month'] = monthly_comparison_df['month'].astype(str)
    fig = px.bar(monthly_comparison_df, x='month', y=['amount_Income', 'amount_Expenses'], 
                 barmode='group', title='Monthly Income and Expenses Comparison')
    st.plotly_chart(fig)

    # Cumulative Savings Over Time
    st.header("Cumulative Savings Over Time")
    savings_df = savings_df.sort_values('date')
    savings_df['cumulative_savings'] = savings_df['amount'].cumsum()

    st.write('Last 10 Savings Table')
    st.write(savings_df.tail(10))
    fig = px.line(savings_df, x='date', y='amount', title='Savings Over Time')
    st.plotly_chart(fig)


elif page == "Data Input":
    st.title("Data Input")

    st.header("Add New Income")
    with st.form(key='income_form'):
        income_date = st.date_input("Date")
        income_source = st.text_input("Source").upper()
        income_amount = st.number_input("Amount", min_value=0.0, format="%.2f")
        submit_income = st.form_submit_button(label='Add Income')
        
        if submit_income:
            add_income(income_date, income_source, income_amount)
            st.success(f"Added income: {income_source} - ${income_amount} on {income_date}")

    st.header("Add New Expense")
    with st.form(key='expense_form'):
        expense_date = st.date_input("Date")
        expense_category = st.text_input("Category").upper()
        expense_amount = st.number_input("Amount", min_value=0.0, format="%.2f")
        expense_description = st.text_area("Description")
        submit_expense = st.form_submit_button(label='Add Expense')
        
        if submit_expense:
            add_expense(expense_date, expense_category.upper(), expense_amount, expense_description)
            st.success(f"Added expense: {expense_category} - ${expense_amount} on {expense_date}")

    st.header("Add New Savings")
    with st.form(key='savings_form'):
        savings_date = st.date_input("Date")
        savings_amount = st.number_input("Amount", min_value=0.0, format="%.2f")
        submit_savings = st.form_submit_button(label='Add Savings')
        
        if submit_savings:
            add_savings(savings_date, savings_amount)
            st.success(f"Added savings: ${savings_amount} on {savings_date}")
