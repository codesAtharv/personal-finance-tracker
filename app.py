import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import auth
import functions

# check if user is logged in or not
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# if not logged in show login page
if st.session_state['logged_in'] == False:
    auth.show_login_screen()

# otherwise show the main app
else:
    user_id = st.session_state['user_id']

    st.sidebar.title("Finance Tracker")
    page = st.sidebar.radio("Go to", ["Add Transaction", "View Transactions", "Charts"])

    if st.sidebar.button("Logout"):
        st.session_state['logged_in'] = False
        st.session_state['user_id'] = None
        st.rerun()

    # ---- Add Transaction page ----
    if page == "Add Transaction":
        st.title("Add Transaction")

        txn_type = st.selectbox("Type", ["expense", "income"])

        # get categories of selected type from database
        categories = functions.get_categories(txn_type)

        category_names = []
        category_ids = {}
        for cat in categories:
            category_names.append(cat[1])    # cat[1] is the name
            category_ids[cat[1]] = cat[0]    # cat[0] is the id

        amount = st.number_input("Amount", min_value=0.01)
        txn_date = st.date_input("Date")
        category_name = st.selectbox("Category", category_names)
        note = st.text_input("Note")

        if st.button("Save"):
            category_id = category_ids[category_name]
            functions.add_transaction(user_id, category_id, amount, txn_type, txn_date, note)
            st.success("Transaction added")

    # ---- View Transactions page ----
    elif page == "View Transactions":
        st.title("Your Transactions")

        df = functions.get_dataframe(user_id)

        if df.empty:
            st.write("No transactions yet")
        else:
            st.dataframe(df)

            txn_id = st.selectbox("Select TxnID to delete", df['TxnID'])
            if st.button("Delete"):
                functions.delete_transaction(txn_id, user_id)
                st.rerun()

    # ---- Charts page ----
    else:
        st.title("Charts")

        df = functions.get_dataframe(user_id)

        if df.empty:
            st.write("No data yet, add some transactions first")
        else:
            # add a month column like 2026-09
            df['month'] = df['txnDate'].dt.strftime('%Y-%m')

            # user selects which month to see (latest month comes first)
            month_list = sorted(df['month'].unique(), reverse=True)
            selected_month = st.selectbox("Select Month", month_list)

            # keep only the data of the selected month
            month_df = df[df['month'] == selected_month]
            income_df = month_df[month_df['txnType'] == 'income']
            expense_df = month_df[month_df['txnType'] == 'expense']

            total_income = income_df['amount'].sum()
            total_expense = expense_df['amount'].sum()
            balance = total_income - total_expense

            st.subheader("Summary of " + selected_month)
            st.write("Total Income:", total_income)
            st.write("Total Expense:", total_expense)
            st.write("Balance:", balance)

            # chart 1 - expense by category (only selected month)
            st.subheader("Expense by Category")
            if len(expense_df) > 0:
                category_total = expense_df.groupby('CategoryName')['amount'].sum()
                fig1 = plt.figure()
                plt.pie(category_total, labels=category_total.index)
                st.pyplot(fig1)
            else:
                st.write("No expenses in this month")

            # chart 2 - income and expense of every month
            st.subheader("Month wise Income vs Expense")

            all_months = sorted(df['month'].unique())
            income_list = []
            expense_list = []

            for m in all_months:
                data = df[df['month'] == m]
                income_list.append(data[data['txnType'] == 'income']['amount'].sum())
                expense_list.append(data[data['txnType'] == 'expense']['amount'].sum())

            x = np.arange(len(all_months))
            fig2 = plt.figure()
            plt.bar(x - 0.2, income_list, width=0.4, color='green', label='Income')
            plt.bar(x + 0.2, expense_list, width=0.4, color='red', label='Expense')
            plt.xticks(x, all_months)
            plt.xlabel("Month")
            plt.ylabel("Amount")
            plt.legend()
            st.pyplot(fig2)