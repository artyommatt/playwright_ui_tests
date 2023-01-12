import os
import subprocess


def run_lints() -> None:
    subprocess.run(
        'flake8 .',
        cwd=os.getcwd()
    )
    subprocess.run(
        'mypy .',
        cwd=os.getcwd()
    )


run_lints()
