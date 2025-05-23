# PrintOptimizer_BD

<div align="center">

![Python](https://img.shields.io/badge/python-v3.11+-blue.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-blue.svg)
![Docker](https://img.shields.io/badge/Docker-24.0+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![CI](https://github.com/tu-usuario/PrintOptimizer_BD/workflows/CI/badge.svg)

Sistema de optimización y gestión de trabajos de impresión con base de datos PostgreSQL.

[Instalación](#-instalación) •
[Documentación](#-documentación) •
[Contribuir](#-contribuir) •
[Licencia](#-licencia)

</div>

## 📋 Tabla de Contenidos

- [Sobre el Proyecto](#-sobre-el-proyecto)
- [Tecnologías](#-tecnologías)
- [Arquitectura](#-arquitectura)
- [Requisitos Previos](#-requisitos-previos)
- [Instalación](#-instalación)
- [Configuración](#-configuración)
- [Uso](#-uso)
- [Testing](#-testing)
- [API](#-api)
- [Base de Datos](#-base-de-datos)
- [Docker](#-docker)
- [Desarrollo](#-desarrollo)
- [Contribuir](#-contribuir)
- [Roadmap](#-roadmap)
- [Licencia](#-licencia)
- [Autores](#-autores)

## 🎯 Sobre el Proyecto

**PrintOptimizer_BD** es un sistema diseñado para optimizar y gestionar trabajos de impresión en entornos empresariales. Permite:

- 📊 Gestión centralizada de impresoras y trabajos de impresión
- 🚀 Optimización automática de colas de impresión
- 📈 Análisis y reportes de uso
- 💰 Control de costos de impresión
- 🔐 Gestión de usuarios y permisos
- 📱 API RESTful para integración con otros sistemas

### Características Principales

- **Gestión de Impresoras**: Registro y monitoreo de múltiples impresoras
- **Cola Inteligente**: Algoritmos de optimización para distribución de trabajos
- **Reportes Detallados**: Estadísticas de uso, costos y eficiencia
- **Multi-tenant**: Soporte para múltiples organizaciones
- **API REST**: Integración fácil con sistemas existentes
- **Tiempo Real**: Actualizaciones en tiempo real del estado de impresión

## 🚀 Tecnologías

### Backend
- **[Python 3.11+](https://www.python.org/)** - Lenguaje de programación principal
- **[FastAPI](https://fastapi.tiangolo.com/)** - Framework web moderno y rápido
- **[SQLAlchemy 2.0](https://www.sqlalchemy.org/)** - ORM potente y flexible
- **[PostgreSQL 15+](https://www.postgresql.org/)** - Base de datos relacional
- **[Alembic](https://alembic.sqlalchemy.org/)** - Migraciones de base de datos
- **[Pydantic](https://pydantic-docs.helpmanual.io/)** - Validación de datos

### DevOps
- **[Docker](https://www.docker.com/)** - Containerización
- **[Docker Compose](https://docs.docker.com/compose/)** - Orquestación local
- **[GitHub Actions](https://github.com/features/actions)** - CI/CD
- **[pytest](https://pytest.org/)** - Framework de testing

### Herramientas de Desarrollo
- **[Black](https://black.readthedocs.io/)** - Formateador de código
- **[Flake8](https://flake8.pycqa.org/)** - Linter
- **[mypy](http://mypy-lang.org/)** - Type checking
- **[pre-commit](https://pre-commit.com/)** - Git hooks

## 🏗️ Arquitectura

```
PrintOptimizer_BD/
├── .github/                 # Configuración de GitHub
│   ├── workflows/          # GitHub Actions
│   └── ISSUE_TEMPLATE/     # Templates para issues
├── docker/                 # Archivos Docker
│   ├── Dockerfile         
│   └── docker-compose.yml 
├── src/                    # Código fuente
│   └── printoptimizer/     # Paquete principal
│       ├── api/           # Endpoints de la API
│       │   └── v1/        # Versión 1 de la API
│       ├── core/          # Configuración central
│       ├── db/            # Base de datos
│       │   └── migrations/# Migraciones Alembic
│       ├── models/        # Modelos SQLAlchemy
│       ├── schemas/       # Schemas Pydantic
│       ├── services/      # Lógica de negocio
│       └── utils/         # Utilidades
├── tests/                  # Tests
│   ├── unit/              # Tests unitarios
│   ├── integration/       # Tests de integración
│   └── e2e/               # Tests end-to-end
├── scripts/                # Scripts útiles
├── docs/                   # Documentación
│   ├── api/               # Documentación API
│   ├── architecture/      # Diagramas de arquitectura
│   └── deployment/        # Guías de despliegue
├── .env.example           # Variables de entorno ejemplo
├── alembic.ini            # Configuración de Alembic
├── requirements.txt       # Dependencias Python
├── requirements-dev.txt   # Dependencias de desarrollo
└── Makefile              # Comandos útiles
```

## 📋 Requisitos Previos

Antes de comenzar, asegúrate de tener instalado:

- **Python 3.11** o superior
- **PostgreSQL 15** o superior
- **Docker** 24.0+ y **Docker Compose** 2.20+
- **Git** 2.40+

### Verificar instalaciones:
```bash
python --version      # Python 3.11.x
psql --version       # psql (PostgreSQL) 15.x
docker --version     # Docker version 24.x.x
docker-compose --version  # Docker Compose version v2.20.x
```

## 🔧 Instalación

### Opción 1: Instalación con Docker (Recomendado)

1. **Clonar el repositorio**
```bash
git clone https://github.com/tu-usuario/PrintOptimizer_BD.git
cd PrintOptimizer_BD
```

2. **Configurar variables de entorno**
```bash
cp .env.example .env
# Editar .env con tus configuraciones
```

3. **Construir y levantar servicios**
```bash
docker-compose -f docker/docker-compose.yml up -d --build
```

4. **Ejecutar migraciones**
```bash
docker-compose exec app alembic upgrade head
```

5. **Verificar instalación**
```bash
# Ver logs
docker-compose logs -f app

# La API estará disponible en http://localhost:8000
# Documentación en http://localhost:8000/docs
```

### Opción 2: Instalación Local

1. **Clonar el repositorio**
```bash
git clone https://github.com/tu-usuario/PrintOptimizer_BD.git
cd PrintOptimizer_BD
```

2. **Crear y activar entorno virtual**
```bash
# Linux/Mac
python -m venv .venv
source .venv/bin/activate

# Windows
python -m venv .venv
.venv\Scripts\activate
```

3. **Instalar dependencias**
```bash
pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Para desarrollo
```

4. **Configurar PostgreSQL**
```bash
# Crear base de datos
createdb printoptimizer_db

# O usando psql
psql -U postgres -c "CREATE DATABASE printoptimizer_db;"
```

5. **Configurar variables de entorno**
```bash
cp .env.example .env
# Editar .env con tus configuraciones
```

6. **Ejecutar migraciones**
```bash
alembic upgrade head
```

7. **Iniciar la aplicación**
```bash
# Desarrollo (con recarga automática)
uvicorn src.printoptimizer.main:app --reload --host 0.0.0.0 --port 8000

# Producción
python src/main.py
```

## ⚙️ Configuración

### Variables de Entorno

Crea un archivo `.env` basado en `.env.example`:

```env
# Application
APP_NAME=PrintOptimizer_BD
APP_ENV=development
DEBUG=True
SECRET_KEY=tu-clave-secreta-aqui

# Database
DATABASE_URL=postgresql://usuario:password@localhost:5432/printoptimizer_db
DB_ECHO=False  # True para ver queries SQL en desarrollo

# API Configuration
API_V1_PREFIX=/api/v1
PROJECT_NAME=PrintOptimizer BD
VERSION=0.1.0
BACKEND_CORS_ORIGINS=["http://localhost:3000", "http://localhost:8000"]

# Security
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALGORITHM=HS256

# Pagination
DEFAULT_PAGE_SIZE=20
MAX_PAGE_SIZE=100

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
```

### Configuración de Base de Datos

Para configurar la base de datos en producción:

```sql
-- Crear usuario
CREATE USER printopt_user WITH PASSWORD 'password_seguro';

-- Crear base de datos
CREATE DATABASE printoptimizer_db OWNER printopt_user;

-- Otorgar permisos
GRANT ALL PRIVILEGES ON DATABASE printoptimizer_db TO printopt_user;
```

## 🎮 Uso

### Iniciar el servidor

```bash
# Con Make
make run

# Con Docker
make docker-up

# Manualmente
uvicorn src.printoptimizer.main:app --reload
```

### Endpoints principales

- **API Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health
- **API v1**: http://localhost:8000/api/v1/

### Ejemplos de uso

```python
import requests

# Obtener todas las impresoras
response = requests.get("http://localhost:8000/api/v1/printers")
printers = response.json()

# Crear una nueva impresora
new_printer = {
    "name": "HP LaserJet Pro",
    "model": "M404dn",
    "location": "Oficina Principal",
    "ip_address": "192.168.1.100"
}
response = requests.post(
    "http://localhost:8000/api/v1/printers",
    json=new_printer
)
```

## 🧪 Testing

### Ejecutar todos los tests
```bash
# Con Make
make test

# Con pytest directamente
pytest

# Con coverage
pytest --cov=src --cov-report=html
```

### Ejecutar tests específicos
```bash
# Solo tests unitarios
pytest tests/unit

# Solo tests de integración
pytest tests/integration

# Un archivo específico
pytest tests/unit/test_printer_service.py

# Con output verbose
pytest -v

# Con prints
pytest -s
```

### Generar reporte de cobertura
```bash
# Generar reporte HTML
pytest --cov=src --cov-report=html

# Ver reporte en el navegador
open htmlcov/index.html  # Mac
xdg-open htmlcov/index.html  # Linux
```

## 📚 API

### Documentación

La documentación completa de la API está disponible en:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Autenticación

La API utiliza JWT (JSON Web Tokens) para autenticación:

```bash
# Obtener token
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "password"}'

# Usar token en requests
curl -X GET "http://localhost:8000/api/v1/printers" \
  -H "Authorization: Bearer <tu-token-aqui>"
```

### Endpoints principales

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/v1/printers` | Listar todas las impresoras |
| POST | `/api/v1/printers` | Crear nueva impresora |
| GET | `/api/v1/printers/{id}` | Obtener impresora por ID |
| PUT | `/api/v1/printers/{id}` | Actualizar impresora |
| DELETE | `/api/v1/printers/{id}` | Eliminar impresora |
| GET | `/api/v1/jobs` | Listar trabajos de impresión |
| POST | `/api/v1/jobs` | Crear nuevo trabajo |
| GET | `/api/v1/reports/usage` | Reporte de uso |

## 🗄️ Base de Datos

### Migraciones

```bash
# Crear nueva migración
alembic revision --autogenerate -m "descripcion del cambio"

# Aplicar migraciones
alembic upgrade head

# Revertir última migración
alembic downgrade -1

# Ver historial de migraciones
alembic history

# Ver migración actual
alembic current
```

### Backup y Restore

```bash
# Backup
pg_dump -U printopt_user -h localhost printoptimizer_db > backup.sql

# Restore
psql -U printopt_user -h localhost printoptimizer_db < backup.sql

# Con Docker
docker-compose exec db pg_dump -U printopt_user printoptimizer_db > backup.sql
```

## 🐳 Docker

### Comandos útiles

```bash
# Construir imagen
docker-compose build

# Levantar servicios
docker-compose up -d

# Ver logs
docker-compose logs -f app

# Ejecutar comandos en el contenedor
docker-compose exec app bash
docker-compose exec app python -m pytest

# Detener servicios
docker-compose down

# Detener y eliminar volúmenes
docker-compose down -v
```

### Docker en producción

Para producción, usa el archivo `docker-compose.prod.yml`:

```bash
docker-compose -f docker-compose.prod.yml up -d
```

## 👨‍💻 Desarrollo

### Configurar entorno de desarrollo

```bash
# Instalar dependencias de desarrollo
pip install -r requirements-dev.txt

# Instalar pre-commit hooks
pre-commit install

# Ejecutar pre-commit en todos los archivos
pre-commit run --all-files
```

### Flujo de trabajo

1. **Crear rama desde main**
```bash
git checkout main
git pull origin main
git checkout -b feature/nombre-feature
```

2. **Hacer cambios y commits**
```bash
git add .
git commit -m "feat: descripción del cambio"
```

3. **Push y crear Pull Request**
```bash
git push origin feature/nombre-feature
```

### Guía de estilo

- Seguimos [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Usamos [Black](https://black.readthedocs.io/) para formateo
- Docstrings en formato [Google](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings)
- Type hints en todas las funciones

### Comandos Make útiles

```bash
make help        # Ver todos los comandos disponibles
make format      # Formatear código
make lint        # Ejecutar linters
make test        # Ejecutar tests
make clean       # Limpiar archivos temporales
make dev         # Iniciar entorno de desarrollo
```

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Por favor, lee nuestra [guía de contribución](CONTRIBUTING.md) para más detalles.

### Proceso de contribución

1. Fork el proyecto
2. Crea tu rama de feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'feat: add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

### Tipos de contribuciones

- 🐛 Reportar bugs
- 💡 Sugerir nuevas features
- 📝 Mejorar documentación
- 🔧 Enviar PRs con mejoras

## 🗺️ Roadmap

### v0.2.0 (Q2 2024)
- [ ] Sistema de notificaciones
- [ ] Dashboard de analytics
- [ ] API GraphQL
- [ ] Soporte multi-idioma

### v0.3.0 (Q3 2024)
- [ ] Aplicación móvil
- [ ] Integración con Active Directory
- [ ] Machine Learning para optimización
- [ ] Soporte para Cloud Printing

### v1.0.0 (Q4 2024)
- [ ] Alta disponibilidad
- [ ] Kubernetes support
- [ ] Marketplace de plugins
- [ ] SaaS mode

Ver el [proyecto en GitHub](https://github.com/tu-usuario/PrintOptimizer_BD/projects) para más detalles.

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## ✨ Autores

- **Tu Nombre** - *Trabajo inicial* - [@tu-usuario](https://github.com/tu-usuario)

### Colaboradores

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- ALL-CONTRIBUTORS-LIST:END -->

## 🙏 Agradecimientos

- FastAPI por el excelente framework
- SQLAlchemy team
- Todos los contribuidores

---

<div align="center">

Hecho por [José Ángel](https://github.com/Angel-Alvarez-Dev)

[⬆ Volver arriba](#printoptimizer_bd)

</div>