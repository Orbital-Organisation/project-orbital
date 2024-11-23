import streamlit as st

def main():
    st.dataframe(st.session_state.df)
