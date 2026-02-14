import streamlit as st
from app import run_app

if __name__ == "__main__":
    try:
        run_app()
    except Exception as e:
        st.error(f"❌ An error occurred: {str(e)}")
        st.stop()