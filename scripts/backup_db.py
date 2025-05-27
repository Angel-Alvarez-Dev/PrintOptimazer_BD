# scripts/backup_db.py
"""
Database backup script
"""
import subprocess
import os
from datetime import datetime
from pathlib import Path
from app.core.config import settings

def create_backup():
    """Create database backup"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = Path("backups")
    backup_dir.mkdir(exist_ok=True)
    
    if "postgresql" in settings.DATABASE_URL:
        # PostgreSQL backup
        backup_file = backup_dir / f"printoptimizer_backup_{timestamp}.sql"
        
        # Extract connection details from DATABASE_URL
        # postgresql://user:pass@host:port/db
        url_parts = settings.DATABASE_URL.replace("postgresql://", "").split("/")
        db_name = url_parts[1]
        user_host = url_parts[0].split("@")
        user_pass = user_host[0].split(":")
        host_port = user_host[1].split(":")
        
        username = user_pass[0]
        password = user_pass[1] if len(user_pass) > 1 else ""
        host = host_port[0]
        port = host_port[1] if len(host_port) > 1 else "5432"
        
        # Set password environment variable
        env = os.environ.copy()
        env["PGPASSWORD"] = password
        
        cmd = [
            "pg_dump",
            "-h", host,
            "-p", port,
            "-U", username,
            "-d", db_name,
            "-f", str(backup_file),
            "--verbose"
        ]
        
        result = subprocess.run(cmd, env=env, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✓ Database backup created: {backup_file}")
            return str(backup_file)
        else:
            print(f"✗ Backup failed: {result.stderr}")
            return None
            
    elif "sqlite" in settings.DATABASE_URL:
        # SQLite backup
        db_file = settings.DATABASE_URL.replace("sqlite:///", "")
        backup_file = backup_dir / f"printoptimizer_backup_{timestamp}.db"
        
        import shutil
        shutil.copy2(db_file, backup_file)
        print(f"✓ Database backup created: {backup_file}")
        return str(backup_file)
    
    else:
        print("✗ Unsupported database type for backup")
        return None

def restore_backup(backup_file: str):
    """Restore database from backup"""
    if not os.path.exists(backup_file):
        print(f"✗ Backup file not found: {backup_file}")
        return False
    
    if "postgresql" in settings.DATABASE_URL and backup_file.endswith(".sql"):
        # PostgreSQL restore
        # Implementation similar to backup but using psql
        print("PostgreSQL restore not implemented yet")
        return False
        
    elif "sqlite" in settings.DATABASE_URL and backup_file.endswith(".db"):
        # SQLite restore
        import shutil
        db_file = settings.DATABASE_URL.replace("sqlite:///", "")
        shutil.copy2(backup_file, db_file)
        print(f"✓ Database restored from: {backup_file}")
        return True
    
    else:
        print("✗ Incompatible backup file or database type")
        return False

def list_backups():
    """List available backups"""
    backup_dir = Path("backups")
    if not backup_dir.exists():
        print("No backups found")
        return []
    
    backups = list(backup_dir.glob("printoptimizer_backup_*"))
    backups.sort(key=lambda x: x.stat().st_mtime, reverse=True)
    
    print("Available backups:")
    for backup in backups:
        timestamp = datetime.fromtimestamp(backup.stat().st_mtime)
        size = backup.stat().st_size / 1024 / 1024  # MB
        print(f"  {backup.name} ({size:.2f} MB) - {timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
    
    return [str(b) for b in backups]

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python scripts/backup_db.py create")
        print("  python scripts/backup_db.py restore <backup_file>")
        print("  python scripts/backup_db.py list")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "create":
        create_backup()
    elif command == "restore":
        if len(sys.argv) < 3:
            print("Error: Please specify backup file")
            sys.exit(1)
        restore_backup(sys.argv[2])
    elif command == "list":
        list_backups()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)