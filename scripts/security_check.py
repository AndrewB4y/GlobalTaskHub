import os
import subprocess
import sys


def run_security_scan():
    print("Running Bandit Security Scan...")
    # Excluding tests and docs as configured in pyproject.toml
    # bandit -r global_task_hub -c pyproject.toml
    result = subprocess.run(
        ["bandit", "-r", "global_task_hub", "-c", "pyproject.toml"],
        capture_output=True,
        text=True,
    )

    print(result.stdout)
    if result.returncode != 0:
        print("Security vulnerabilities found!")
        print(result.stderr)
        sys.exit(result.returncode)
    else:
        print("No high-severity vulnerabilities found.")


if __name__ == "__main__":
    run_security_scan()
