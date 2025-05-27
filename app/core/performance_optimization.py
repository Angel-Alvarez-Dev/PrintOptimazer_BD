# app/core/performance_optimization.py
"""
Production performance optimization and configuration
"""
import asyncio
import functools
import time
from typing import Dict, Any, Optional, Callable
from sqlalchemy import event, engine_from_config
from sqlalchemy.pool import QueuePool
from sqlalchemy.orm import sessionmaker
import redis
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

class DatabaseOptimizer:
    """Database performance optimization"""
    
    @staticmethod
    def configure_postgresql_pool():
        """Configure PostgreSQL connection pool for production"""
        pool_config = {
            "poolclass": QueuePool,
            "pool_size": 20,
            "max_overflow": 30,
            "pool_pre_ping": True,
            "pool_recycle": 3600,  # 1 hour
            "pool_timeout": 30,
            "echo": False,  # Disable SQL logging in production
        }
        return pool_config
    
    @staticmethod
    def configure_query_optimization():
        """Configure query optimization settings"""
        optimization_config = {
            # Connection settings
            "connect_args": {
                "options": "-c default_transaction_isolation=read_committed "
                          "-c timezone=UTC "
                          "-c statement_timeout=30000 "  # 30 seconds
                          "-c lock_timeout=10000 "       # 10 seconds
                          "-c idle_in_transaction_session_timeout=300000 "  # 5 minutes
                          "-c shared_preload_libraries=pg_stat_statements "
                          "-c track_activity_query_size=2048 "
                          "-c log_min_duration_statement=1000 "  # Log slow queries > 1s
            }
        }
        return optimization_config

class RedisOptimizer:
    """Redis performance optimization"""
    
    @staticmethod
    def configure_redis_connection():
        """Configure Redis for optimal performance"""
        redis_config = {
            "host": settings.REDIS_HOST if hasattr(settings, 'REDIS_HOST') else "localhost",
            "port": settings.REDIS_PORT if hasattr(settings, 'REDIS_PORT') else 6379,
            "db": 0,
            "decode_responses": False,  # Keep binary for better performance
            "max_connections": 100,
            "retry_on_timeout": True,
            "health_check_interval": 30,
            "socket_keepalive": True,
            "socket_keepalive_options": {
                1: 1,  # TCP_KEEPIDLE
                2: 3,  # TCP_KEEPINTVL  
                3: 5,  # TCP_KEEPCNT
            }
        }
        return redis_config
    
    @staticmethod
    def configure_redis_cluster():
        """Configure Redis cluster for high availability"""
        cluster_config = {
            "startup_nodes": [
                {"host": "redis-node-1", "port": 7000},
                {"host": "redis-node-2", "port": 7000},
                {"host": "redis-node-3", "port": 7000},
            ],
            "decode_responses": False,
            "skip_full_coverage_check": True,
            "max_connections_per_node": 50,
        }
        return cluster_config

class CacheOptimizer:
    """Advanced caching strategies"""
    
    def __init__(self, redis_client):
        self.redis_client = redis_client
        self.cache_stats = {"hits": 0, "misses": 0}
    
    async def get_or_set(self, key: str, factory: Callable, expire: int = 300):
        """Get from cache or set using factory function"""
        try:
            # Try to get from cache
            cached_value = await self.redis_client.get(key)
            if cached_value:
                self.cache_stats["hits"] += 1
                return cached_value
            
            # Cache miss - compute value
            self.cache_stats["misses"] += 1
            value = await factory()
            
            # Set in cache with expiration
            await self.redis_client.setex(key, expire, value)
            return value
            
        except Exception as e:
            logger.error(f"Cache error for key {key}: {e}")
            # Fallback to direct computation
            return await factory()
    
    def cache_key_generator(self, prefix: str, **kwargs) -> str:
        """Generate consistent cache keys"""
        key_parts = [prefix]
        for k, v in sorted(kwargs.items()):
            key_parts.append(f"{k}:{v}")
        return ":".join(key_parts)
    
    async def invalidate_pattern(self, pattern: str):
        """Invalidate cache keys matching pattern"""
        try:
            keys = await self.redis_client.keys(pattern)
            if keys:
                await self.redis_client.delete(*keys)
                logger.info(f"Invalidated {len(keys)} cache keys matching {pattern}")
        except Exception as e:
            logger.error(f"Cache invalidation error for pattern {pattern}: {e}")

class APIOptimizer:
    """API performance optimization"""
    
    @staticmethod
    def configure_uvicorn_production():
        """Configure Uvicorn for production"""
        return {
            "host": "0.0.0.0",
            "port": 8000,
            "workers": 4,  # Adjust based on CPU cores
            "worker_class": "uvicorn.workers.UvicornWorker",
            "worker_connections": 1000,
            "max_requests": 1000,
            "max_requests_jitter": 100,
            "timeout": 30,
            "keepalive": 2,
            "preload_app": True,
            "access_log": False,  # Use structured logging instead
            "error_log": "-",
            "log_level": "info",
        }
    
    @staticmethod
    def configure_response_compression():
        """Configure response compression"""
        return {
            "compression_level": 6,
            "minimum_size": 1024,
            "excluded_media_types": [
                "image/jpeg",
                "image/png", 
                "image/gif",
                "application/pdf",
                "application/octet-stream",
            ]
        }
