#!/usr/bin/env python3
"""
Clear Database Script
This script safely clears the database to prepare for fresh data collection.
"""

import sqlite3
import os
from datetime import datetime

def clear_database():
    """Clear all tweets from the database"""
    db_path = "backend/tweets.db"
    
    print("🗑️ Database Cleanup Script")
    print("="*50)
    
    # Check if database exists
    if not os.path.exists(db_path):
        print(f"❌ Database not found at: {db_path}")
        return False
    
    # Get current database stats
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get current stats
        cursor.execute("SELECT COUNT(*) FROM tweets")
        current_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(DISTINCT username) FROM tweets")
        unique_users = cursor.fetchone()[0]
        
        print(f"📊 Current Database Stats:")
        print(f"   Total tweets: {current_count:,}")
        print(f"   Unique users: {unique_users}")
        print(f"   Database size: {os.path.getsize(db_path) / (1024*1024):.2f} MB")
        
        # Confirm deletion
        print(f"\n⚠️  WARNING: This will delete ALL tweets from the database!")
        confirm = input("Are you sure you want to continue? (yes/no): ").lower().strip()
        
        if confirm != 'yes':
            print("❌ Operation cancelled.")
            return False
        
        # Clear all tweets
        print(f"\n🗑️ Clearing database...")
        cursor.execute("DELETE FROM tweets")
        conn.commit()
        
        # Verify deletion
        cursor.execute("SELECT COUNT(*) FROM tweets")
        new_count = cursor.fetchone()[0]
        
        if new_count == 0:
            print(f"✅ Database cleared successfully!")
            print(f"   Remaining tweets: {new_count}")
            
            # Create backup of old database
            backup_path = f"backend/tweets_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
            import shutil
            shutil.copy2(db_path, backup_path)
            print(f"📦 Backup created: {backup_path}")
            
            return True
        else:
            print(f"❌ Error: {new_count} tweets still remain")
            return False
            
    except Exception as e:
        print(f"❌ Error clearing database: {e}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    clear_database()
