# Personal Finance Tracker

A web app to track your income and expenses, built with Python, MySQL and Streamlit. Each user has their own account and sees only their own transactions, with monthly charts to understand spending.

## Features

- User registration and login (passwords are stored as hashes)
- Add income and expense transactions with a category, date and note
- View and delete your transactions
- Monthly summary: total income, total expense and balance
- Charts: expense by category (pie) and month-wise income vs expense (bar)

## Tech Stack

- Python
- Streamlit (frontend)
- MySQL 8.0+ (database)
- pandas, NumPy, Matplotlib (data handling and charts)
- mysql-connector-python, python-dotenv

## Project Structure

```
├── app.py               # Streamlit app (pages and charts)
├── auth.py              # Login and registration
├── database.py          # MySQL connection (reads .env)
├── functions.py         # Database queries
├── test1.py             # Quick database connection check
├── requirements.txt
├── .env.example         # Template for database settings
└── database/
    ├── schema.sql       # Creates the database and tables
    └── seed_categories.sql   # Default categories
```

## Setup

**Requires Python 3.9+ and MySQL 8.0+.**

1. Clone the repo

   ```
   git clone https://github.com/codesAtharv/personal-finance-tracker.git
   cd personal-finance-tracker
   ```

2. Install the packages

   ```
   pip install -r requirements.txt
   ```

3. Create the database and tables, then add the default categories

   ```
   mysql -u root -p < database/schema.sql
   mysql -u root -p < database/seed_categories.sql
   ```

   On Windows PowerShell the `<` symbol doesn't work. Use Command Prompt, or open `mysql -u root -p` and run:

   ```
   source database/schema.sql
   source database/seed_categories.sql
   ```

4. Create your settings file. Copy `.env.example` to `.env` and enter your MySQL password:

   ```
   DB_HOST=localhost
   DB_USER=root
   DB_PASSWORD=your_mysql_password
   DB_NAME=financetracker
   ```

5. Run the app

   ```
   streamlit run app.py
   ```

Then register a new account, log in and add your first transaction.

## Screenshots

Login Page:
<img width="1917" height="1010" alt="image" src="https://github.com/user-attachments/assets/b1c15cfb-64fe-4ae1-8486-4be58d85c7d6" />

Home Page:
<img width="1917" height="1020" alt="image" src="https://github.com/user-attachments/assets/048c9088-caf7-41c0-9893-e7e70d2d310b" />

Transactions Page:
<img width="1917" height="1013" alt="image" src="https://github.com/user-attachments/assets/e6134b50-15c1-4c9c-be81-d5eddc510980" />

Charts:
<img width="1915" height="1008" alt="image" src="https://github.com/user-attachments/assets/8f8985c2-cd54-4c6c-8f6f-2afc8d4db98a" />
<img width="673" height="832" alt="image" src="https://github.com/user-attachments/assets/afcbb1a5-2d84-4f6c-b37b-a10c9bcc6846" />




## Known Limitations

- Passwords use unsalted SHA-256. bcrypt would be a stronger choice.
- Transactions can be added and deleted, but there is no edit page yet (the `update_transaction` function exists and is not used in the UI).

## Future Improvements

- Edit transactions
- Switch to bcrypt for password hashing
- Export transactions to CSV
- Monthly budget limits

## Author

Atharva Bajaj
codesAtharv
