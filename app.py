


import streamlit as st
import sqlite3

conn = sqlite3.connect("users.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
    email TEXT PRIMARY KEY,
    password TEXT,
    counter INTEGER)
""")
conn.commit()

def get_user(email):
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    return cursor.fetchone()

def update_counter(email, increment=1):
    cursor.execute("UPDATE users SET counter = counter + ? WHERE email = ?", (increment, email))
    conn.commit()

st.title("User Counter App")

email = st.text_input("Email")
password = st.text_input("Password", type="password")

if st.button("Login"):
    user = get_user(email)
    if user and user[1] == password:
        st.session_state.logged_in = True
        st.session_state.email = email
        st.session_state.counter = user[2]
        st.success("Logged in successfully!")
    else:
        st.error("Invalid credentials")

if st.session_state.get("logged_in"):
    st.write(f"Hello, {st.session_state.email}")
    st.write(f"Your current count: {st.session_state.counter}")
    if st.button("Increment Counter"):
        st.session_state.counter += 1
        update_counter(st.session_state.email)
        st.success("Counter incremented!")
