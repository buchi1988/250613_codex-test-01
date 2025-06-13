import json
import os
import click


def default_file():
    return os.environ.get('TODO_FILE', 'tasks.json')


def read_tasks(file_path=None):
    file_path = file_path or default_file()
    if not os.path.exists(file_path):
        return []
    with open(file_path, 'r') as f:
        try:
            data = json.load(f)
            return data.get('tasks', [])
        except json.JSONDecodeError:
            return []


def write_tasks(tasks, file_path=None):
    file_path = file_path or default_file()
    with open(file_path, 'w') as f:
        json.dump({'tasks': tasks}, f)


@click.group()
def cli():

    """シンプルなTODO CLI。"""

    """Simple TODO CLI."""

    pass


@cli.command()
@click.argument('description')
def add(description):

    """新しいタスクを追加します。"""

    """Add a new task."""

    tasks = read_tasks()
    next_id = max([t['id'] for t in tasks], default=0) + 1
    tasks.append({'id': next_id, 'description': description, 'done': False})
    write_tasks(tasks)
    click.echo(f"Added task {next_id}: {description}")


@cli.command(name='list')
def list_tasks():

    """すべてのタスクを表示します。"""

    """List all tasks."""

    tasks = read_tasks()
    for t in tasks:
        status = 'x' if t.get('done') else ' '
        click.echo(f"{t['id']}. [{status}] {t['description']}")


@cli.command()
@click.argument('task_id', type=int)
def done(task_id):

    """指定したタスクを完了済みにします。"""

    """Mark a task as done."""

    tasks = read_tasks()
    for t in tasks:
        if t['id'] == task_id:
            t['done'] = True
            write_tasks(tasks)
            click.echo(f"Marked task {task_id} as done")
            return
    click.echo(f"Task {task_id} not found", err=True)


if __name__ == '__main__':
    cli()
