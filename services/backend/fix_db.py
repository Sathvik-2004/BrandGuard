import sqlite3
import os

# Connect and check schema
conn = sqlite3.connect('dev.db')
cursor = conn.cursor()

# Check if cluster_id column exists
cursor.execute('PRAGMA table_info(mentions)')
columns = [column[1] for column in cursor.fetchall()]
print('Existing columns in mentions table:', columns)

if 'cluster_id' not in columns:
    print('Adding cluster_id column...')
    cursor.execute('ALTER TABLE mentions ADD COLUMN cluster_id INTEGER')
    conn.commit()
    print('cluster_id column added!')
    
# Check if alerts table exists
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='alerts'")
alerts_exists = cursor.fetchone()
if not alerts_exists:
    print('Creating alerts table...')
    cursor.execute('''
        CREATE TABLE alerts (
            id INTEGER PRIMARY KEY,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            alert_type VARCHAR(50),
            message TEXT,
            resolved BOOLEAN DEFAULT 0
        )
    ''')
    conn.commit()
    print('alerts table created!')

# Verify final schema
cursor.execute('PRAGMA table_info(mentions)')
columns = [column[1] for column in cursor.fetchall()]
print('Final mentions columns:', columns)

cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [table[0] for table in cursor.fetchall()]
print('Final tables:', tables)

conn.close()
print('Database schema updated successfully!')