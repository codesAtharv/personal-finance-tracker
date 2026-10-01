import streamlit as st
import hashlib
from database import get_connection


# Turn the password into a fixed-length hash so plain passwords are never stored
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def register_user(username, email, password):
    conn = get_connection()
    cursor = conn.cursor()

    # Step 1: check if the username is already taken
    cursor.execute("SELECT UserID FROM users WHERE Username = %s", (username,))
    if cursor.fetchone():
        cursor.close()
        conn.close()
        return False

    # Step 2: save the new user (with hashed password)
    query = """
    INSERT INTO users (Username, password, email, createdat)
    VALUES (%s, %s, %s, NOW())
    """
    cursor.execute(query, (username, hash_password(password), email))
    conn.commit()

    cursor.close()
    conn.close()
    return True


def login_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT UserID FROM users WHERE Username = %s AND password = %s"
    cursor.execute(query, (username, hash_password(password)))
    row = cursor.fetchone()

    cursor.close()
    conn.close()

    if row:
        return row[0]      # the UserID
    return None            # wrong username or password


def show_login_screen():
    st.title("Personal Finance Tracker")
    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")

        if st.button("Login"):
            user_id = login_user(username, password)
            if user_id:
                st.session_state['logged_in'] = True
                st.session_state['user_id'] = user_id
                st.rerun()
            else:
                st.error("Wrong username or password")

    with tab2:
        new_username = st.text_input("Choose a username", key="reg_username")
        new_email = st.text_input("Email", key="reg_email")
        new_password = st.text_input("Choose a password", type="password", key="reg_password")

        if st.button("Register"):
            if new_username == "" or new_password == "":
                st.error("Username and password are required")
            elif register_user(new_username, new_email, new_password):
                st.success("Account created! Now go to the Login tab.")
            else:
                st.error("That username is already taken")