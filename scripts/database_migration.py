## 6. scripts/database_migration.py - Database Management
#!/usr/bin/env python3
"""
Database Migration and Management Script
Handles database setup, migrations, and data management
"""

import asyncio
import asyncpg
import os
from alembic import command
from alembic.config import Config

class DatabaseManager:
    def __init__(self):
        self.db_url = os.getenv('DATABASE_URL')
        if not self.db_url:
            raise ValueError("DATABASE_URL environment variable not set")
    
    async def create_database(self, db_name):
        """Create a new database"""
        # Connect to postgres database to create new database
        conn = await asyncpg.connect(self.db_url.replace('/patent_agent', '/postgres'))
        try:
            await conn.execute(f'CREATE DATABASE {db_name}')
            print(f"✅ Database '{db_name}' created successfully")
        except asyncpg.DuplicateDatabaseError:
            print(f"ℹ️ Database '{db_name}' already exists")
        finally:
            await conn.close()
    
    async def drop_database(self, db_name):
        """Drop a database"""
        conn = await asyncpg.connect(self.db_url.replace('/patent_agent', '/postgres'))
        try:
            await conn.execute(f'DROP DATABASE IF EXISTS {db_name}')
            print(f"✅ Database '{db_name}' dropped successfully")
        finally:
            await conn.close()
    
    def run_migrations(self):
        """Run database migrations"""
        alembic_cfg = Config("alembic.ini")
        command.upgrade(alembic_cfg, "head")
        print("✅ Database migrations completed")
    
    def create_migration(self, message):
        """Create a new migration"""
        alembic_cfg = Config("alembic.ini")
        command.revision(alembic_cfg, message=message, autogenerate=True)
        print(f"✅ Migration '{message}' created")
    
    async def seed_data(self):
        """Seed database with initial data"""
        conn = await asyncpg.connect(self.db_url)
        try:
            # Insert sample patent classifications
            await conn.execute("""
                INSERT INTO patent_classifications (code, description) VALUES
                ('G06F', 'Electric digital data processing'),
                ('G06N', 'Computing arrangements based on specific computational models'),
                ('H04L', 'Transmission of digital information')
                ON CONFLICT (code) DO NOTHING
            """)
            
            # Insert sample user roles
            await conn.execute("""
                INSERT INTO user_roles (name, permissions) VALUES
                ('admin', '["read", "write", "delete", "admin"]'),
                ('user', '["read", "write"]'),
                ('readonly', '["read"]')
                ON CONFLICT (name) DO NOTHING
            """)
            
            print("✅ Database seeded with initial data")
        finally:
            await conn.close()

async def main():
    """Main function for database management"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Database Management Tool")
    parser.add_argument('action', choices=['create', 'drop', 'migrate', 'seed', 'reset'])
    parser.add_argument('--db-name', default='patent_agent')
    parser.add_argument('--message', help='Migration message')
    
    args = parser.parse_args()
    
    db_manager = DatabaseManager()
    
    if args.action == 'create':
        await db_manager.create_database(args.db_name)
    elif args.action == 'drop':
        await db_manager.drop_database(args.db_name)
    elif args.action == 'migrate':
        if args.message:
            db_manager.create_migration(args.message)
        else:
            db_manager.run_migrations()
    elif args.action == 'seed':
        await db_manager.seed_data()
    elif args.action == 'reset':
        await db_manager.drop_database(args.db_name)
        await db_manager.create_database(args.db_name)
        db_manager.run_migrations()
        await db_manager.seed_data()
        print("🔄 Database reset completed")

if __name__ == "__main__":
    asyncio.run(main())
