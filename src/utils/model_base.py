from pydantic import BaseModel
from typing import Optional

class HedgeFundRequest(BaseModel):
    ticker: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    initial_capital: float = 100000.0
    initial_position: int = 0
    show_reasoning: bool = False
    num_of_news: int = 5