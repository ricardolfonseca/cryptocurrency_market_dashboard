import streamlit as st
from app import run_app

# ✅ Set page layout to wide
st.set_page_config(page_title="Crypto Dashboard", layout="wide")

if __name__ == "__main__":
    run_app()