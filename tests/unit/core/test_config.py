"""Tests para la configuración."""

import pytest
from printoptimizer.core.config import Settings, get_settings


def test_settings_default_values():
    """Test que los valores por defecto se cargan correctamente."""
    settings = Settings()
    
    assert settings.app_name == "PrintOptimizer BD"
    assert settings.app_env == "development"
    assert settings.debug is True
    assert settings.api_v1_prefix == "/api/v1"


def test_get_settings_returns_cached_instance():
    """Test que get_settings retorna la misma instancia (cached)."""
    settings1 = get_settings()
    settings2 = get_settings()
    
    assert settings1 is settings2
