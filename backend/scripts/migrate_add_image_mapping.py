#!/usr/bin/env python3
"""
Database migration script: Add image_mapping column to test_session table

This script adds the image_mapping column to existing test_session records.
For SQLite databases, we need to handle the migration carefully.

Usage:
    python backend/scripts/migrate_add_image_mapping.py
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app import create_app
from models import db

def migrate():
    """Add image_mapping column to test_session table."""
    app = create_app()

    with app.app_context():
        # Check if we're using SQLite
        if 'sqlite' in app.config['SQLALCHEMY_DATABASE_URI']:
            print("Detected SQLite database")

            # SQLite doesn't support ALTER COLUMN, but db.create_all() will
            # add the new column if it doesn't exist
            try:
                # Check if column exists
                result = db.session.execute(db.text("PRAGMA table_info(test_session)"))
                columns = [row[1] for row in result]

                if 'image_mapping' in columns:
                    print("✓ Column 'image_mapping' already exists. No migration needed.")
                    return

                print("Adding 'image_mapping' column to test_session table...")

                # For SQLite, we use ALTER TABLE ADD COLUMN
                db.session.execute(db.text(
                    "ALTER TABLE test_session ADD COLUMN image_mapping TEXT"
                ))
                db.session.commit()

                print("✓ Successfully added 'image_mapping' column")
                print("\nNote: Existing sessions will have NULL image_mapping.")
                print("They will continue to use the old on-the-fly generation system.")

            except Exception as e:
                print(f"✗ Migration failed: {e}")
                db.session.rollback()
                raise
        else:
            # For PostgreSQL or MySQL
            print("Detected non-SQLite database")
            print("Please run the appropriate ALTER TABLE command for your database:")
            print("\nPostgreSQL:")
            print("  ALTER TABLE test_session ADD COLUMN image_mapping JSONB;")
            print("\nMySQL:")
            print("  ALTER TABLE test_session ADD COLUMN image_mapping JSON;")

            # Attempt to run it anyway
            try:
                db.session.execute(db.text(
                    "ALTER TABLE test_session ADD COLUMN image_mapping JSON"
                ))
                db.session.commit()
                print("\n✓ Successfully added 'image_mapping' column")
            except Exception as e:
                print(f"\n✗ Migration failed: {e}")
                print("You may need to run the migration manually.")
                db.session.rollback()


if __name__ == '__main__':
    print("=" * 60)
    print("Database Migration: Add image_mapping to test_session")
    print("=" * 60)
    print()

    migrate()

    print()
    print("=" * 60)
    print("Migration complete")
    print("=" * 60)
