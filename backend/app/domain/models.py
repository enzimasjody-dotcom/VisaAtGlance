from pydantic import BaseModel, Field


class HealthStatus(BaseModel):
    status: str = Field(description="Service status")
    service: str = Field(description="Service name")
