# scripts/production_maintenance.py
"""
Production maintenance tasks and health monitoring
"""
import asyncio
import psutil
import subprocess
import requests
from datetime import datetime, timedelta
from pathlib import Path
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ProductionMaintenance:
    """Production maintenance and monitoring"""
    
    def __init__(self, config_file="maintenance_config.json"):
        self.config = self.load_config(config_file)
        self.alerts = []
    
    def load_config(self, config_file):
        """Load maintenance configuration"""
        default_config = {
            "api_url": "http://localhost:8000",
            "database_url": "postgresql://user:pass@localhost:5432/db",
            "redis_url": "redis://localhost:6379/0",
            "email": {
                "smtp_server": "smtp.gmail.com",
                "smtp_port": 587,
                "username": "alerts@printoptimizer.com",
                "password": "app_password",
                "recipients": ["admin@printoptimizer.com"]
            },
            "thresholds": {
                "cpu_percent": 80,
                "memory_percent": 85,
                "disk_percent": 90,
                "response_time_ms": 2000,
                "error_rate_percent": 5
            },
            "maintenance": {
                "log_retention_days": 30,
                "backup_retention_days": 30,
                "temp_cleanup_days": 7,
                "analytics_retention_days": 90
            }
        }
        
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
            return {**default_config, **config}
        except FileNotFoundError:
            logger.warning(f"Config file {config_file} not found, using defaults")
            return default_config
    
    def check_system_health(self):
        """Comprehensive system health check"""
        health_report = {
            "timestamp": datetime.now().isoformat(),
            "status": "healthy",
            "checks": {}
        }
        
        # System resources
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        health_report["checks"]["system"] = {
            "cpu_percent": cpu_percent,
            "memory_percent": memory.percent,
            "disk_percent": (disk.used / disk.total) * 100,
            "load_average": psutil.getloadavg() if hasattr(psutil, 'getloadavg') else None
        }
        
        # Check thresholds
        if cpu_percent > self.config["thresholds"]["cpu_percent"]:
            health_report["status"] = "degraded"
            self.alerts.append(f"High CPU usage: {cpu_percent:.1f}%")
        
        if memory.percent > self.config["thresholds"]["memory_percent"]:
            health_report["status"] = "degraded"
            self.alerts.append(f"High memory usage: {memory.percent:.1f}%")
        
        disk_percent = (disk.used / disk.total) * 100
        if disk_percent > self.config["thresholds"]["disk_percent"]:
            health_report["status"] = "critical"
            self.alerts.append(f"High disk usage: {disk_percent:.1f}%")
        
        # Process checks
        health_report["checks"]["processes"] = self.check_processes()
        
        # Network checks
        health_report["checks"]["network"] = self.check_network_connectivity()
        
        # Database checks
        health_report["checks"]["database"] = self.check_database_health()
        
        # Application checks
        health_report["checks"]["application"] = self.check_application_health()
        
        return health_report
    
    def check_processes(self):
        """Check critical processes"""
        critical_processes = ["postgres", "redis-server", "nginx", "gunicorn"]
        process_status = {}
        
        for proc_name in critical_processes:
            try:
                processes = [p for p in psutil.process_iter(['pid', 'name']) 
                           if proc_name in p.info['name'].lower()]
                process_status[proc_name] = {
                    "running": len(processes) > 0,
                    "count": len(processes),
                    "pids": [p.info['pid'] for p in processes]
                }
                
                if not processes:
                    self.alerts.append(f"Critical process not running: {proc_name}")
                    
            except Exception as e:
                process_status[proc_name] = {"error": str(e)}
        
        return process_status
    
    def check_network_connectivity(self):
        """Check network connectivity"""
        network_checks = {
            "external_dns": self.ping_host("8.8.8.8"),
            "external_web": self.ping_host("google.com"),
            "database_port": self.check_port("localhost", 5432),
            "redis_port": self.check_port("localhost", 6379)
        }
        
        return network_checks
    
    def ping_host(self, host):
        """Ping a host to check connectivity"""
        try:
            result = subprocess.run(['ping', '-c', '1', host], 
                                  capture_output=True, timeout=5)
            return {"reachable": result.returncode == 0}
        except Exception as e:
            return {"reachable": False, "error": str(e)}
    
    def check_port(self, host, port):
        """Check if a port is open"""
        import socket
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex((host, port))
            sock.close()
            return {"open": result == 0}
        except Exception as e:
            return {"open": False, "error": str(e)}
    
    def check_database_health(self):
        """Check database health and performance"""
        try:
            # Simple connection test
            result = subprocess.run(
                ['psql', self.config['database_url'], '-c', 'SELECT 1;'],
                capture_output=True, timeout=10, text=True
            )
            
            if result.returncode == 0:
                # Advanced database checks
                db_checks = {
                    "connection": "ok",
                    "query_performance": self.check_slow_queries(),
                    "connection_count": self.get_db_connection_count(),
                    "database_size": self.get_database_size()
                }
            else:
                db_checks = {
                    "connection": "failed",
                    "error": result.stderr
                }
                self.alerts.append("Database connection failed")
            
            return db_checks
            
        except Exception as e:
            self.alerts.append(f"Database health check failed: {e}")
            return {"connection": "error", "error": str(e)}
    
    def check_slow_queries(self):
        """Check for slow database queries"""
        try:
            # This would query pg_stat_statements or similar
            # Simplified implementation
            return {"slow_queries_count": 0, "average_time": "< 100ms"}
        except Exception:
            return {"error": "Unable to check slow queries"}
    
    def get_db_connection_count(self):
        """Get current database connection count"""
        try:
            # Query to get connection count
            query = "SELECT count(*) FROM pg_stat_activity WHERE state = 'active';"
            result = subprocess.run(
                ['psql', self.config['database_url'], '-t', '-c', query],
                capture_output=True, text=True
            )
            
            if result.returncode == 0:
                return int(result.stdout.strip())
            else:
                return None
        except Exception:
            return None
    
    def get_database_size(self):
        """Get database size"""
        try:
            query = "SELECT pg_size_pretty(pg_database_size(current_database()));"
            result = subprocess.run(
                ['psql', self.config['database_url'], '-t', '-c', query],
                capture_output=True, text=True
            )
            
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                return None
        except Exception:
            return None
    
    def check_application_health(self):
        """Check application-specific health"""
        try:
            # API health check
            response = requests.get(f"{self.config['api_url']}/health", timeout=10)
            
            app_health = {
                "api_status": response.status_code,
                "api_response_time": response.elapsed.total_seconds() * 1000,
                "api_healthy": response.status_code == 200
            }
            
            if response.status_code != 200:
                self.alerts.append(f"API health check failed: HTTP {response.status_code}")
            
            if app_health["api_response_time"] > self.config["thresholds"]["response_time_ms"]:
                self.alerts.append(f"Slow API response: {app_health['api_response_time']:.0f}ms")
            
            # Check specific endpoints
            endpoints_to_check = [
                "/api/v1/auth/login",
                "/api/v1/projects/",
                "/api/v1/analytics/dashboard"
            ]
            
            endpoint_health = {}
            for endpoint in endpoints_to_check:
                try:
                    resp = requests.get(f"{self.config['api_url']}{endpoint}", timeout=5)
                    endpoint_health[endpoint] = {
                        "status": resp.status_code,
                        "response_time": resp.elapsed.total_seconds() * 1000
                    }
                except Exception as e:
                    endpoint_health[endpoint] = {"error": str(e)}
            
            app_health["endpoints"] = endpoint_health
            
            return app_health
            
        except Exception as e:
            self.alerts.append(f"Application health check failed: {e}")
            return {"error": str(e)}
    
    def perform_maintenance_tasks(self):
        """Perform routine maintenance tasks"""
        maintenance_results = {}
        
        # Clean up old logs
        maintenance_results["log_cleanup"] = self.cleanup_old_logs()
        
        # Clean up temporary files
        maintenance_results["temp_cleanup"] = self.cleanup_temp_files()
        
        # Rotate logs
        maintenance_results["log_rotation"] = self.rotate_logs()
        
        # Database maintenance
        maintenance_results["database_maintenance"] = self.database_maintenance()
        
        # Update system packages (careful in production)
        # maintenance_results["system_updates"] = self.check_system_updates()
        
        return maintenance_results
    
    def cleanup_old_logs(self):
        """Clean up old log files"""
        try:
            logs_dir = Path("logs")
            if not logs_dir.exists():
                return {"status": "skipped", "reason": "logs directory not found"}
            
            cutoff_time = time.time() - (self.config["maintenance"]["log_retention_days"] * 86400)
            cleaned_files = 0
            cleaned_size = 0
            
            for log_file in logs_dir.glob("*.log*"):
                if log_file.stat().st_mtime < cutoff_time:
                    file_size = log_file.stat().st_size
                    log_file.unlink()
                    cleaned_files += 1
                    cleaned_size += file_size
            
            return {
                "status": "completed",
                "files_cleaned": cleaned_files,
                "size_cleaned_mb": cleaned_size / 1024 / 1024
            }
            
        except Exception as e:
            return {"status": "failed", "error": str(e)}
    
    def cleanup_temp_files(self):
        """Clean up temporary files"""
        try:
            temp_dir = Path("uploads/temp")
            if not temp_dir.exists():
                return {"status": "skipped", "reason": "temp directory not found"}
            
            cutoff_time = time.time() - (self.config["maintenance"]["temp_cleanup_days"] * 86400)
            cleaned_files = 0
            cleaned_size = 0
            
            for temp_file in temp_dir.rglob("*"):
                if temp_file.is_file() and temp_file.stat().st_mtime < cutoff_time:
                    file_size = temp_file.stat().st_size
                    temp_file.unlink()
                    cleaned_files += 1
                    cleaned_size += file_size
            
            return {
                "status": "completed",
                "files_cleaned": cleaned_files,
                "size_cleaned_mb": cleaned_size / 1024 / 1024
            }
            
        except Exception as e:
            return {"status": "failed", "error": str(e)}
    
    def rotate_logs(self):
        """Rotate application logs"""
        try:
            # This would typically be handled by logrotate
            # Simple implementation for demonstration
            logs_dir = Path("logs")
            
            for log_file in logs_dir.glob("*.log"):
                if log_file.stat().st_size > 10 * 1024 * 1024:  # 10MB
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    rotated_name = f"{log_file.stem}_{timestamp}.log"
                    log_file.rename(logs_dir / rotated_name)
                    
                    # Create new empty log file
                    log_file.touch()
            
            return {"status": "completed"}
            
        except Exception as e:
            return {"status": "failed", "error": str(e)}
    
    def database_maintenance(self):
        """Perform database maintenance tasks"""
        try:
            maintenance_commands = [
                "VACUUM ANALYZE;",  # PostgreSQL maintenance
                "REINDEX DATABASE printoptimizer_db;"  # Rebuild indexes
            ]
            
            results = []
            for command in maintenance_commands:
                try:
                    result = subprocess.run(
                        ['psql', self.config['database_url'], '-c', command],
                        capture_output=True, text=True, timeout=300  # 5 minutes
                    )
                    
                    results.append({
                        "command": command,
                        "status": "success" if result.returncode == 0 else "failed",
                        "output": result.stdout or result.stderr
                    })
                    
                except subprocess.TimeoutExpired:
                    results.append({
                        "command": command,
                        "status": "timeout",
                        "error": "Command timed out after 5 minutes"
                    })
            
            return {"status": "completed", "commands": results}
            
        except Exception as e:
            return {"status": "failed", "error": str(e)}
    
    def send_health_report(self, health_report):
        """Send health report via email if issues found"""
        if not self.alerts:
            return
        
        try:
            msg = MIMEMultipart()
            msg['From'] = self.config["email"]["username"]
            msg['To'] = ", ".join(self.config["email"]["recipients"])
            msg['Subject'] = f"PrintOptimizer Health Alert - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            
            body = "PrintOptimizer Health Report\n"
            body += "=" * 40 + "\n\n"
            body += f"Status: {health_report['status'].upper()}\n"
            body += f"Timestamp: {health_report['timestamp']}\n\n"
            
            if self.alerts:
                body += "ALERTS:\n"
                for alert in self.alerts:
                    body += f"• {alert}\n"
                body += "\n"
            
            body += "System Status:\n"
            body += f"• CPU: {health_report['checks']['system']['cpu_percent']:.1f}%\n"
            body += f"• Memory: {health_report['checks']['system']['memory_percent']:.1f}%\n"
            body += f"• Disk: {health_report['checks']['system']['disk_percent']:.1f}%\n\n"
            
            body += "For detailed information, check the server logs.\n"
            
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP(
                self.config["email"]["smtp_server"],
                self.config["email"]["smtp_port"]
            )
            server.starttls()
            server.login(
                self.config["email"]["username"],
                self.config["email"]["password"]
            )
            
            text = msg.as_string()
            server.sendmail(
                self.config["email"]["username"],
                self.config["email"]["recipients"],
                text
            )
            server.quit()
            
            logger.info("Health report email sent successfully")
            
        except Exception as e:
            logger.error(f"Failed to send health report email: {e}")
    
    def run_full_maintenance(self):
        """Run complete maintenance cycle"""
        logger.info("Starting production maintenance cycle...")
        
        # Health check
        health_report = self.check_system_health()
        
        # Maintenance tasks
        maintenance_results = self.perform_maintenance_tasks()
        
        # Create combined report
        full_report = {
            "health": health_report,
            "maintenance": maintenance_results,
            "timestamp": datetime.now().isoformat()
        }
        
        # Save report
        report_file = Path("reports") / f"maintenance_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        report_file.parent.mkdir(exist_ok=True)
        
        with open(report_file, 'w') as f:
            json.dump(full_report, f, indent=2)
        
        # Send alerts if needed
        if self.alerts:
            self.send_health_report(health_report)
        
        logger.info(f"Maintenance cycle completed. Report saved: {report_file}")
        
        return full_report

if __name__ == "__main__":
    import time
    maintenance = ProductionMaintenance()
    maintenance.run_full_maintenance()