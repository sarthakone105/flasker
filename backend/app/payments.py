from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, db, auth
import uuid

router = APIRouter(prefix="/payments", tags=["Payments"])


# Dependency
def get_db():
    session = db.SessionLocal()
    try:
        yield session
    finally:
        session.close()


@router.post("/create", response_model=schemas.EscrowResponse)
def create_payment(
    escrow: schemas.EscrowCreate,
    session: Session = Depends(get_db),
    username: str = Depends(auth.get_current_user),
):
    request_obj = session.query(models.Request).filter(models.Request.id == escrow.request_id).first()
    if not request_obj:
        raise HTTPException(status_code=404, detail="Request not found")

    user = session.query(models.User).filter(models.User.username == username).first()
    if request_obj.requester_id != user.id:
        raise HTTPException(status_code=403, detail="Only requester can create payment")
    
    if request_obj.status != models.RequestStatus.accepted:
        raise HTTPException(status_code=403, detail="Payment can only be created after traveler accepts the request")

    fake_payment_id = f"pay_{uuid.uuid4().hex[:8]}"
    new_escrow = models.Escrow(
        request_id=escrow.request_id,
        amount_inr=escrow.amount_inr,
        provider_payment_id=fake_payment_id,
        status=models.EscrowStatus.paid  # simulate instant success
    )
    session.add(new_escrow)
    session.commit()
    session.refresh(new_escrow)
    return new_escrow


@router.put("/{escrow_id}/release", response_model=schemas.EscrowResponse)
def release_payment(
    escrow_id: int,
    session: Session = Depends(get_db),
    username: str = Depends(auth.get_current_user),
):
    escrow = session.query(models.Escrow).filter(models.Escrow.id == escrow_id).first()
    if not escrow:
        raise HTTPException(status_code=404, detail="Escrow not found")

    user = session.query(models.User).filter(models.User.username == username).first()
    if escrow.request.trip.user_id != user.id:
        raise HTTPException(status_code=403, detail="Only traveler can release funds")

    escrow.status = models.EscrowStatus.released
    session.commit()
    session.refresh(escrow)
    return escrow


@router.put("/{escrow_id}/refund", response_model=schemas.EscrowResponse)
def refund_payment(
    escrow_id: int,
    session: Session = Depends(get_db),
    username: str = Depends(auth.get_current_user),
):
    escrow = session.query(models.Escrow).filter(models.Escrow.id == escrow_id).first()
    if not escrow:
        raise HTTPException(status_code=404, detail="Escrow not found")

    user = session.query(models.User).filter(models.User.username == username).first()
    if escrow.request.requester_id != user.id:
        raise HTTPException(status_code=403, detail="Only requester can refund")

    escrow.status = models.EscrowStatus.refunded
    session.commit()
    session.refresh(escrow)
    return escrow
