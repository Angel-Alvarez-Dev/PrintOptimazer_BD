# app/core/logging_config.py
"""
Advanced logging configuration
"""
import logging
import logging.handlers
import os
import sys
from pathlib import Path
from datetime import datetime
import json

class JSONFormatter(logging.Formatter):
    """JSON formatter for structured logging"""
    
    def format(self, record):
        log_obj = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
        }
        
        # Add exception info if present
        if record.exc_info:
            log_obj['exception'] = self.formatException(record.exc_info)
        
        # Add extra fields
        for key, value in record.__dict__.items():
            if key not in ['name', 'msg', 'args', 'levelname', 'levelno', 'pathname', 
                          'filename', 'module', 'exc_info', 'exc_text', 'stack_info',
                          'lineno', 'funcName', 'created', 'msecs', 'relativeCreated',
                          'thread', 'threadName', 'processName', 'process', 'getMessage']:
                log_obj[key] = value
        
        return json.dumps(log_obj)

def setup_logging(
    log_level: str = "INFO",
    log_dir: str = "logs",
    enable_json: bool = False,
    enable_file_rotation: bool = True
):
    """Setup comprehensive logging configuration"""
    
    # Create logs directory
    log_path = Path(log_dir)
    log_path.mkdir(exist_ok=True)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level.upper()))
    
    # Clear existing handlers
    root_logger.handlers.clear()
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    
    if enable_json:
        console_formatter = JSONFormatter()
    else:
        console_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)
    
    # File handlers
    if enable_file_rotation:
        # Application logs with rotation
        app_handler = logging.handlers.RotatingFileHandler(
            log_path / "app.log",
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        app_handler.setLevel(logging.DEBUG)
        
        # Error logs with rotation
        error_handler = logging.handlers.RotatingFileHandler(
            log_path / "error.log",
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        error_handler.setLevel(logging.ERROR)
        
    else:
        # Simple file handlers
        app_handler = logging.FileHandler(log_path / "app.log")
        app_handler.setLevel(logging.DEBUG)
        
        error_handler = logging.FileHandler(log_path / "error.log")
        error_handler.setLevel(logging.ERROR)
    
    # Set formatters
    if enable_json:
        file_formatter = JSONFormatter()
    else:
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(module)s:%(lineno)d - %(message)s'
        )
    
    app_handler.setFormatter(file_formatter)
    error_handler.setFormatter(file_formatter)
    
    root_logger.addHandler(app_handler)
    root_logger.addHandler(error_handler)
    
    # Configure third-party loggers
    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    logging.getLogger("alembic").setLevel(logging.WARNING)
    
    # Application loggers
    logging.getLogger("printoptimizer").setLevel(logging.DEBUG)
    
    return root_logger