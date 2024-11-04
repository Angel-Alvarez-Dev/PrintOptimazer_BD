from sqlalchemy.orm import Session
from faker import Faker
import random
from PrintOptimazer_BD.backend.models import User, UserRole, Project, Category, Tag, ProjectTag, ProjectCost, ProjectCostHistory, Material, MaterialUsage, MarketStat, SalesRegionStat, Platform  # Importa tus modelos
from database import engine  # Asume que tienes un archivo de configuración de Base de Datos

# Configuración de Faker
fake = Faker()

def populate_roles(session):
    roles = ['Admin', 'User', 'Editor']
    role_instances = [UserRole(name=role) for role in roles]
    session.add_all(role_instances)
    session.commit()
    return role_instances

def populate_users(session, roles):
    users = []
    user_data = [
        {"username": "jdoe", "email": "jdoe@example.com", "password": "password123", "role": "User"},
        {"username": "asmith", "email": "asmith@example.com", "password": "password123", "role": "Admin"},
        {"username": "mbrown", "email": "mbrown@example.com", "password": "password123", "role": "Editor"},
        {"username": "cjohnson", "email": "cjohnson@example.com", "password": "password123", "role": "User"},
        {"username": "lwhite", "email": "lwhite@example.com", "password": "password123", "role": "User"},
    ]
    
    for data in user_data:
        role = next((r for r in roles if r.name == data['role']), None)
        user = User(
            username=data['username'],
            email=data['email'],
            password_hash=fake.sha256(),  # Genera un hash aleatorio simulado
            role_id=role.id if role else None
        )
        users.append(user)
    session.add_all(users)
    session.commit()
    return users

def populate_categories(session):
    categories = ['Technology', 'Art', 'Science', 'Business', 'Education']
    category_instances = [Category(name=cat) for cat in categories]
    session.add_all(category_instances)
    session.commit()
    return category_instances

def populate_tags(session):
    tags = ['AI', 'Blockchain', 'ML', 'Design', 'Robotics', 'Software', 'Data', 'Finance', 'Education', 'Health']
    tag_instances = [Tag(name=tag) for tag in tags]
    session.add_all(tag_instances)
    session.commit()
    return tag_instances

def populate_projects(session, users, categories, tags):
    projects = []
    for _ in range(10):
        project = Project(
            user_id=random.choice(users).id,
            category_id=random.choice(categories).id,
            name=fake.bs(),
            description=fake.paragraph(),
        )
        projects.append(project)
    session.add_all(projects)
    session.commit()

    # Asigna etiquetas a los proyectos
    for project in projects:
        num_tags = random.randint(1, 3)  # Cada proyecto tendrá entre 1 y 3 etiquetas
        project_tags = [ProjectTag(project_id=project.id, tag_id=random.choice(tags).id) for _ in range(num_tags)]
        session.add_all(project_tags)
    session.commit()
    return projects

def populate_materials(session):
    materials = []
    for _ in range(10):
        material = Material(
            material_name=fake.word(),
            cost_per_kg=round(random.uniform(10, 100), 2),
            parameters=fake.sentence(),
            supplier=fake.company(),
            color=fake.color_name(),
            weight_kg=round(random.uniform(1, 50), 2),
            in_stock=fake.boolean(),
            in_use=fake.boolean()
        )
        materials.append(material)
    session.add_all(materials)
    session.commit()
    return materials

def populate_material_usage(session, projects, materials):
    usages = []
    for project in projects:
        num_materials = random.randint(1, 3)
        for _ in range(num_materials):
            usage = MaterialUsage(
                project_id=project.id,
                material_id=random.choice(materials).id,
                amount_used=round(random.uniform(1, 10), 2),
                cost=round(random.uniform(50, 500), 2)
            )
            usages.append(usage)
    session.add_all(usages)
    session.commit()
    return usages

def populate_project_costs(session, projects):
    costs = []
    for project in projects:
        cost = ProjectCost(
            project_id=project.id,
            material_cost=round(random.uniform(500, 1000), 2),
            energy_cost=round(random.uniform(200, 700), 2),
            labor_cost=round(random.uniform(300, 800), 2),
            maintenance_cost=round(random.uniform(100, 400), 2),
            total_cost=round(random.uniform(1200, 2500), 2)
        )
        costs.append(cost)
    session.add_all(costs)
    session.commit()
    return costs

def populate_project_cost_history(session, projects):
    cost_histories = []
    for project in projects:
        for _ in range(3):  # Tres registros de historial por proyecto
            cost_history = ProjectCostHistory(
                project_id=project.id,
                material_cost=round(random.uniform(500, 1000), 2),
                energy_cost=round(random.uniform(200, 700), 2),
                labor_cost=round(random.uniform(300, 800), 2),
                maintenance_cost=round(random.uniform(100, 400), 2),
                total_cost=round(random.uniform(1200, 2500), 2),
                recorded_at=fake.date_time_this_decade()
            )
            cost_histories.append(cost_history)
    session.add_all(cost_histories)
    session.commit()
    return cost_histories

def populate_platforms(session):
    platforms = []
    for _ in range(5):  # Cinco plataformas diferentes
        platform = Platform(
            name=fake.company(),
            email=fake.email(),
            password_hash=fake.sha256(),
            commission=round(random.uniform(5, 15), 2),
            payment_method=fake.credit_card_provider(),
            supported_file_types="PDF, PNG, JPG",
            foreign_exchange_info="USD, EUR",
            url=fake.url()
        )
        platforms.append(platform)
    session.add_all(platforms)
    session.commit()
    return platforms

def populate_market_stats(session, projects, platforms):
    stats = []
    for project in projects:
        for platform in platforms:
            stat = MarketStat(
                project_id=project.id,
                platform_id=platform.id,
                views=random.randint(100, 1000),
                downloads=random.randint(50, 500),
                sales=random.randint(20, 200),
                revenue=round(random.uniform(1000, 5000), 2)
            )
            stats.append(stat)
    session.add_all(stats)
    session.commit()
    return stats

def populate_sales_region_stats(session, market_stats):
    regions = ['North America', 'Europe', 'Asia', 'South America', 'Africa']
    sales_region_stats = []
    for stat in market_stats:
        for region in random.sample(regions, 2):  # Dos regiones por estadística
            sales_region_stat = SalesRegionStat(
                market_stat_id=stat.id,
                region=region,
                sales=random.randint(10, 50),
                revenue=round(random.uniform(100, 1000), 2)
            )
            sales_region_stats.append(sales_region_stat)
    session.add_all(sales_region_stats)
    session.commit()
    return sales_region_stats

def main():
    session = Session(engine)
    roles = populate_roles(session)
    users = populate_users(session, roles)
    categories = populate_categories(session)
    tags = populate_tags(session)
    projects = populate_projects(session, users, categories, tags)
    materials = populate_materials(session)
    populate_material_usage(session, projects, materials)
    populate_project_costs(session, projects)
    populate_project_cost_history(session, projects)
    platforms = populate_platforms(session)
    market_stats = populate_market_stats(session, projects, platforms)
    populate_sales_region_stats(session, market_stats)
    session.close()

if __name__ == "__main__":
    main()
