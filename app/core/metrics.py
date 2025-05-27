# app/core/metrics.py
"""
Business metrics and KPI tracking
"""
import time
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from app.models.models import Project, Quote, Material, User, ModelFile
import asyncio

@dataclass
class BusinessMetrics:
    """Business metrics data structure"""
    # Revenue metrics
    total_revenue: float = 0.0
    monthly_recurring_revenue: float = 0.0
    average_order_value: float = 0.0
    
    # Customer metrics
    total_customers: int = 0
    active_customers: int = 0
    new_customers_this_month: int = 0
    customer_retention_rate: float = 0.0
    
    # Project metrics
    total_projects: int = 0
    completed_projects: int = 0
    average_project_duration: float = 0.0
    project_success_rate: float = 0.0
    
    # Operational metrics
    total_quotes_sent: int = 0
    quote_to_project_conversion_rate: float = 0.0
    average_quote_value: float = 0.0
    
    # Inventory metrics
    total_materials: int = 0
    materials_low_stock: int = 0
    inventory_turnover_rate: float = 0.0
    
    # Efficiency metrics
    average_response_time: float = 0.0
    api_uptime_percentage: float = 0.0
    user_satisfaction_score: float = 0.0
    
    # Growth metrics
    month_over_month_growth: float = 0.0
    user_acquisition_cost: float = 0.0
    customer_lifetime_value: float = 0.0
    
    timestamp: datetime = field(default_factory=datetime.utcnow)

class MetricsCollector:
    """Collect and calculate business metrics"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def calculate_revenue_metrics(self) -> Dict[str, float]:
        """Calculate revenue-related metrics"""
        # Total revenue from completed projects
        total_revenue = self.db.query(func.sum(Project.budget)).filter(
            Project.status == "completed"
        ).scalar() or 0.0
        
        # Monthly recurring revenue (last 30 days)
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        monthly_revenue = self.db.query(func.sum(Project.budget)).filter(
            and_(
                Project.status == "completed",
                Project.updated_at >= thirty_days_ago
            )
        ).scalar() or 0.0
        
        # Average order value
        completed_projects_count = self.db.query(Project).filter(
            Project.status == "completed"
        ).count()
        
        average_order_value = (
            total_revenue / completed_projects_count 
            if completed_projects_count > 0 else 0.0
        )
        
        return {
            "total_revenue": total_revenue,
            "monthly_recurring_revenue": monthly_revenue,
            "average_order_value": average_order_value
        }
    
    def calculate_customer_metrics(self) -> Dict[str, float]:
        """Calculate customer-related metrics"""
        # Total and active customers
        total_customers = self.db.query(User).filter(User.role == "user").count()
        
        # Active customers (had activity in last 30 days)
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        active_customers = self.db.query(User).filter(
            and_(
                User.role == "user",
                User.updated_at >= thirty_days_ago
            )
        ).count()
        
        # New customers this month
        start_of_month = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        new_customers = self.db.query(User).filter(
            and_(
                User.role == "user",
                User.created_at >= start_of_month
            )
        ).count()
        
        # Customer retention rate (simplified)
        retention_rate = (active_customers / total_customers * 100) if total_customers > 0 else 0.0
        
        return {
            "total_customers": total_customers,
            "active_customers": active_customers,
            "new_customers_this_month": new_customers,
            "customer_retention_rate": retention_rate
        }
    
    def calculate_project_metrics(self) -> Dict[str, float]:
        """Calculate project-related metrics"""
        total_projects = self.db.query(Project).count()
        completed_projects = self.db.query(Project).filter(
            Project.status == "completed"
        ).count()
        
        # Average project duration (in days)
        completed_projects_with_dates = self.db.query(Project).filter(
            and_(
                Project.status == "completed",
                Project.created_at.isnot(None),
                Project.updated_at.isnot(None)
            )
        ).all()
        
        if completed_projects_with_dates:
            total_duration = sum([
                (project.updated_at - project.created_at).days
                for project in completed_projects_with_dates
            ])
            average_duration = total_duration / len(completed_projects_with_dates)
        else:
            average_duration = 0.0
        
        # Project success rate
        success_rate = (completed_projects / total_projects * 100) if total_projects > 0 else 0.0
        
        return {
            "total_projects": total_projects,
            "completed_projects": completed_projects,
            "average_project_duration": average_duration,
            "project_success_rate": success_rate
        }
    
    def calculate_quote_metrics(self) -> Dict[str, float]:
        """Calculate quote-related metrics"""
        total_quotes = self.db.query(Quote).count()
        accepted_quotes = self.db.query(Quote).filter(
            Quote.status == "accepted"
        ).count()
        
        # Quote to project conversion rate
        projects_from_quotes = self.db.query(Project).filter(
            Project.client_name.isnot(None)  # Assuming projects with clients came from quotes
        ).count()
        
        conversion_rate = (projects_from_quotes / total_quotes * 100) if total_quotes > 0 else 0.0
        
        # Average quote value
        average_quote_value = self.db.query(func.avg(Quote.total_amount)).scalar() or 0.0
        
        return {
            "total_quotes_sent": total_quotes,
            "quote_to_project_conversion_rate": conversion_rate,
            "average_quote_value": average_quote_value
        }
    
    def calculate_inventory_metrics(self) -> Dict[str, float]:
        """Calculate inventory-related metrics"""
        total_materials = self.db.query(Material).count()
        
        materials_low_stock = self.db.query(Material).filter(
            Material.current_stock <= Material.low_stock_threshold
        ).count()
        
        # Simplified inventory turnover rate
        # This would need more complex calculation in real scenario
        inventory_turnover_rate = 0.0  # Placeholder
        
        return {
            "total_materials": total_materials,
            "materials_low_stock": materials_low_stock,
            "inventory_turnover_rate": inventory_turnover_rate
        }
    
    def collect_all_metrics(self) -> BusinessMetrics:
        """Collect all business metrics"""
        revenue_metrics = self.calculate_revenue_metrics()
        customer_metrics = self.calculate_customer_metrics()
        project_metrics = self.calculate_project_metrics()
        quote_metrics = self.calculate_quote_metrics()
        inventory_metrics = self.calculate_inventory_metrics()
        
        return BusinessMetrics(
            # Revenue metrics
            total_revenue=revenue_metrics["total_revenue"],
            monthly_recurring_revenue=revenue_metrics["monthly_recurring_revenue"],
            average_order_value=revenue_metrics["average_order_value"],
            
            # Customer metrics
            total_customers=customer_metrics["total_customers"],
            active_customers=customer_metrics["active_customers"],
            new_customers_this_month=customer_metrics["new_customers_this_month"],
            customer_retention_rate=customer_metrics["customer_retention_rate"],
            
            # Project metrics
            total_projects=project_metrics["total_projects"],
            completed_projects=project_metrics["completed_projects"],
            average_project_duration=project_metrics["average_project_duration"],
            project_success_rate=project_metrics["project_success_rate"],
            
            # Quote metrics
            total_quotes_sent=quote_metrics["total_quotes_sent"],
            quote_to_project_conversion_rate=quote_metrics["quote_to_project_conversion_rate"],
            average_quote_value=quote_metrics["average_quote_value"],
            
            # Inventory metrics
            total_materials=inventory_metrics["total_materials"],
            materials_low_stock=inventory_metrics["materials_low_stock"],
            inventory_turnover_rate=inventory_metrics["inventory_turnover_rate"]
        )