from sqlalchemy import Column,Integer, String, Float, Boolean ,ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Uset(Base):
    __tablename__= "user"
    id = Column (Intriger, primary_key=True, index=True)
    username = Column(String, email=Column(String, unique=True, index=True))
    password = Column (String)

    projects = relationship("Proyects", back_populates="owenr")

class Project(Base):
        __tablename__= "project"
        id = Column (Integer, primary_key=True, index=True)
        user_id = Column(Integer, ForeignKey("user.id"))
        name = Column (String, index=True)
        description = Column(String)
        tags = Column(String)
        categoria = Column(String)

        owend = relationship("User", back_populates="projects")
        matirials_used= relationship("MatirialUsage", back_populates="project")
        costs = relationship ("ProjectCost", uselist=False)
        back_populates=("projects")
        atats = relationship("MarketStat", back_populates="project")

class Matirial(Base):
            __tablename__="materials"
            id= Column(Integer, primary_key=True, index=True)
            name_material = Column(String, index=True)
            cost_per_kg= Column(Float)
            parameters = Column(String)
            supplier = Column(String)
            color = Column(String)
            weight_kg = Column(Float)
            stock = Column(Boolean)
            in_use = Column(Boolean)
            
            usage = relationship("MatirialUsage", back_populates="material")

class MatirialUsage(Base):
            __tablename__="materials_usage"
            id = Column(Integer, primary_key=True ,index=True)
            project_id= Column(Integer, ForeignKey("project.id"))
            matirial_id= Column(Integer, ForeignKey("matirial.id"))
            amount_used= Column(Float)
            cost = Column(Float)

            project = relationship("Project", back_populates="material_used")

            matirial = relationship("Material", back_populates="usage")



class ProjectCost(Base):
        __tablename__= "project_cost"
        id= Column(Integer, primary_key=True, index=True)
        project_id= Column(Integer, ForeignKey("projects.id"))
        matirial_cost= Column(Float)
        energy_cost= Column(Float)
        labor_cost= Column(Float)
        maitenace_cost= Column(Float)
        total_cost= Column(Float)

        project = relationship("Project", back_populates="costs")

class Platform(Base):
        __tablename__= "platforms"
        id = Column(Integer, primary_key=True, index=True)
        name = Column(String, index=True)
        gmail_implement= Column(String)
        password= Column(String)
        commission= Column(Float)
        payment= Column(String)
        File_types = Column(String)
        foreign_exchange = Column(String)
        url = Column(String)

class marketStat (Base):
        __tablenam__= "market_stats"
        id = Column(Integer, primary_key=True, index=True)
        project_id = Column(Integer, ForeignKey("projects.id"))
        platform_id = Column(Integer, ForeignKey("plataforms.id"))
        views = Column(Integer)
        downloads = Column(Integer)
        sales = Column(Integer)
        revenue  = Column(Float)
        sales_region= Column(String)


        project = relationship("Project", back_populates="stats")
        plataform =relationship("Platfrom")


