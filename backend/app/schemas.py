from pydantic import BaseModel
from datetime import datetime
from enum import Enum


# -------------------------
# User Schemas
# -------------------------
class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    model_config = {
        "from_attributes": True
    }


class UserLogin(BaseModel):
    username: str  # or email if you prefer
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# -------------------------
# Trip Schemas
# -------------------------
class TripBase(BaseModel):
    origin: str
    destination: str
    travel_date: datetime


class TripCreate(TripBase):
    pass


class TripResponse(TripBase):
    id: int
    user_id: int

    model_config = {
        "from_attributes": True
    }


# -------------------------
# Request Schemas
# -------------------------
class RequestStatus(str, Enum):
    pending = "pending"
    accepted = "accepted"
    rejected = "rejected"


class RequestBase(BaseModel):
    product_name: str
    product_description: str | None = None


class RequestCreate(RequestBase):
    trip_id: int


class RequestResponse(RequestBase):
    id: int
    trip_id: int
    requester_id: int
    status: RequestStatus

    model_config = {
        "from_attributes": True
    }
