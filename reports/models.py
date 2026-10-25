from dataclasses import dataclass
from math import fsum
from typing import Annotated

from pydantic import BaseModel, Field

Number = Annotated[float, Field(ge=-1e12, le=1e12, allow_inf_nan=False)]


class ReportInput(BaseModel):
    values: list[Number] = Field(min_length=1, max_length=1000)
    delay_seconds: int = Field(default=10, ge=0, le=300)


@dataclass
class ReportJob:
    report_id: str
    values: list[float]
    delay_seconds: int


def summarize(values: list[float]) -> dict:
    total = fsum(values)
    return {
        "count": len(values),
        "sum": total,
        "min": min(values),
        "max": max(values),
        "mean": total / len(values),
    }
