# GlobalTaskHub

A robust, scalable Python backend project implementing Clean Architecture (Hexagonal) principles.

## Features

- **Clean Architecture**: Clear separation of concerns (Domain, Application, Infrastructure, Presentation).
- **Web API**: Built with FastAPI, featuring i18n, session management, and event handling.
- **CLI**: Interactive command-line interface using Typer.
- **Database**: SQLAlchemy ORM with support for SQLite and PostgreSQL.
- **Dependency Management**: Managed via Poetry.
- **Quality Assurance**: Integrated testing with Pytest and security scanning with Bandit.
- **Documentation**: Auto-generated API docs using Sphinx and ReadTheDocs theme.

## Architecture Layers

- **Domain**: Pure business entities and interfaces. No external dependencies.
- **Application**: Business use cases and application logic.
- **Infrastructure**: Adapters for databases, external APIs, and network services.
- **Presentation**: Entry points (API & CLI).

## Installation

1. Ensure you have Python 3.10+ and [Poetry](https://python-poetry.org/) installed.
2. Clone the repository:
   ```bash
   git clone <repository-url>
   cd GlobalTaskHub
   ```
3. Install dependencies:
   ```bash
   poetry install
   ```

## Usage

### Web API

Start the FastAPI server:
```bash
poetry run uvicorn global_task_hub.presentation.api:app --reload
```
Access the interactive documentation at `http://localhost:8000/docs`.

### CLI

Use the Command Line Interface to manage tasks. First, initialize the database:
```bash
poetry run global-task-hub init-db
```

Then you can verify by creating and listing tasks:
```bash
# Create a task
poetry run global-task-hub create "My Task" --description "Details here"

# List tasks
poetry run global-task-hub list-tasks

# Complete a task
poetry run global-task-hub complete <TASK_UUID>
```

## Testing & Verification

Run the integration suite:
```bash
poetry run pytest tests/integration
```

Run security check:
```bash
poetry run python scripts/security_check.py
```

## Documentation

Build the project documentation locally:
```bash
poetry run sphinx-build -b html docs docs/_build/html
```
Open `docs/_build/html/index.html` in your browser.