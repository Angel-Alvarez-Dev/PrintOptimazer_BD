"""Punto de entrada principal de la aplicación."""

import uvicorn
from printoptimizer.core.config import get_settings


def main() -> None:
    """Iniciar el servidor de la aplicación."""
    settings = get_settings()
    
    uvicorn.run(
        "printoptimizer.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level="info" if settings.debug else "warning",
    )


if __name__ == "__main__":
    main()
