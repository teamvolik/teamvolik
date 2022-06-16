#!/usr/bin/python3
"""Doit main file."""
# nosec
import shutil
import subprocess  # nosec
import sys


def task_tests():
    """Run tests."""
    return {
        "targets": [".build/pytest.results"],
        "task_dep": ["mkdir"],
        "actions": [f"{sys.executable} -m pytest . > .build/pytest.results"],
        "clean": True,
    }


def task_sphinx():
    """Generate html from sphinx."""
    return {"targets": ["src/build/**"], "actions": ["cd src/ && make html"]}


def task_cleanall():
    """Clean .build."""
    return {"actions": [(shutil.rmtree, [".build", True]), (shutil.rmtree, ["build", True]), (shutil.rmtree, ["dist", True])]}


def task_mkdir():
    """Create .build directory."""
    return {
        "actions": ["mkdir -p .build"],
        "targets": [".build"],
    }


def task_localization():
    """Make babel localization."""
    return {
        "actions": ["pybabel compile -l ru -D bot -d src/teamvolik/localization"],
        "targets": ["src/localization/ru/LC_MESSAGES/bot.mo"],
        "clean": True,
    }


def task_pydocstyle():
    """Run pydocstyle documentation linter."""
    return {
        "targets": [".build/pydocstyle.results"],
        "task_dep": ["mkdir"],
        "actions": [f"{sys.executable} -m pydocstyle . > .build/pydocstyle.results"],
        "clean": True,
    }


def task_flake8():
    """Run flake8 linter."""
    return {
        "targets": [".build/flake8.results"],
        "task_dep": ["mkdir"],
        "actions": [f"{sys.executable} -m flake8 . > .build/flake8.results"],
        "clean": True,
    }


def task_black():
    """Run black linter."""
    return {
        "targets": [".build/black.results"],
        "task_dep": ["mkdir"],
        "actions": [f"{sys.executable} -m black . 2> .build/black.results"],
        "clean": True,
    }


def task_bandit():
    """Run bandit."""
    return {
        "targets": [".build/bandit.results"],
        "task_dep": ["mkdir"],
        "actions": [f"{sys.executable} -m bandit -r . > .build/bandit.results"],
        "clean": True,
    }


def task_all():
    """Run all tasks."""
    return {
        "actions": [],
        "task_dep": ["bandit", "black", "flake8", "pydocstyle", "tests", "localization", "wheel"],
        "clean": True,
    }


def task_installdeps():
    """Install all development dependencies."""

    def install_dependencies(python_version):
        subprocess.check_call([python_version, "-m", "pip", "install", "-r", "devrequirements.txt"])  # nosec

    return {
        "actions": [(install_dependencies,)],
        "params": [
            {
                "name": "python_version",
                "short": "p",
                "type": str,
                "default": "python3.10",
            }
        ],
    }


def task_wheel():
    """Build wheel from sources."""
    return {
        "actions": [f"{sys.executable} setup.py bdist_wheel"],
    }
