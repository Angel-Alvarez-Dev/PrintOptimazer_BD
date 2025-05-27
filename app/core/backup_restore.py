# app/core/backup_restore.py
"""
Production backup and restore system
"""
import os
import subprocess
import shutil
import gzip
import boto3
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

class BackupManager:
    """Comprehensive backup management system"""
    
    def __init__(self):
        self.backup_dir = Path("backups")
        self.backup_dir.mkdir(exist_ok=True)
        
        # S3 client for cloud backups (optional)
        self.s3_client = None
        if hasattr(settings, 'AWS_ACCESS_KEY_ID'):
            self.s3_client = boto3.client(
                's3',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_REGION
            )
    
    def create_database_backup(self) -> Optional[str]:
        """Create complete database backup"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"db_backup_{timestamp}.sql.gz"
        backup_path = self.backup_dir / backup_filename
        
        try:
            # Extract database connection info
            db_url = settings.DATABASE_URL
            if "postgresql://" in db_url:
                # Parse PostgreSQL URL
                url_parts = db_url.replace("postgresql://", "").split("/")
                db_name = url_parts[1].split("?")[0]  # Remove query params if any
                user_host = url_parts[0].split("@")
                user_pass = user_host[0].split(":")
                host_port = user_host[1].split(":")
                
                username = user_pass[0]
                password = user_pass[1] if len(user_pass) > 1 else ""
                host = host_port[0]
                port = host_port[1] if len(host_port) > 1 else "5432"
                
                # Set environment for pg_dump
                env = os.environ.copy()
                env["PGPASSWORD"] = password
                
                # Create backup command
                cmd = [
                    "pg_dump",
                    "-h", host,
                    "-p", port,
                    "-U", username,
                    "-d", db_name,
                    "--verbose",
                    "--no-password",
                    "--format=custom",
                    "--compress=9"
                ]
                
                # Execute backup
                with open(backup_path.with_suffix('.sql'), 'wb') as f:
                    result = subprocess.run(cmd, stdout=f, stderr=subprocess.PIPE, env=env)
                
                if result.returncode == 0:
                    # Compress backup
                    with open(backup_path.with_suffix('.sql'), 'rb') as f_in:
                        with gzip.open(backup_path, 'wb') as f_out:
                            shutil.copyfileobj(f_in, f_out)
                    
                    # Remove uncompressed file
                    backup_path.with_suffix('.sql').unlink()
                    
                    logger.info(f"Database backup created: {backup_path}")
                    
                    # Upload to S3 if configured
                    if self.s3_client:
                        self.upload_to_s3(backup_path, f"database-backups/{backup_filename}")
                    
                    return str(backup_path)
                else:
                    logger.error(f"Database backup failed: {result.stderr.decode()}")
                    return None
            
            elif "sqlite:///" in db_url:
                # SQLite backup
                db_file = db_url.replace("sqlite:///", "")
                if Path(db_file).exists():
                    with open(db_file, 'rb') as f_in:
                        with gzip.open(backup_path, 'wb') as f_out:
                            shutil.copyfileobj(f_in, f_out)
                    
                    logger.info(f"SQLite backup created: {backup_path}")
                    return str(backup_path)
                else:
                    logger.error(f"SQLite database file not found: {db_file}")
                    return None
            
        except Exception as e:
            logger.error(f"Database backup failed: {e}")
            return None
    
    def create_files_backup(self) -> Optional[str]:
        """Create backup of uploaded files"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"files_backup_{timestamp}.tar.gz"
        backup_path = self.backup_dir / backup_filename
        
        try:
            uploads_dir = Path("uploads")
            if uploads_dir.exists():
                # Create tar.gz archive
                cmd = [
                    "tar", "-czf", str(backup_path),
                    "-C", str(uploads_dir.parent),
                    str(uploads_dir.name)
                ]
                
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                if result.returncode == 0:
                    logger.info(f"Files backup created: {backup_path}")
                    
                    # Upload to S3 if configured
                    if self.s3_client:
                        self.upload_to_s3(backup_path, f"files-backups/{backup_filename}")
                    
                    return str(backup_path)
                else:
                    logger.error(f"Files backup failed: {result.stderr}")
                    return None
            else:
                logger.warning("Uploads directory not found, skipping files backup")
                return None
                
        except Exception as e:
            logger.error(f"Files backup failed: {e}")
            return None
    
    def create_full_backup(self) -> Dict[str, Optional[str]]:
        """Create complete system backup"""
        logger.info("Starting full system backup...")
        
        results = {
            "database": self.create_database_backup(),
            "files": self.create_files_backup(),
            "timestamp": datetime.now().isoformat()
        }
        
        # Create manifest file
        manifest_path = self.backup_dir / f"backup_manifest_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        import json
        with open(manifest_path, 'w') as f:
            json.dump(results, f, indent=2)
        
        logger.info(f"Full backup completed. Manifest: {manifest_path}")
        return results
    
    def upload_to_s3(self, file_path: Path, s3_key: str):
        """Upload backup to S3"""
        try:
            if self.s3_client and hasattr(settings, 'BACKUP_S3_BUCKET'):
                self.s3_client.upload_file(
                    str(file_path),
                    settings.BACKUP_S3_BUCKET,
                    s3_key
                )
                logger.info(f"Backup uploaded to S3: s3://{settings.BACKUP_S3_BUCKET}/{s3_key}")
        except Exception as e:
            logger.error(f"S3 upload failed: {e}")
    
    def restore_database_backup(self, backup_path: str) -> bool:
        """Restore database from backup"""
        try:
            backup_path = Path(backup_path)
            if not backup_path.exists():
                logger.error(f"Backup file not found: {backup_path}")
                return False
            
            # Decompress if needed
            if backup_path.suffix == '.gz':
                decompressed_path = backup_path.with_suffix('')
                with gzip.open(backup_path, 'rb') as f_in:
                    with open(decompressed_path, 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
                backup_path = decompressed_path
            
            # Restore based on database type
            db_url = settings.DATABASE_URL
            
            if "postgresql://" in db_url:
                # PostgreSQL restore
                # Parse connection details...
                # Implementation similar to backup but using pg_restore
                logger.info("PostgreSQL restore not fully implemented")
                return False
                
            elif "sqlite:///" in db_url:
                # SQLite restore
                db_file = db_url.replace("sqlite:///", "")
                shutil.copy2(backup_path, db_file)
                logger.info(f"SQLite database restored from {backup_path}")
                return True
            
        except Exception as e:
            logger.error(f"Database restore failed: {e}")
            return False
    
    def cleanup_old_backups(self, keep_days: int = 30):
        """Clean up backups older than specified days"""
        cutoff_date = datetime.now() - timedelta(days=keep_days)
        
        try:
            for backup_file in self.backup_dir.glob("*backup*"):
                if backup_file.stat().st_mtime < cutoff_date.timestamp():
                    backup_file.unlink()
                    logger.info(f"Deleted old backup: {backup_file}")
        except Exception as e:
            logger.error(f"Backup cleanup failed: {e}")
    
    def list_backups(self) -> List[Dict[str, any]]:
        """List available backups"""
        backups = []
        
        for backup_file in self.backup_dir.glob("*backup*"):
            stat = backup_file.stat()
            backups.append({
                "filename": backup_file.name,
                "path": str(backup_file),
                "size_mb": stat.st_size / 1024 / 1024,
                "created": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "type": "database" if "db_backup" in backup_file.name else "files"
            })
        
        return sorted(backups, key=lambda x: x["created"], reverse=True)