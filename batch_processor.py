import pandas as pd
import requests
from datetime import datetime, timedelta
from tqdm import tqdm
import sys
import akshare as ak
from src.utils.model_base import HedgeFundRequest

# FastAPI endpoint URL
FASTAPI_URL = "http://localhost:8000/hedge-fund"

def process_ticker(ticker, start_date, end_date):
    """Process a single ticker through the FastAPI endpoint"""
    data = {
            "ticker": ticker,
            "start_date": start_date.strftime('%Y-%m-%d'),
            "end_date": end_date.strftime('%Y-%m-%d'),
            "initial_capital": 100000.0,
            "initial_position": 0,
            "show_reasoning": False,
            "num_of_news": 50
        }
    # data = HedgeFundRequest(
    #     ticker=ticker,
    #     start_date=start_date.strftime('%Y-%m-%d'),
    #     end_date=end_date.strftime('%Y-%m-%d'),
    #     initial_capital=100000.0,
    #     initial_position=0,
    #     show_reasoning=False,
    #     num_of_news=50
    # )
    
    try:
        response = requests.post(FASTAPI_URL, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error processing {ticker}: {str(e)}")
        return None

def process_batch(input_file, output_file):
    """Process a batch of tickers from input Excel and save results to output Excel"""
    # Read input Excel
    try:
        df = pd.read_excel(input_file, dtype={'ticker': str})  # 确保ticker列读取为字符串
        if 'ticker' not in df.columns:
            print("Error: Input Excel must have a 'ticker' column")
            return
        # 去除可能的空白字符并补全前导零
        df['ticker'] = df['ticker'].str.strip().str.zfill(6)
    except Exception as e:
        print(f"Error reading input file: {str(e)}")
        return

    # Prepare results storage
    results = []

    stock_info_a_code_name_df = ak.stock_info_a_code_name()

    # Set date range
    end_date = datetime.now() - timedelta(days=1)
    start_date = end_date - timedelta(days=365)

    # Process each ticker
    for ticker in tqdm(df['ticker'], desc="Processing tickers"):
        result = process_ticker(ticker, start_date, end_date)
        if result:
            try:
                ticker_name = stock_info_a_code_name_df.loc[stock_info_a_code_name_df['code'] == ticker, 'name'].iloc[0] 
            except IndexError:
                ticker_name = "Unknown"
        
            results.append({
                'ticker': ticker,
                'ticker_name': ticker_name,
                'result': result
            })

    # Save results to Excel
    if results:
        result_df = pd.DataFrame(results)
        try:
            result_df.to_excel(output_file, index=False)
            print(f"\nSuccessfully saved results to {output_file}")
        except Exception as e:
            print(f"Error saving results: {str(e)}")
    else:
        print("No results to save")

if __name__ == "__main__":
    input_file = "ticker_list.xlsx"
    output_file = "ticker_list_result.xlsx"
    process_batch(input_file, output_file)
