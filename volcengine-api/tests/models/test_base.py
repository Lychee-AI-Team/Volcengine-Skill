from volcengine_api.toolkit.models.base import TaskStatus, TaskType, BaseModelConfig
from pydantic import BaseModel


def test_task_status_enum_values():
    assert TaskStatus.QUEUED.value == "QUEUED"
    assert TaskStatus("RUNNING").value == "RUNNING"
    assert len(list(TaskStatus)) == 5


def test_task_type_enum_values():
    assert TaskType.IMAGE_GENERATION.value == "IMAGE_GENERATION"
    assert TaskType("VISION_DETECTION").value == "VISION_DETECTION"
    assert len(list(TaskType)) == 8


def test_base_model_config_inherits_enum_values():
    class MyModel(BaseModelConfig):
        status: TaskStatus

    m = MyModel(status=TaskStatus.QUEUED)
    assert m.status == "QUEUED"
