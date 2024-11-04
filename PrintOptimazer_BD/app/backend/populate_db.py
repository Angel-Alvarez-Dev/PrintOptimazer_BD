from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from PrintOptimazer_BD.app.database import Base
from PrintOptimazer_BD.app.models import User, UserRole, Project, Category, Tag, ProjectTag, ProjectCostHistory, Platform, MarketStat, SalesRegionStat

# Crea la base de datos
DATABASE_URL = "sqlite:///./test.db"  # Cambia esta URL según tu configuración
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crea las tablas
Base.metadata.create_all(bind=engine)

# Función para poblar la base de datos
def populate_db():
    db = SessionLocal()
    try:
        # Crear roles de usuario
        user_role = UserRole(name="admin")
        db.add(user_role)
        db.commit()  # Asegúrate de hacer commit para que el ID se asigne

        # Crear un usuario
        user = User(username="admin_user", email="admin@example.com", password_hash="hashed_password", role_id=user_role.id)
        db.add(user)
        db.commit()  # Asegúrate de hacer commit

        # Crear categorías
        category1 = Category(name="Diseño 3D")
        category2 = Category(name="Prototipos")
        db.add(category1)
        db.add(category2)
        db.commit()  # Asegúrate de hacer commit

        # Crear proyectos
        project1 = Project(name="Proyecto 1", description="Descripción del Proyecto 1", user_id=user.id, category_id=category1.id)
        project2 = Project(name="Proyecto 2", description="Descripción del Proyecto 2", user_id=user.id, category_id=category2.id)
        db.add(project1)
        db.add(project2)
        db.commit()  # Asegúrate de hacer commit

        # Crear historial de costos del proyecto
        cost_history1 = ProjectCostHistory(
            project_id=project1.id,  # Usamos el ID del proyecto directamente
            material_cost=20.0,
            energy_cost=5.0,
            labor_cost=10.0,
            maintenance_cost=2.0,
            total_cost=37.0
        )
        cost_history2 = ProjectCostHistory(
            project_id=project2.id,  # Usamos el ID del proyecto directamente
            material_cost=15.0,
            energy_cost=3.0,
            labor_cost=8.0,
            maintenance_cost=1.5,
            total_cost=27.5
        )

        # Añadir historial de costos a la base de datos
        db.add(cost_history1)
        db.add(cost_history2)

        # Confirmar los cambios en la base de datos
        db.commit()

    except Exception as e:
        db.rollback()
        print(f"Error al poblar la base de datos: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    populate_db()
