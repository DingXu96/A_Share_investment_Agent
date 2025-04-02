import streamlit as st
import requests
from datetime import datetime, timedelta

# FastAPI endpoint URL
FASTAPI_URL = "http://localhost:8000/hedge-fund"

def main():
    st.title("Hedge Fund Trading System")
    st.markdown("### Make trading decisions using AI agents")

    # Input fields
    ticker = st.text_input("Stock Ticker Symbol", placeholder="e.g. AAPL")
    
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", 
                                 value=datetime.now() - timedelta(days=365),
                                 max_value=datetime.now() - timedelta(days=1))
    with col2:
        end_date = st.date_input("End Date", 
                               value=datetime.now() - timedelta(days=1),
                               max_value=datetime.now() - timedelta(days=1))

    initial_capital = st.number_input("Initial Capital ($)", 
                                    value=100000.0, 
                                    min_value=0.0,
                                    step=1000.0)
    
    initial_position = st.number_input("Initial Position (shares)", 
                                     value=0,
                                     min_value=0)
    
    show_reasoning = st.checkbox("Show Agent Reasoning", value=False)
    num_of_news = st.slider("Number of News Articles to Analyze", 
                           min_value=1, 
                           max_value=100, 
                           value=5)

    if st.button("Run Analysis"):
        if not ticker:
            st.error("Please enter a stock ticker symbol")
            return

        # Prepare request data
        data = {
            "ticker": ticker,
            "start_date": start_date.strftime('%Y-%m-%d'),
            "end_date": end_date.strftime('%Y-%m-%d'),
            "initial_capital": float(initial_capital),
            "initial_position": int(initial_position),
            "show_reasoning": bool(show_reasoning),
            "num_of_news": int(num_of_news)
        }

        try:
            # Make POST request to FastAPI
            response = requests.post(FASTAPI_URL, json=data)
            response.raise_for_status()
            
            # Display results
            result = response.json()
            st.success("Analysis Complete!")
            
            # st.markdown("### Trading Decision")
            st.markdown("#### Analysis Results (JSON Format)")
            st.json(result)  # 使用st.json展示格式化数据
                
        except requests.exceptions.RequestException as e:
            st.error(f"Error making request: {str(e)}")

if __name__ == "__main__":
    main()
