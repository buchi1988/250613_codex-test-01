import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import json
from click.testing import CliRunner
from todo_cli import cli, read_tasks


def test_add_and_list(tmp_path):
    tasks_file = tmp_path / "tasks.json"
    env = {"TODO_FILE": str(tasks_file)}
    runner = CliRunner()
    result = runner.invoke(cli, ["add", "write tests"], env=env)
    assert result.exit_code == 0
    assert "Added task" in result.output

    result = runner.invoke(cli, ["list"], env=env)
    assert "[ ] write tests" in result.output

    data = json.loads(tasks_file.read_text())
    assert data["tasks"][0]["description"] == "write tests"
    assert not data["tasks"][0]["done"]


def test_done(tmp_path):
    tasks_file = tmp_path / "tasks.json"
    env = {"TODO_FILE": str(tasks_file)}
    runner = CliRunner()
    runner.invoke(cli, ["add", "task1"], env=env)
    result = runner.invoke(cli, ["done", "1"], env=env)
    assert result.exit_code == 0
    assert "Marked task 1 as done" in result.output

    tasks = read_tasks(str(tasks_file))
    assert tasks[0]["done"] is True
