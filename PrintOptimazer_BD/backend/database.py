from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL de conexión a la base de datos PostgreSQL
DATABASE_URL = "postgresql://print_admin:MR.232004@localhost/printoptimizer_db"

# Configurar el motor de la base de datos
engine = create_engine(DATABASE_URL)

# Crear una sesión local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para definir modelos de SQLAlchemy
Base = declarative_base()
