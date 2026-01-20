import typer
from rich.console import Console
from rich.table import Table

from global_task_hub.infrastructure.database import (
    SQLAlchemyTaskRepository,
    SessionLocal,
)
from global_task_hub.application.use_cases import (
    CreateTaskUseCase,
    CompleteTaskUseCase,
    GetTasksUseCase,
)

app = typer.Typer()
console = Console()


def get_repository():
    db = SessionLocal()
    return SQLAlchemyTaskRepository(db)


@app.command()
def create(title: str, description: str = ""):
    """Create a new task."""
    repo = get_repository()
    use_case = CreateTaskUseCase(repo)
    task = use_case.execute(title, description)
    console.print(f"[green]Task created successfully![/green] ID: {task.id}")


@app.command()
def list_tasks():
    """List all tasks."""
    repo = get_repository()
    use_case = GetTasksUseCase(repo)
    tasks = use_case.execute()

    table = Table(title="Global Task Hub")
    table.add_column("ID", style="cyan")
    table.add_column("Title", style="magenta")
    table.add_column("Status", style="green")

    for task in tasks:
        table.add_row(str(task.id), task.title, task.status.value)

    console.print(table)


@app.command()
def complete(task_id: str):
    """Mark a task as complete."""
    repo = get_repository()
    # Simple event publisher (print to console)
    task_id_uuid = None
    try:
        from uuid import UUID

        task_id_uuid = UUID(task_id)
    except ValueError:
        console.print("[red]Invalid UUID format.[/red]")
        return

    class ConsoleEventPublisher:
        def publish_completed(self, task):
            console.print(
                f"[bold blue]EVENT:[/bold blue] Task '{task.title}' was completed!"
            )

    use_case = CompleteTaskUseCase(repo, event_publisher=ConsoleEventPublisher())
    try:
        use_case.execute(task_id_uuid)
        console.print(f"[green]Task {task_id} completed![/green]")
    except ValueError as e:
        console.print(f"[red]{e}[/red]")


if __name__ == "__main__":
    app()
