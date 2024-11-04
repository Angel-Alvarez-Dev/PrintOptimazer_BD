# backend/__init__.py

from .database import Base, SessionLocal, engine
from .models import User, UserRole, Category, Tag, Project, ProjectTag, ProjectCostHistory, MarketStat, SalesRegionStat
from .crud import create_user, get_user_by_email, create_category, create_project

# Definir qué elementos están disponibles al importar `app`
__all__ = [
    "Base", "SessionLocal", "engine",
    "User", "UserRole", "Category", "Tag", "Project", "ProjectTag", "ProjectCostHistory", "MarketStat", "SalesRegionStat",
    "create_user", "get_user_by_email", "create_category", "create_project"
]
