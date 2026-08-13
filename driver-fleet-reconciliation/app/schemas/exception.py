from datetime import date

from pydantic import BaseModel, ConfigDict

from app.models.output.exception import ExceptionSeverity


class ExceptionResponse(BaseModel):
    id: int
    summary_id: int
    driver_id: str
    exception_date: date
    reason_code: str
    severity: ExceptionSeverity
    message: str

    model_config = ConfigDict(from_attributes=True)