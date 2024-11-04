from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime

# UserRole schemas
class UserRoleBase(BaseModel):
    name: str = Field(..., title="Role name", description="Role of the user (e.g., Admin, User)")

class UserRoleCreate(UserRoleBase):
    pass

class UserRole(UserRoleBase):
    id: int

    class Config:
        orm_mode = True


# User schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    role: UserRole

    class Config:
        orm_mode = True


# Category schemas
class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int

    class Config:
        orm_mode = True


# Tag schemas
class TagBase(BaseModel):
    name: str

class TagCreate(TagBase):
    pass

class Tag(TagBase):
    id: int

    class Config:
        orm_mode = True


# ProjectTag schemas (relationship table between Project and Tag)
class ProjectTagBase(BaseModel):
    project_id: int
    tag_id: int

class ProjectTagCreate(ProjectTagBase):
    pass

class ProjectTag(ProjectTagBase):
    id: int
    tag: Tag

    class Config:
        orm_mode = True


# Project schemas
class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None

class ProjectCreate(ProjectBase):
    category_id: int

class Project(ProjectBase):
    id: int
    owner: User
    category: Category
    tags: List[ProjectTag] = []

    class Config:
        orm_mode = True


# ProjectCostHistory schemas
class ProjectCostHistoryBase(BaseModel):
    material_cost: float
    energy_cost: float
    labor_cost: float
    maintenance_cost: float
    total_cost: float
    recorded_at: Optional[datetime] = None

class ProjectCostHistoryCreate(ProjectCostHistoryBase):
    pass

class ProjectCostHistory(ProjectCostHistoryBase):
    id: int
    project_id: int

    class Config:
        orm_mode = True


# MarketStat schemas
class MarketStatBase(BaseModel):
    views: int
    downloads: int
    sales: int
    revenue: float

class MarketStatCreate(MarketStatBase):
    platform_id: int

class MarketStat(MarketStatBase):
    id: int
    project_id: int
    platform: Optional[str] = None
    sales_regions: List["SalesRegionStat"] = []

    class Config:
        orm_mode = True


# SalesRegionStat schemas
class SalesRegionStatBase(BaseModel):
    region: str
    sales: int
    revenue: float

class SalesRegionStatCreate(SalesRegionStatBase):
    pass

class SalesRegionStat(SalesRegionStatBase):
    id: int
    market_stat_id: int

    class Config:
        orm_mode = True
