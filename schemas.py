
from pydantic import BaseModel, Field


class ParsedOrder(BaseModel):
    shop_name: str | None = Field(default=None, description="Name of the shop.")
    time_interval: str | None = Field(
        default=None,
        description="The requested delivery time interval, e.g., '14:00-16:00'.",
    )
    address: str | None = Field(
        default=None, description="The full delivery address."
    )
    driver_details: str | None = Field(
        default=None, description="Any specific instructions for the driver."
    )
    order_contents: str | None = Field(
        default=None, description="What is being delivered."
    )
    payment_status: str | None = Field(
        default=None,
        description="Payment status, e.g., 'Оплачено', 'К оплате: нал 50р', etc.",
    )

    # We ask the AI to sanity check the data
    is_valid_order: bool = Field(
        description="True if this looks like a real order. False if it's just random chat."
    )

    # Coordinates to be filled later
    latitude: float | None = None
    longitude: float | None = None
