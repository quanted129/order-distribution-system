from datetime import datetime

from sqlalchemy import (
    BigInteger,
    Boolean,
    DateTime,
    Double,
    ForeignKey,
    Integer,
    SmallInteger,
    String,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Shop(Base):
    __tablename__ = "shops"

    shop_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)
    telegram_chat_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    telegram_topic_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    latitude: Mapped[float] = mapped_column(Double)
    longitude: Mapped[float] = mapped_column(Double)
    address: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


class Driver(Base):
    __tablename__ = "drivers"

    driver_id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True)
    latitude: Mapped[float] = mapped_column(Double)
    longitude: Mapped[float] = mapped_column(Double)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


class Order(Base):
    __tablename__ = "orders"

    order_id: Mapped[int] = mapped_column(primary_key=True)
    shop_id: Mapped[int] = mapped_column(ForeignKey("shops.shop_id"))
    driver_id: Mapped[int | None] = mapped_column(
        ForeignKey("drivers.driver_id"), nullable=True
    )
    status: Mapped[int] = mapped_column(SmallInteger, default=0)
    type: Mapped[int] = mapped_column(SmallInteger, default=0)
    latitude: Mapped[float | None] = mapped_column(Double, nullable=True)
    longitude: Mapped[float | None] = mapped_column(Double, nullable=True)
    address: Mapped[str] = mapped_column(String)
    distance_km: Mapped[float | None] = mapped_column(Double, nullable=True)
    start_time: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    end_time: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    eta: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    route_sequence: Mapped[int | None] = mapped_column(SmallInteger, nullable=True)
    item_info: Mapped[str | None] = mapped_column(String, nullable=True)
    driver_info: Mapped[str | None] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
