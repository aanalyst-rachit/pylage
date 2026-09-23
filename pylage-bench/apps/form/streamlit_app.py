
import streamlit as st

if "rows" not in st.session_state:
    st.session_state.rows = []
if "status" not in st.session_state:
    st.session_state.status = "Ready"

st.title("Complex Form")
st.write(st.session_state.status)
name = st.text_input("Name")
email = st.text_input("Email")
if st.button("Submit"):
    if not name.strip() or not email.strip():
        st.session_state.status = "Please fill name and email"
    else:
        st.session_state.rows = [{"name": name.strip(), "email": email.strip()}] + st.session_state.rows
        st.session_state.status = "Saved"
    st.rerun()
st.write("Submitted:")
for r in st.session_state.rows:
    st.write(f'{r["name"]} | {r["email"]}')
