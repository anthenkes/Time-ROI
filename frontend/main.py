import logging
from PySide6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QFormLayout, QLineEdit, QPushButton, QSpinBox, QDoubleSpinBox, QDateEdit, QTimeEdit, QTextEdit, QMessageBox
from PySide6.QtCore import QDate, QTime, QTimer, Qt
from PySide6.QtGui import QKeySequence, QShortcut
from models.task import Task
from backend.data.dbmanager import DatabaseManager

class MainWindow(QMainWindow):
    def __init__(self, logger):
        super().__init__()

        self.logger = logger
        self.setWindowTitle("Task Entry Form")

        # Initialize DatabaseManager
        self.db_manager = DatabaseManager(logger)

        # Set the central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create a vertical layout
        main_layout = QVBoxLayout()

        # Create a label for toast notifications
        self.toast_label = QLabel("")
        self.toast_label.setStyleSheet("background-color: green; color: black;")
        self.toast_label.setVisible(False)
        main_layout.addWidget(self.toast_label)

        # Create a form layout
        form_layout = QFormLayout()

        # Create input fields
        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        form_layout.addRow("Date:", self.date_edit)

        self.task_edit = QLineEdit()
        self.task_edit.returnPressed.connect(self.submit_task)  # Submit on Enter key press
        form_layout.addRow("Task:", self.task_edit)

        self.category_edit = QLineEdit()
        self.category_edit.returnPressed.connect(self.submit_task)  # Submit on Enter key press
        form_layout.addRow("Category:", self.category_edit)

        self.time_investment_spin = QSpinBox()
        self.time_investment_spin.setRange(0, 1440)  # Minutes in a day
        form_layout.addRow("Time Investment (minutes):", self.time_investment_spin)

        self.start_time_edit = QTimeEdit()
        self.start_time_edit.setTime(QTime.currentTime())
        form_layout.addRow("Start Time:", self.start_time_edit)

        self.end_time_edit = QTimeEdit()
        self.end_time_edit.setTime(QTime.currentTime())
        form_layout.addRow("End Time:", self.end_time_edit)

        self.immediate_benefit_spin = QDoubleSpinBox()
        self.immediate_benefit_spin.setRange(0.0, 5.0)
        self.immediate_benefit_spin.setDecimals(1)
        form_layout.addRow("Immediate Benefit:", self.immediate_benefit_spin)

        self.future_impact_spin = QDoubleSpinBox()
        self.future_impact_spin.setRange(0.0, 5.0)
        self.future_impact_spin.setDecimals(1)
        form_layout.addRow("Future Impact:", self.future_impact_spin)

        self.personal_fulfillment_spin = QDoubleSpinBox()
        self.personal_fulfillment_spin.setRange(0.0, 5.0)
        self.personal_fulfillment_spin.setDecimals(1)
        form_layout.addRow("Personal Fulfillment:", self.personal_fulfillment_spin)

        self.progress_spin = QDoubleSpinBox()
        self.progress_spin.setRange(0, 100)
        self.progress_spin.setDecimals(0)   
        form_layout.addRow("Quantity of Progress (%):", self.progress_spin)

        self.notes_edit = QTextEdit()
        form_layout.addRow("Notes:", self.notes_edit)

        # Create a submit button
        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(self.submit_task)
        submit_button.setToolTip("You can also press Ctrl+Enter to submit the form.")
        form_layout.addRow(submit_button)

        #Add the form layout to the main layout
        main_layout.addLayout(form_layout)

        # Set the layout
        central_widget.setLayout(main_layout)

        # Create a shortcut for Ctrl+Enter to submit the form
        submit_shortcut = QShortcut(QKeySequence(Qt.CTRL | Qt.Key_Return), self)
        submit_shortcut.activated.connect(self.submit_task)

    def submit_task(self):
        try:
            # Collect data from input fields
            date = self.date_edit.date().toString("yyyy-MM-dd")
            task = self.task_edit.text()
            category = self.category_edit.text()
            time_investment = self.time_investment_spin.value() / 60  # Convert minutes to hours
            if time_investment <= 0:
                self.show_error("Time investment must be greater than zero.")
                return
            start_time = self.start_time_edit.time().toString("HH:mm")
            end_time = self.end_time_edit.time().toString("HH:mm")
            immediate_benefit = self.immediate_benefit_spin.value()
            future_impact = self.future_impact_spin.value()
            personal_fulfillment = self.personal_fulfillment_spin.value()
            progress = self.progress_spin.value()
            notes = self.notes_edit.toPlainText()

            # Create a Task object
            task_obj = Task(
                date=date,
                task=task,
                category=category,
                time_investment=time_investment,
                start_time=start_time,
                end_time=end_time,
                immediate_benefit=immediate_benefit,
                future_impact=future_impact,
                personal_fulfillment=personal_fulfillment,
                progress=progress,
                notes=notes
            )

            # Add the task to the database
            task_id = self.db_manager.add_task_entry(task_obj)
            if task_id:
                self.logger.info(f"Task added successfully with ID {task_id}.")
                self.show_toast("Task added successfully!")
                self.clear_form()
            else:
                raise Exception("Failed to add task to the database.")
        except Exception as e:
            self.logger.error(f"An error occurred: {e}")
            self.show_error(f"An error occurred: {e}")

    def clear_form(self):
        """Clear all input fields."""
        self.date_edit.setDate(QDate.currentDate())
        self.task_edit.clear()
        self.category_edit.clear()
        self.time_investment_spin.setValue(0)
        self.start_time_edit.setTime(QTime.currentTime())
        self.end_time_edit.setTime(QTime.currentTime())
        self.immediate_benefit_spin.setValue(0.0)
        self.future_impact_spin.setValue(0.0)
        self.personal_fulfillment_spin.setValue(0.0)
        self.progress_spin.setValue(0.0)
        self.notes_edit.clear()

    def show_toast(self, message):
        """Show a toast notification."""
        self.toast_label.setText(message)
        self.toast_label.setVisible(True)
        QTimer.singleShot(3000, self.hide_toast)  # Hide after 3 seconds

    def hide_toast(self):
        """Hide the toast notification."""
        self.toast_label.setVisible(False)

    def show_error(self, message):
        """Show an error message in a pop-up."""
        QMessageBox.critical(self, "Error", message)