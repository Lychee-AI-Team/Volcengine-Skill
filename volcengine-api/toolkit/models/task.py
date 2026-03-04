from __future__ import annotations

from typing import Optional, Dict, Any
from datetime import datetime

from pydantic import BaseModel
from .base import TaskStatus, TaskType, BaseModelConfig


class TaskParams(BaseModel):
    """Base class for task parameters."""
    pass


class TaskResult(BaseModel):
    url: Optional[str] = None
    local_path: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

    class Config(BaseModelConfig):
        arbitrary_types_allowed = True


class TaskInfo(BaseModel):
    id: str
    type: TaskType
    status: TaskStatus
    params: TaskParams
    result: Optional[TaskResult] = None
    error: Optional[str] = None
    created_at: datetime
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None

    class Config(BaseModelConfig):
        json_encoders = {
            datetime: lambda v: v.isoformat(),
        }
