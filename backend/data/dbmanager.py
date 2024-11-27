import os
import sqlite3, logging
from datetime import datetime
from models.task import Task
from backend.data.dbSetUp import initialize_database

class DatabaseManager:
    def __init__(self, logger: logging.Logger, db_path=None):
        self.logger = logger
        self.db_path = os.path.join(os.path.dirname(__file__), "db/task_log.db") if db_path is None else db_path
        self._ensure_db_folder_exists()
        if not self._database_exists():
            self.logger.debug("initializing database")
            initialize_database(self.db_path)

    def _ensure_db_folder_exists(self):
        """
        Ensures that the database folder exists.
        """
        db_folder = os.path.dirname(self.db_path)
        if not os.path.exists(db_folder):
            os.makedirs(db_folder)
            self.logger.debug(f"Created database folder at {db_folder}")


    def _connect(self):
                """
                Establishes a database connection using the context manager.
                """
                try:
                    return sqlite3.connect(self.db_path)
                except sqlite3.Error as e:
                    self.logger.error(f"An error occurred while connecting to the database: {e}")
                    return None
    
    
    def get_connection(self):
        """
        Returns a connection object.
        """
        return self._connect() 
    

    def _database_exists(self):
        """
        Checks if the database file exists and has the necessary tables.
        """
        try:
            with self._connect() as connection:
                cursor = connection.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='TaskLog';")
                return cursor.fetchone() is not None
        except sqlite3.Error:
            return False 
        

    def add_task_entry(self, task: Task):
        """
        Adds a new task entry to the TaskLog table.
        """
        connection = self._connect()
        if not connection:
            return False

        try:
            task.validate()
            with connection:
                cursor = connection.cursor()
                cursor.execute('''
                    INSERT INTO TaskLog (date, task, category, time_investment, start_time, end_time, 
                                            immediate_benefit, future_impact, personal_fulfillment, progress, 
                                            output_score, roi, notes)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (task.to_tuple()))
                return cursor.lastrowid # Returns the last row id as a success indicator
        except sqlite3.Error as e:
            self.logger.error(f"An error occurred while adding the task entry: {e}")
            return False