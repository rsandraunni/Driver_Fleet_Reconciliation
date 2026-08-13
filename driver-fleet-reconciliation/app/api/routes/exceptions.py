from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.models.output.exception import ReconciliationException
from app.schemas.exception import ExceptionResponse

router = APIRouter(
    prefix="/exceptions",
    tags=["Exceptions"],
)


@router.get(
    "/",
    response_model=list[ExceptionResponse],
)
def get_exceptions(
    db: Session = Depends(get_db),
):
    return (
        db.query(ReconciliationException)
        .order_by(
            ReconciliationException.exception_date.desc(),
            ReconciliationException.id.desc(),
        )
        .all()
    )


@router.get(
    "/driver/{driver_id}",
    response_model=list[ExceptionResponse],
)
def get_driver_exceptions(
    driver_id: int,
    db: Session = Depends(get_db),
):
    return (
        db.query(ReconciliationException)
        .filter(
            ReconciliationException.driver_id == str(driver_id)
        )
        .order_by(ReconciliationException.id.desc())
        .all()
    )