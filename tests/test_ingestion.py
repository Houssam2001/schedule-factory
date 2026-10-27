import pytest

from factory_scheduler.ingestion import load_tasks_csv


def _write(tmp_path, content):
    path = tmp_path / "tasks.csv"
    path.write_text(content, encoding="utf-8")
    return path


def test_missing_column_raises(tmp_path):
    path = _write(tmp_path, "id,machine,duration_minutes\nA,M1,10\n")
    with pytest.raises(ValueError, match="missing required columns"):
        load_tasks_csv(path)


def test_bad_int_reports_row(tmp_path):
    path = _write(tmp_path, "id,machine,duration_minutes,due_minute\nA,M1,abc,10\n")
    with pytest.raises(ValueError, match="row 2"):
        load_tasks_csv(path)


def test_duplicate_ids_raise(tmp_path):
    path = _write(
        tmp_path,
        "id,machine,duration_minutes,due_minute\nA,M1,10,20\nA,M2,5,30\n",
    )
    with pytest.raises(ValueError, match="Duplicate task IDs"):
        load_tasks_csv(path)


def test_blank_id_raises(tmp_path):
    path = _write(tmp_path, "id,machine,duration_minutes,due_minute\n ,M1,10,20\n")
    with pytest.raises(ValueError, match="row 2"):
        load_tasks_csv(path)


def test_negative_duration_raises(tmp_path):
    path = _write(tmp_path, "id,machine,duration_minutes,due_minute\nA,M1,-5,20\n")
    with pytest.raises(ValueError, match="row 2"):
        load_tasks_csv(path)
