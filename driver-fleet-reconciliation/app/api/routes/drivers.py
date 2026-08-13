'''
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.models.ground_truth.driver import Driver


router = APIRouter(
    prefix="/drivers",
    tags=["Drivers"],
)


@router.get("/")
def get_drivers(
    db: Session = Depends(get_db),
):
    drivers = db.query(Driver).all()

    return drivers
    '''

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.models.ground_truth.driver import Driver
from app.schemas.driver import DriverResponse

router = APIRouter(
    prefix="/drivers",
    tags=["Drivers"],
)


@router.get(
    "/",
    response_model=list[DriverResponse],
)
def get_drivers(
    db: Session = Depends(get_db),
):
    return db.query(Driver).order_by(Driver.id).all()