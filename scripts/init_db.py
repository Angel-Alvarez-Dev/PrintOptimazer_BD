# scripts/init_db.py
"""
Database initialization script
Creates default admin user and sample data
"""
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy.orm import Session
from app.core.database import engine, SessionLocal, init_db
from app.core.auth import create_user_account
from app.models.models import User, Material, MaterialType
from app.core.config import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_admin_user(db: Session) -> User:
    """Create default admin user"""
    try:
        admin_user = create_user_account(
            db=db,
            username="admin",
            email="admin@printoptimizer.com",
            password="admin123",
            full_name="Administrator",
            business_name="PrintOptimizer Demo",
            role="admin"
        )
        logger.info("Admin user created successfully")
        return admin_user
    except Exception as e:
        logger.warning(f"Admin user might already exist: {e}")
        return db.query(User).filter(User.username == "admin").first()

def create_sample_materials(db: Session, user: User):
    """Create sample materials"""
    sample_materials = [
        {
            "name": "PLA Filament - Black",
            "brand": "eSUN",
            "material_type": MaterialType.FILAMENT,
            "color": "Black",
            "current_stock": 5.0,
            "unit": "kg",
            "low_stock_threshold": 2.0,
            "reorder_threshold": 1.0,
            "cost_per_unit": 25.0,
            "supplier": "Amazon",
            "properties": {
                "print_temp": "190-220°C",
                "bed_temp": "50-60°C",
                "density": "1.24 g/cm³"
            }
        },
        {
            "name": "PETG Filament - Clear",
            "brand": "Overture",
            "material_type": MaterialType.FILAMENT,
            "color": "Clear",
            "current_stock": 3.0,
            "unit": "kg",
            "low_stock_threshold": 1.0,
            "reorder_threshold": 0.5,
            "cost_per_unit": 30.0,
            "supplier": "Amazon",
            "properties": {
                "print_temp": "230-250°C",
                "bed_temp": "70-80°C",
                "density": "1.27 g/cm³"
            }
        },
        {
            "name": "Standard Resin - Grey",
            "brand": "Elegoo",
            "material_type": MaterialType.RESIN,
            "color": "Grey",
            "current_stock": 2.0,
            "unit": "L",
            "low_stock_threshold": 1.0,
            "reorder_threshold": 0.5,
            "cost_per_unit": 35.0,
            "supplier": "Elegoo Store",
            "properties": {
                "cure_time": "2-3s per layer",
                "density": "1.05 g/cm³",
                "shore_hardness": "83D"
            }
        }
    ]
    
    for material_data in sample_materials:
        material = Material(**material_data, user_id=user.id)
        db.add(material)
    
    db.commit()
    logger.info("Sample materials created successfully")

def main():
    """Initialize database with sample data"""
    logger.info("Starting database initialization...")
    
    # Initialize database tables
    init_db()
    
    # Create session
    db = SessionLocal()
    
    try:
        # Create admin user
        admin_user = create_admin_user(db)
        
        if admin_user:
            # Create sample materials
            create_sample_materials(db, admin_user)
            
            logger.info("Database initialization completed successfully!")
            logger.info("Admin credentials:")
            logger.info("Username: admin")
            logger.info("Password: admin123")
        else:
            logger.error("Failed to create admin user")
            
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()
