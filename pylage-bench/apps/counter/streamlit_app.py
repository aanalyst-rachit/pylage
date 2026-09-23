import streamlit as st

if "count" not in st.session_state:
    st.session_state.count = 0

st.title("Counter")
st.write(st.session_state.count)

if st.button("Increment"):
    st.session_state.count += 1
    st.rerun()
