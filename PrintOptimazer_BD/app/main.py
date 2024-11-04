from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from . import models, schemas, crud
from .database import SessionLocal, engine

# Crear la aplicación FastAPI
app = FastAPI(title="PrintOptimizer_BD")

# Crear las tablas en la base de datos
models.Base.metadata.create_all(bind=engine)

# Dependencia para obtener la sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Rutas para Usuarios
@app.post("/users/", response_model=schemas.User, summary="Crear un nuevo usuario")
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email ya registrado")
    return crud.create_user(db=db, user=user)

@app.get("/users/{user_id}", response_model=schemas.User, summary="Obtener usuario por ID")
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_user

# Rutas para Categorías
@app.post("/categories/", response_model=schemas.Category, summary="Crear una nueva categoría")
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    return crud.create_category(db=db, category=category)

@app.get("/categories/", response_model=List[schemas.Category], summary="Obtener lista de categorías")
def read_categories(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_categories(db, skip=skip, limit=limit)

# Rutas para Proyectos
@app.post("/projects/", response_model=schemas.Project, summary="Crear un nuevo proyecto")
def create_project(project: schemas.ProjectCreate, db: Session = Depends(get_db)):
    return crud.create_project(db=db, project=project)

@app.get("/projects/{project_id}", response_model=schemas.Project, summary="Obtener proyecto por ID")
def read_project(project_id: int, db: Session = Depends(get_db)):
    db_project = crud.get_project(db, project_id=project_id)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    return db_project

# Rutas para Tags
@app.post("/tags/", response_model=schemas.Tag, summary="Crear un nuevo tag")
def create_tag(tag: schemas.TagCreate, db: Session = Depends(get_db)):
    return crud.create_tag(db=db, tag=tag)

@app.get("/tags/", response_model=List[schemas.Tag], summary="Obtener lista de tags")
def read_tags(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_tags(db, skip=skip, limit=limit)

# Rutas para MarketStats
@app.post("/market_stats/", response_model=schemas.MarketStat, summary="Crear estadísticas de mercado")
def create_market_stat(market_stat: schemas.MarketStatCreate, db: Session = Depends(get_db)):
    return crud.create_market_stat(db=db, market_stat=market_stat)

@app.get("/market_stats/{market_stat_id}", response_model=schemas.MarketStat, summary="Obtener estadísticas de mercado por ID")
def read_market_stat(market_stat_id: int, db: Session = Depends(get_db)):
    db_market_stat = crud.get_market_stat(db, market_stat_id=market_stat_id)
    if db_market_stat is None:
        raise HTTPException(status_code=404, detail="Estadísticas de mercado no encontradas")
    return db_market_stat

# Ruta raíz de bienvenida
@app.get("/", summary="Página de inicio")
def read_root():
    return {"message": "Bienvenido a la API de PrintOptimizer_BD"}
