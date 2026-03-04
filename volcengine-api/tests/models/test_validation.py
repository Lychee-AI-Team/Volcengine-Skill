import importlib.util
from pathlib import Path
import json


def _load_validation_result_class():
    test_path = Path(__file__).resolve()
    root = test_path
    while root.name != "volcengine-api" and root.parent != root:
        root = root.parent
    module_path = root / "toolkit" / "models" / "validation.py"

    spec = importlib.util.spec_from_file_location("volcengine_validation", str(module_path))
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore
    return module.ValidationResult


ValidationResult = _load_validation_result_class()


def test_creation_defaults():
    vr = ValidationResult()
    assert vr.is_valid is True
    assert vr.errors == []
    assert vr.warnings == []
    assert vr.details is None


def test_add_error_marks_invalid():
    vr = ValidationResult()
    vr.add_error("boom")
    assert vr.is_valid is False
    assert vr.errors == ["boom"]


def test_add_warning_does_not_mark_invalid():
    vr = ValidationResult()
    vr.add_warning("note")
    assert vr.warnings == ["note"]
    assert vr.is_valid is True


def test_serialization():
    vr = ValidationResult()
    vr.add_error("err")
    vr.add_warning("warn")
    vr.details = {"code": 123}
    d = vr.dict()
    assert d["is_valid"] is False
    assert d["errors"] == ["err"]
    assert d["warnings"] == ["warn"]
    assert d["details"] == {"code": 123}
    j = vr.json()
    parsed = json.loads(j)
    assert parsed["is_valid"] is False
