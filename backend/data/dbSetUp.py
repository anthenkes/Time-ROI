import sqlite3
from datetime import datetime

# Function to initialize the SQLite database with a given path
def initialize_database(db_path):
    with sqlite3.connect(db_path) as connection:
        cursor = connection.cursor()

        # Create table with specified columns
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS TaskLog (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,                          -- Stores date as a string in ISO format (YYYY-MM-DD)
                task TEXT,                          -- Task name or description
                category TEXT,                      -- Category of the task (e.g., "Learning", "Health", etc.)
                time_investment INTEGER,            -- Time investment in minutes
                start_time TEXT,                    -- Start time of the task (for future time-frame feature)
                end_time TEXT,                      -- End time of the task (for future time-frame feature)
                immediate_benefit INTEGER,          -- Score for immediate benefit (1-5 scale)
                future_impact INTEGER,              -- Score for future impact (1-5 scale)
                personal_fulfillment INTEGER,       -- Score for personal fulfillment (1-5 scale)
                progress INTEGER,                   -- Score for progress (1-5 scale)
                output_score REAL,                  -- Calculated output score
                roi REAL,                           -- Calculated return on investment (ROI)
                notes TEXT                          -- Optional notes about the task
            )
        ''')
