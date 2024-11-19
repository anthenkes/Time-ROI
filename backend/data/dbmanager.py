import sqlite3, logging
from datetime import datetime
from dbSetUp import initialize_database

class DatabaseManager:
    def __init__(self, logger: logging.Logger, db_path="task_log.db"):
        self.logger = logger
        self.db_path = db_path
        if not self._database_exists():
            initialize_database()

    def _connect(self):
                """
                Establishes a database connection using the context manager.
                """
                try:
                    return sqlite3.connect(self.db_path)
                except sqlite3.Error as e:
                    self.logger.error(f"An error occurred while connecting to the database: {e}")
                    return None
    

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
        

    def add_task_entry(self, date, task, category, time_investment, start_time, end_time, 
                        immediate_benefit, future_impact, personal_fulfillment, progress, output_score, roi, notes=""):
        """
        Adds a new task entry to the TaskLog table.
        """
        connection = self._connect()
        if not connection:
            return False

        try:
            with connection:
                cursor = connection.cursor()
                cursor.execute('''
                    INSERT INTO TaskLog (date, task, category, time_investment, start_time, end_time, 
                                            immediate_benefit, future_impact, personal_fulfillment, progress, 
                                            output_score, roi, notes)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (date, task, category, time_investment, start_time, end_time, 
                        immediate_benefit, future_impact, personal_fulfillment, progress, output_score, roi, notes))
        except sqlite3.Error as e:
            self.logger.error(f"An error occurred while adding the task entry: {e}")
            return False