from database import get_connection
import pandas as pd


# ---------- Categories ----------
def get_categories(txn_type):
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT CategoryID, CategoryName FROM categories WHERE CategoryType = %s"
    cursor.execute(query, (txn_type,))
    data = cursor.fetchall()   # list of (CategoryID, CategoryName)

    cursor.close()
    conn.close()
    return data


# ---------- Transactions ----------
def add_transaction(user_id, category_id, amount, txn_type, txn_date, note):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO transactions (UserID, CategoryID, amount, txnType, txnDate, note, createdat)
    VALUES (%s, %s, %s, %s, %s, %s, NOW())
    """
    cursor.execute(query, (user_id, category_id, amount, txn_type, txn_date, note))
    conn.commit()

    cursor.close()  
    conn.close()


def get_transactions(user_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)   # rows come back as dictionaries

    query = """
    SELECT t.TxnID, c.CategoryName, t.amount, t.txnType, t.txnDate, t.note
    FROM transactions t
    JOIN categories c ON t.CategoryID = c.CategoryID
    WHERE t.UserID = %s
    ORDER BY t.txnDate DESC
    """
    cursor.execute(query, (user_id,))
    data = cursor.fetchall()

    cursor.close()
    conn.close()
    return data


def delete_transaction(txn_id, user_id):
    conn = get_connection()
    cursor = conn.cursor()

    # UserID check means a user can only delete their own transactions
    query = "DELETE FROM transactions WHERE TxnID = %s AND UserID = %s"
    cursor.execute(query, (txn_id, user_id))
    conn.commit()

    cursor.close()
    conn.close()


def update_transaction(txn_id, user_id, amount, category_id, txn_type, txn_date, note):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    UPDATE transactions
    SET amount = %s, CategoryID = %s, txnType = %s, txnDate = %s, note = %s
    WHERE TxnID = %s AND UserID = %s
    """
    cursor.execute(query, (amount, category_id, txn_type, txn_date, note, txn_id, user_id))
    conn.commit()

    cursor.close()
    conn.close()


# ---------- For charts ----------
def get_dataframe(user_id):
    data = get_transactions(user_id)
    df = pd.DataFrame(data)
    if not df.empty:
        df['amount'] = df['amount'].astype(float)     # DECIMAL -> float
        df['txnDate'] = pd.to_datetime(df['txnDate'])
    return df