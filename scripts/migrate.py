"""
Database migration management script
"""
import subprocess
import sys
import os
from pathlib import Path

def run_command(command: str, description: str = ""):
    """Run shell command and handle errors"""
    print(f"Running: {description or command}")
    result = subprocess.run(command.split(), capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        sys.exit(1)
    
    if result.stdout:
        print(result.stdout)
    
    return result

def init_alembic():
    """Initialize Alembic if not already initialized"""
    alembic_dir = Path("alembic")
    if not alembic_dir.exists():
        print("Initializing Alembic...")
        run_command("alembic init alembic", "Initialize Alembic")
        print("✓ Alembic initialized")
    else:
        print("✓ Alembic already initialized")

def create_migration(message: str = "Auto migration"):
    """Create new migration"""
    run_command(f"alembic revision --autogenerate -m '{message}'", f"Create migration: {message}")
    print(f"✓ Migration created: {message}")

def upgrade_database(revision: str = "head"):
    """Upgrade database to specific revision"""
    run_command(f"alembic upgrade {revision}", f"Upgrade database to {revision}")
    print(f"✓ Database upgraded to {revision}")

def downgrade_database(revision: str):
    """Downgrade database to specific revision"""
    run_command(f"alembic downgrade {revision}", f"Downgrade database to {revision}")
    print(f"✓ Database downgraded to {revision}")

def show_current_revision():
    """Show current database revision"""
    run_command("alembic current", "Show current revision")

def show_migration_history():
    """Show migration history"""
    run_command("alembic history", "Show migration history")

def main():
    """Main migration management function"""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python scripts/migrate.py init                 # Initialize Alembic")
        print("  python scripts/migrate.py create [message]     # Create new migration")
        print("  python scripts/migrate.py upgrade [revision]   # Upgrade database")
        print("  python scripts/migrate.py downgrade <revision> # Downgrade database")
        print("  python scripts/migrate.py current              # Show current revision")
        print("  python scripts/migrate.py history              # Show migration history")
        sys.exit(1)
    
    command = sys.argv[1]
    
    try:
        if command == "init":
            init_alembic()
            
        elif command == "create":
            message = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else "Auto migration"
            create_migration(message)
            
        elif command == "upgrade":
            revision = sys.argv[2] if len(sys.argv) > 2 else "head"
            upgrade_database(revision)
            
        elif command == "downgrade":
            if len(sys.argv) < 3:
                print("Error: Downgrade requires a revision")
                sys.exit(1)
            revision = sys.argv[2]
            downgrade_database(revision)
            
        elif command == "current":
            show_current_revision()
            
        elif command == "history":
            show_migration_history()
            
        else:
            print(f"Unknown command: {command}")
            sys.exit(1)
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()