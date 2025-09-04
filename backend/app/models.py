from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DateTime, Text, func, Float
from sqlalchemy.orm import relationship
from app.db import Base
import enum
from datetime import datetime


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    # Relationships
    trips = relationship("Trip", back_populates="traveler")
    requests = relationship("Request", back_populates="requester")
    sent_messages = relationship("Message", foreign_keys="Message.sender_id", back_populates="sender")
    received_messages = relationship("Message", foreign_keys="Message.receiver_id", back_populates="receiver")


class Trip(Base):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    origin = Column(String, nullable=False)
    destination = Column(String, nullable=False)
    travel_date = Column(DateTime, nullable=False)

    # Relationships
    traveler = relationship("User", back_populates="trips")
    requests = relationship("Request", back_populates="trip")


class RequestStatus(str, enum.Enum):
    pending = "pending"
    accepted = "accepted"
    rejected = "rejected"


class Request(Base):
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, ForeignKey("trips.id"), nullable=False)
    requester_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_name = Column(String, nullable=False)
    product_description = Column(String, nullable=True)
    status = Column(Enum(RequestStatus), default=RequestStatus.pending)

    # Relationships
    trip = relationship("Trip", back_populates="requests")
    requester = relationship("User", back_populates="requests")
    messages = relationship("Message", back_populates="request", cascade="all, delete")
    escrow = relationship("Escrow", back_populates="request", uselist=False)



class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(Integer, ForeignKey("requests.id", ondelete="CASCADE"), nullable=False)
    sender_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    receiver_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    sender = relationship("User", foreign_keys=[sender_id], back_populates="sent_messages")
    receiver = relationship("User", foreign_keys=[receiver_id], back_populates="received_messages")
    request = relationship("Request", back_populates="messages")



class EscrowStatus(str, enum.Enum):
    pending = "pending"
    paid = "paid"
    released = "released"
    refunded = "refunded"


class Escrow(Base):
    __tablename__ = "escrows"

    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(Integer, ForeignKey("requests.id", ondelete="CASCADE"), nullable=False)
    amount_inr = Column(Float, nullable=False)
    provider_payment_id = Column(String, nullable=False)  # e.g., Razorpay/Stripe payment_id
    status = Column(Enum(EscrowStatus), default=EscrowStatus.pending)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship
    request = relationship("Request", back_populates="escrow")