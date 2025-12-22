"""Migration script to add user_narration column to projects table."""
import os
from sqlalchemy import create_engine, text

# Database connection
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "docker")
DB_PASSWORD = os.getenv("DB_PASSWORD", "docker")
DB_NAME = os.getenv("DB_NAME", "postgres")
DB_PORT = os.getenv("DB_PORT", "5433")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

def add_user_narration_column():
    """Add user_narration column to projects table if it doesn't exist."""
    engine = create_engine(DATABASE_URL)
    
    with engine.connect() as conn:
        # Check if column exists
        check_query = text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='projects' 
            AND column_name='user_narration'
        """)
        
        result = conn.execute(check_query)
        exists = result.fetchone()
        
        if exists:
            print("✅ Column 'user_narration' already exists in projects table")
        else:
            print("Adding 'user_narration' column to projects table...")
            
            # Add the column
            alter_query = text("""
                ALTER TABLE projects 
                ADD COLUMN user_narration TEXT
            """)
            
            conn.execute(alter_query)
            conn.commit()
            
            print("✅ Successfully added 'user_narration' column to projects table")
    
    engine.dispose()

if __name__ == "__main__":
    print("\n" + "="*60)
    print("DATABASE MIGRATION: Add user_narration column")
    print("="*60 + "\n")
    
    try:
        add_user_narration_column()
        print("\n✅ Migration completed successfully!\n")
    except Exception as e:
        print(f"\n❌ Migration failed: {e}\n")
        raise
