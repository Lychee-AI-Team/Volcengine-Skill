import json
from datetime import datetime
import importlib.util
import pathlib

# Load modules directly from file paths to avoid Python package import issues
MODULE_ROOT = pathlib.Path(__file__).resolve().parents[3]  # repo root
BASE_PATH = MODULE_ROOT / 'volcengine-api' / 'toolkit' / 'models' / 'base.py'
TASK_PATH = MODULE_ROOT / 'volcengine-api' / 'toolkit' / 'models' / 'task.py'

def load_module_from_path(name, path):
    spec = importlib.util.spec_from_file_location(name, str(path))
    mod = importlib.util.module_from_spec(spec)  # type: ignore
    spec.loader.exec_module(mod)  # type: ignore
    return mod

base = load_module_from_path('volcengine_api_base', BASE_PATH)
task_model = load_module_from_path('volcengine_api_task', TASK_PATH)

TaskStatus = getattr(base, 'TaskStatus')
TaskType = getattr(base, 'TaskType')
TaskParams = getattr(task_model, 'TaskParams')
TaskResult = getattr(task_model, 'TaskResult')
TaskInfo = getattr(task_model, 'TaskInfo')


def test_task_params_can_be_instantiated():
    p = TaskParams()
    assert isinstance(p, TaskParams)


def test_task_result_serialization():
    r = TaskResult(url="https://example.com/file.txt", local_path="/tmp/file.txt", metadata={"k": "v"})
    s = r.json()
    assert '"url": "https://example.com/file.txt"' in s
    assert '"local_path": "/tmp/file.txt"' in s
    assert '"metadata": {"k": "v"}' in s or '"metadata": {"k":"v"}' in s


def test_task_info_serialization_and_fields():
    p = TaskParams()
    res = TaskResult(url="https://example.com/file.txt", local_path="/tmp/file.txt", metadata={})
    created = datetime(2025, 1, 1, 12, 0, 0)
    first_type = list(TaskType)[0]
    first_status = list(TaskStatus)[0]
    info = TaskInfo(
        id="task-123",
        type=first_type,
        status=first_status,
        params=p,
        result=res,
        error=None,
        created_at=created,
        started_at=None,
        finished_at=None,
    )
    js = info.json()
    assert '"id": "task-123"' in js
    assert '"created_at": "2025-01-01T12:00:00"' in js
