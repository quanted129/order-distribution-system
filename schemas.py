from pydantic import BaseModel, Field
from typing import Optional


class ParsedOrder(BaseModel):
    shop_name: Optional[str] = Field(default=None, description="Name of the shop.")
    time_interval: Optional[str] = Field(default=None, description="The requested delivery time interval, e.g., '14:00-16:00'.")
    address: Optional[str] = Field(default=None, description="The full delivery address.")
    driver_details: Optional[str] = Field(default=None, description="Any specific instructions for the driver.")
    order_contents: Optional[str] = Field(default=None, description="What is being delivered.")
    payment_status: Optional[str] = Field(default=None, description="Payment status, e.g., 'Оплачено', 'К оплате: нал 50р', etc.")

    # We ask the AI to sanity check the data
    is_valid_order: bool = Field(description="True if this looks like a real order. False if it's just random chat.")

    # Coordinates to be filled later
    latitude: Optional[float] = None
    longitude: Optional[float] = None