from sqlalchemy.orm import Session

from . import models
from . import schemas
from datetime import datetime

# CRUD para User
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(username=user.username, email=user.email, password_hash=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# CRUD para Category
def get_category(db: Session, category_id: int):
    return db.query(models.Category).filter(models.Category.id == category_id).first()

def get_categories(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Category).offset(skip).limit(limit).all()

def create_category(db: Session, category: schemas.CategoryCreate):
    db_category = models.Category(name=category.name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

# CRUD para Project
def get_project(db: Session, project_id: int):
    return db.query(models.Project).filter(models.Project.id == project_id).first()

def get_projects(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Project).offset(skip).limit(limit).all()

def create_project(db: Session, project: schemas.ProjectCreate, user_id: int):
    db_project = models.Project(
        name=project.name,
        description=project.description,
        user_id=user_id,
        category_id=project.category_id
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

# CRUD para Tag
def get_tag(db: Session, tag_id: int):
    return db.query(models.Tag).filter(models.Tag.id == tag_id).first()

def get_tags(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Tag).offset(skip).limit(limit).all()

def create_tag(db: Session, tag: schemas.TagCreate):
    db_tag = models.Tag(name=tag.name)
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag

# CRUD para MarketStat
def get_market_stat(db: Session, market_stat_id: int):
    return db.query(models.MarketStat).filter(models.MarketStat.id == market_stat_id).first()

def get_market_stats(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.MarketStat).offset(skip).limit(limit).all()

def create_market_stat(db: Session, market_stat: schemas.MarketStatCreate):
    db_market_stat = models.MarketStat(
        project_id=market_stat.project_id,
        platform_id=market_stat.platform_id,
        views=market_stat.views,
        downloads=market_stat.downloads,
        sales=market_stat.sales,
        revenue=market_stat.revenue
    )
    db.add(db_market_stat)
    db.commit()
    db.refresh(db_market_stat)
    return db_market_stat
