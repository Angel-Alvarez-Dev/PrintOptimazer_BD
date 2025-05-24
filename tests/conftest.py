"""Configuración global de pytest."""

import sys
from pathlib import Path

import pytest

# Agregar src al path para imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


@pytest.fixture
def app_settings():
    """Fixture para configuración de pruebas."""
    from printoptimizer.core.config import Settings
    
    return Settings(
        app_env="testing",
        debug=True,
        database_url="postgresql://test:test@localhost/test_db"
    )
