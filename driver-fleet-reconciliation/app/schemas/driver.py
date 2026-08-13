from pydantic import BaseModel, ConfigDict


class DriverResponse(BaseModel):
    id: int
    driver_id: str
    name: str

    model_config = ConfigDict(from_attributes=True)