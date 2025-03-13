import streamlit as st
from app import run_app

def main():
    """Runs the Streamlit Cryptocurrency Dashboard."""
    st.set_page_config(page_title="Crypto Dashboard", layout="wide")
    
    # Run the Streamlit app
    run_app()

if __name__ == "__main__":
    main()