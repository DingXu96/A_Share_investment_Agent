from fastapi import FastAPI, HTTPException
from datetime import datetime, timedelta
from src.utils.model_base import HedgeFundRequest
from main import run_hedge_fund

app = FastAPI()


@app.post("/hedge-fund")
async def hedge_fund(request: HedgeFundRequest):
    # Set end date to yesterday if not specified
    current_date = datetime.now()
    yesterday = current_date - timedelta(days=1)
    end_date = yesterday if not request.end_date else min(
        datetime.strptime(request.end_date, '%Y-%m-%d'), yesterday)

    # Set start date to one year before end date if not specified
    if not request.start_date:
        start_date = end_date - timedelta(days=365)
    else:
        start_date = datetime.strptime(request.start_date, '%Y-%m-%d')

    # Validate dates
    if start_date > end_date:
        raise HTTPException(status_code=400, detail="Start date cannot be after end date")

    # Validate num_of_news
    if request.num_of_news < 1:
        raise HTTPException(status_code=400, detail="Number of news articles must be at least 1")
    if request.num_of_news > 100:
        raise HTTPException(status_code=400, detail="Number of news articles cannot exceed 100")

    # Configure portfolio
    portfolio = {
        "cash": request.initial_capital,
        "stock": request.initial_position
    }

    # Run the hedge fund system
    result = run_hedge_fund(
        ticker=request.ticker,
        start_date=start_date.strftime('%Y-%m-%d'),
        end_date=end_date.strftime('%Y-%m-%d'),
        portfolio=portfolio,
        show_reasoning=request.show_reasoning,
        num_of_news=request.num_of_news
    )

    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
