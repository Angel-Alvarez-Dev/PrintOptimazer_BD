from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from PrintOptimazer_BD.app.database import Base  # Cambiado a importación absoluta
from PrintOptimazer_BD.app.models import User, UserRole, Category, Tag, Project, ProjectCostHistory, MarketStat, SalesRegionStat  # Cambiado a importación absoluta

# URL de conexión a la base de datos PostgreSQL
DATABASE_URL = "postgresql://print_admin:Mr@localhost/printoptimizer_db"

# Configurar el motor de la base de datos
engine = create_engine(DATABASE_URL)

# Crear todas las tablas en la base de datos
Base.metadata.create_all(bind=engine)

print("Tablas creadas correctamente.")
