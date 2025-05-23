.PHONY: help install dev-install run test lint format clean docker-up docker-down migrate

# Variables
PYTHON := python3
PIP := pip3
DOCKER_COMPOSE := docker-compose
APP_NAME := printoptimizer

# Colores
GREEN := \033[0;32m
YELLOW := \033[1;33m
RED := \033[0;31m
NC := \033[0m # No Color

help: ## Mostrar esta ayuda
	@echo "$(GREEN)Comandos disponibles:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Instalar dependencias de producción
	@echo "$(GREEN)Instalando dependencias...$(NC)"
	$(PIP) install -r requirements.txt

dev-install: install ## Instalar dependencias de desarrollo
	@echo "$(GREEN)Instalando dependencias de desarrollo...$(NC)"
	$(PIP) install -r requirements-dev.txt
	pre-commit install

run: ## Ejecutar aplicación localmente
	@echo "$(GREEN)Iniciando aplicación...$(NC)"
	cd src && $(PYTHON) -m uvicorn printoptimizer.main:app --reload --host 0.0.0.0 --port 8000

test: ## Ejecutar tests
	@echo "$(GREEN)Ejecutando tests...$(NC)"
	pytest tests/ -v

test-cov: ## Ejecutar tests con cobertura
	@echo "$(GREEN)Ejecutando tests con cobertura...$(NC)"
	pytest tests/ -v --cov=src --cov-report=html --cov-report=term

lint: ## Ejecutar linters
	@echo "$(GREEN)Running flake8...$(NC)"
	flake8 src/ tests/ || true
	@echo "$(GREEN)Running mypy...$(NC)"
	mypy src/ || true
	@echo "$(GREEN)Running black check...$(NC)"
	black --check src/ tests/ || true
	@echo "$(GREEN)Running isort check...$(NC)"
	isort --check-only src/ tests/ || true

format: ## Formatear código
	@echo "$(GREEN)Formateando código...$(NC)"
	black src/ tests/
	isort src/ tests/

clean: ## Limpiar archivos temporales
	@echo "$(YELLOW)Limpiando archivos temporales...$(NC)"
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .coverage htmlcov .mypy_cache

# Docker commands
docker-up: ## Levantar servicios con Docker
	@echo "$(GREEN)Levantando servicios Docker...$(NC)"
	$(DOCKER_COMPOSE) -f docker/docker-compose.yml up -d

docker-down: ## Detener servicios Docker
	@echo "$(YELLOW)Deteniendo servicios Docker...$(NC)"
	$(DOCKER_COMPOSE) -f docker/docker-compose.yml down

docker-logs: ## Ver logs de Docker
	$(DOCKER_COMPOSE) -f docker/docker-compose.yml logs -f

docker-build: ## Construir imagen Docker
	@echo "$(GREEN)Construyendo imagen Docker...$(NC)"
	$(DOCKER_COMPOSE) -f docker/docker-compose.yml build

# Database commands
migrate: ## Ejecutar migraciones
	@echo "$(GREEN)Ejecutando migraciones...$(NC)"
	alembic upgrade head

migration: ## Crear nueva migración
	@echo "$(GREEN)Creando nueva migración...$(NC)"
	@read -p "Nombre de la migración: " name; \
	alembic revision --autogenerate -m "$$name"

db-shell: ## Acceder a shell de PostgreSQL
	$(DOCKER_COMPOSE) -f docker/docker-compose.yml exec db psql -U printopt_user -d printoptimizer_db

# Development workflow
dev: ## Iniciar entorno de desarrollo completo
	@echo "$(GREEN)Iniciando entorno de desarrollo...$(NC)"
	$(DOCKER_COMPOSE) -f docker/docker-compose.yml -f docker/docker-compose.dev.yml up

setup: ## Configurar proyecto desde cero
	@echo "$(GREEN)Configurando proyecto PrintOptimizer_BD...$(NC)"
	@chmod +x scripts/setup_dev.sh 2>/dev/null || true
	@./scripts/setup_dev.sh 2>/dev/null || echo "Script de setup no encontrado"
