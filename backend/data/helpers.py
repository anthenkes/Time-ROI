import shutil,sqlite3, logging

from dbmanager import DatabaseManager

#TODO: Change the methods below to have try blocks so
# errors can be logged and properly handled
class DatabaseHelper(DatabaseManager):
    def __init__(self, logger: logging.Logger, db_path="task_log.db"):
        super().__init__(logger, db_path)

    def add_column_if_not_exists(self, table_name, column_name, column_type):
        with self._connect() as connection:
            cursor = connection.cursor()

            # Check if the column already exists
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = [column[1] for column in cursor.fetchall()]

            # If the column does not exist, add it
            if column_name not in columns:
                cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}")
                self.logger.info(f"Added column '{column_name}' to '{table_name}' table.")

    def migrate_to_new_table(self):
        '''#TODO: This is incomplete can essentially just makes a copy of the table'''
        with self._connect() as connection:
            cursor = connection.cursor()

            # Create the new table with updated schema
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS TaskLog_New (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT,
                    task TEXT,
                    category TEXT,
                    time_investment INTEGER,
                    start_time TEXT,
                    end_time TEXT,
                    immediate_benefit INTEGER,
                    future_impact INTEGER,
                    personal_fulfillment INTEGER,
                    progress INTEGER,
                    output_score REAL,
                    roi REAL,
                    notes TEXT,
                    new_column_name TEXT  -- Example of a new column
                )
            ''')

            # Copy data from old table to new table
            cursor.execute('''
                INSERT INTO TaskLog_New (id, date, task, category, time_investment, start_time, end_time,
                                         immediate_benefit, future_impact, personal_fulfillment, progress,
                                         output_score, roi, notes)
                SELECT id, date, task, category, time_investment, start_time, end_time,
                       immediate_benefit, future_impact, personal_fulfillment, progress,
                       output_score, roi, notes
                FROM TaskLog
            ''')

            # Drop the old table and rename the new table
            cursor.execute("DROP TABLE TaskLog")
            cursor.execute("ALTER TABLE TaskLog_New RENAME TO TaskLog")
            self.logger.debug("Migrated data to the new schema successfully.")

    def get_database_version(self):
        with self._connect() as connection:
            cursor = connection.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS Meta (version INTEGER)")
            cursor.execute("SELECT version FROM Meta")
            result = cursor.fetchone()
            return result[0] if result else 0
        
    #
    def set_database_version(self, version):
        '''New version number logged as crtical so that it is easy to see'''
        with self._connect() as connection:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM Meta")  # Clear existing version
            cursor.execute("INSERT INTO Meta (version) VALUES (?)", (version,))
            self.logger.critical(f"Database version set to {version}.")

    def backup_database(self):
        try:
            shutil.copy(self.db_path, "task_log_backup.db")
            self.logger.info("Database backup created successfully.")
        except IOError as e:
            self.logger.error(f"Error backing up database: {e}")

    def restore_database(self, backup_path="task_log_backup.db"):
        try:
            shutil.copy(backup_path, self.db_path)
            self.logger.info(f"Database restored successfully from {backup_path}.")
        except IOError as e:
            self.logger.error(f"Error restoring database: {e}")

    #TODO: Add functionality to accept type of data 
    # Can make it so that this function is very versitile for updating the database as the code requirements change
    def migrate_database(self, new_column_name=None):
        current_version = self.get_database_version()
        self.backup_database()

        try:
            if current_version < 1:
                if new_column_name:
                    self.add_column_if_not_exists("TaskLog", new_column_name, "TEXT")
                self.set_database_version(1)
                self.logger.info("Migrated to version 1.")

            if current_version < 2:
                self.migrate_to_new_table()
                self.set_database_version(2)
                self.logger.info("Migrated to version 2.")
        except Exception as e:
            self.logger.error(f"Migration failed: {e}")
            self.restore_database()
            self.logger.info("Database restored to previous state due to migration failure.")