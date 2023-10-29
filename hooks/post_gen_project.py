"""Script run after project generation."""


import os
import shutil

from pathlib import Path

# Current path
path = Path(os.getcwd())

# Source path
parent_path = path.parent.absolute()
package_path = parent_path.joinpath("{{cookiecutter.package_name}}")


def remove(filepath: Path) -> None:
    if filepath.is_file():
        os.remove(filepath)
    elif filepath.is_dir():
        shutil.rmtree(filepath)


features = {
    "docs": "{{cookiecutter.include_docs}}" == "True",
    "tests": "{{cookiecutter.include_tests}}" == "True",
    "github_actions": "{{cookiecutter.include_github_actions}}" == "True"
    and "{{cookiecutter.is_project_only_local}}" != "True",
    "notebooks": "{{cookiecutter.include_notebooks}}" == "True",
}

if not features["docs"]:
    remove(package_path.joinpath("docs"))
    remove(package_path.joinpath("mkdocs.yaml"))
    remove(package_path.joinpath(".github/workflows/documentation.yml"))
if not features["tests"]:
    remove(package_path.joinpath("tests"))
    remove(package_path.joinpath(".github/workflows/tests.yml"))
if not features["github_actions"]:
    remove(package_path.joinpath(".github"))
if not features["notebooks"]:
    remove(package_path.joinpath("notebooks"))
