from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

class UserRole(Base):
    __tablename__ = "user_roles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)  
    role_id = Column(Integer, ForeignKey("user_roles.id"))

    role = relationship("UserRole")
    projects = relationship("Project", back_populates="owner")

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    projects = relationship("Project", back_populates="category")

class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    project_tags = relationship("ProjectTag", back_populates="tag")

class ProjectTag(Base):
    __tablename__ = "project_tags"
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    tag_id = Column(Integer, ForeignKey("tags.id"))

    project = relationship("Project", back_populates="tags")
    tag = relationship("Tag", back_populates="project_tags")

class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    category_id = Column(Integer, ForeignKey("categories.id"))  
    name = Column(String, index=True)
    description = Column(String)

    owner = relationship("User", back_populates="projects")
    category = relationship("Category", back_populates="projects")
    tags = relationship("ProjectTag", back_populates="project")
    cost_details = relationship("ProjectCost", uselist=False, back_populates="project")
    stats = relationship("MarketStat", back_populates="project")

class ProjectCostHistory(Base):
    __tablename__ = "project_cost_history"
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    material_cost = Column(Float)
    energy_cost = Column(Float)
    labor_cost = Column(Float)
    maintenance_cost = Column(Float)
    total_cost = Column(Float)
    recorded_at = Column(DateTime, default=datetime.utcnow)

    project = relationship("Project", back_populates="cost_history")

class Platform(Base):
    __tablename__ = "platforms"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    market_stats = relationship("MarketStat", back_populates="platform")

class MarketStat(Base):
    __tablename__ = "market_stats"
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    platform_id = Column(Integer, ForeignKey("platforms.id"))
    views = Column(Integer)
    downloads = Column(Integer)
    sales = Column(Integer)
    revenue = Column(Float)

    project = relationship("Project", back_populates="stats")
    platform = relationship("Platform", back_populates="market_stats")
    sales_regions = relationship("SalesRegionStat", back_populates="market_stat")

class SalesRegionStat(Base):
    __tablename__ = "sales_region_stats"
    id = Column(Integer, primary_key=True, index=True)
    market_stat_id = Column(Integer, ForeignKey("market_stats.id"))
    region = Column(String)
    sales = Column(Integer)
    revenue = Column(Float)

    market_stat = relationship("MarketStat", back_populates="sales_regions")
