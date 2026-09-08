"""Loads the client without importing the integration package.

The package's __init__ pulls in Home Assistant, which the test job does not
install: the client itself only needs aiohttp, and that is what is tested here.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
from types import ModuleType

import pytest

ROOT = Path(__file__).resolve().parent.parent
API_PATH = ROOT / "custom_components" / "mail_archiver" / "api.py"


def _load_api() -> ModuleType:
    """Load api.py with a stand-in package, so its relative import works."""
    package = ModuleType("mail_archiver_pkg")
    package.__path__ = [str(API_PATH.parent)]
    sys.modules["mail_archiver_pkg"] = package

    for name in ("const", "api"):
        spec = importlib.util.spec_from_file_location(
            f"mail_archiver_pkg.{name}", API_PATH.parent / f"{name}.py"
        )
        assert spec and spec.loader
        module = importlib.util.module_from_spec(spec)
        sys.modules[f"mail_archiver_pkg.{name}"] = module
        spec.loader.exec_module(module)
    return sys.modules["mail_archiver_pkg.api"]


@pytest.fixture(scope="session")
def api() -> ModuleType:
    """Return the api module of the integration."""
    return _load_api()
