from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas, db, security, auth
from typing import List

# Create DB tables
models.Base.metadata.create_all(bind=db.engine)

app = FastAPI()

# Dependency to get DB session
def get_db():
    session = db.SessionLocal()
    try:
        yield session
    finally:
        session.close()

# -----------------------------
# Health check
# -----------------------------
@app.get("/ping")
def ping():
    return {"status": "ok"}


# -----------------------------
# Auth
# -----------------------------
@app.post("/signup", response_model=schemas.UserResponse)
def signup(user: schemas.UserCreate, session: Session = Depends(get_db)):
    db_user = session.query(models.User).filter(
        (models.User.username == user.username) | (models.User.email == user.email)
    ).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username or email already exists")
    hashed_pw = security.hash_password(user.password)
    new_user = models.User(username=user.username, email=user.email, hashed_password=hashed_pw)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user


@app.post("/login", response_model=schemas.Token)
def login(user: schemas.UserLogin, session: Session = Depends(get_db)):
    db_user = session.query(models.User).filter(models.User.username == user.username).first()
    if not db_user or not security.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = auth.create_access_token({"sub": db_user.username})
    return {"access_token": token}


# -----------------------------
# Trips
# -----------------------------
@app.post("/trips", response_model=schemas.TripResponse)
def create_trip(
    trip: schemas.TripCreate,
    session: Session = Depends(get_db),
    username: str = Depends(auth.get_current_user),
):
    user = session.query(models.User).filter(models.User.username == username).first()
    new_trip = models.Trip(
        origin=trip.origin,
        destination=trip.destination,
        travel_date=trip.travel_date,
        user_id=user.id
    )
    session.add(new_trip)
    session.commit()
    session.refresh(new_trip)
    return new_trip


@app.get("/trips", response_model=List[schemas.TripResponse])
def list_trips(session: Session = Depends(get_db)):
    return session.query(models.Trip).all()


@app.get("/trips/{trip_id}", response_model=schemas.TripResponse)
def get_trip(trip_id: int, session: Session = Depends(get_db)):
    trip = session.query(models.Trip).filter(models.Trip.id == trip_id).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    return trip


# -----------------------------
# Requests
# -----------------------------
@app.post("/requests", response_model=schemas.RequestResponse)
def create_request(
    request: schemas.RequestCreate,
    session: Session = Depends(get_db),
    username: str = Depends(auth.get_current_user),
):
    user = session.query(models.User).filter(models.User.username == username).first()
    trip = session.query(models.Trip).filter(models.Trip.id == request.trip_id).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")

    new_request = models.Request(
        product_name=request.product_name,
        product_description=request.product_description,
        status="pending",
        trip_id=request.trip_id,
        requester_id=user.id
    )
    session.add(new_request)
    session.commit()
    session.refresh(new_request)
    return new_request


@app.get("/requests/{trip_id}", response_model=List[schemas.RequestResponse])
def list_requests(trip_id: int, session: Session = Depends(get_db)):
    return session.query(models.Request).filter(models.Request.trip_id == trip_id).all()


@app.put("/requests/{request_id}/accept", response_model=schemas.RequestResponse)
def accept_request(request_id: int, session: Session = Depends(get_db)):
    req = session.query(models.Request).filter(models.Request.id == request_id).first()
    if not req:
        raise HTTPException(status_code=404, detail="Request not found")
    req.status = "accepted"
    session.commit()
    session.refresh(req)
    return req


@app.put("/requests/{request_id}/reject", response_model=schemas.RequestResponse)
def reject_request(request_id: int, session: Session = Depends(get_db)):
    req = session.query(models.Request).filter(models.Request.id == request_id).first()
    if not req:
        raise HTTPException(status_code=404, detail="Request not found")
    req.status = "rejected"
    session.commit()
    session.refresh(req)
    return req
