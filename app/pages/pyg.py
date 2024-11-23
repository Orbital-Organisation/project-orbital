from pygwalker.api.streamlit import StreamlitRenderer
import streamlit as st
import pygwalker as pyg

df = st.session_state.df


def main():
    pyg_app = StreamlitRenderer(df)
    pyg_app.explorer()
