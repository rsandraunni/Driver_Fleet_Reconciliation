from datetime import date

from pydantic import BaseModel, ConfigDict

from app.models.output.daily_summary import SummaryStatus


class DailySummaryResponse(BaseModel):
    id: int
    driver_id: int
    summary_date: date
    hours_on_duty: float | None
    trips_completed: int | None
    distance_km: float | None
    status: SummaryStatus

    model_config = ConfigDict(from_attributes=True)