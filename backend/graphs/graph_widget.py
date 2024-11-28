from PySide6.QtWidgets import QVBoxLayout, QWidget, QComboBox, QLineEdit, QPushButton, QHBoxLayout
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from backend.data.dbmanager import DatabaseManager
import mplcursors

class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super().__init__(fig)

class GraphWidget(QWidget):
    def __init__(self, db_manager: DatabaseManager, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager

        # Track cursor objects
        

        self.cursors = []
        self.layout = QVBoxLayout(self)
        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
        self.layout.addWidget(self.canvas)

        # Add a horizontal layout for task selection and search
        control_layout = QHBoxLayout()

        # Add a dropdown menu for task selection
        self.task_selector = QComboBox(self)
        self.task_selector.currentIndexChanged.connect(self.update_plot)
        control_layout.addWidget(self.task_selector)

        # Add a search bar for task filtering
        self.search_bar = QLineEdit(self)
        self.search_bar.setPlaceholderText("Search tasks...")
        self.search_bar.textChanged.connect(self.update_plot)
        control_layout.addWidget(self.search_bar)

        # Add a button to clear the search bar
        self.clear_search_button = QPushButton("Clear", self)
        self.clear_search_button.clicked.connect(self.clear_search)
        control_layout.addWidget(self.clear_search_button)

        self.layout.addLayout(control_layout)

        self.load_tasks()
        self.plot_data()

        

    def load_tasks(self):
        # Connect to the database and fetch unique task names
        conn = self.db_manager.get_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT task FROM TaskLog;")
            tasks = cursor.fetchall()
            conn.close()

            # Use a set to track unique task names
            unique_tasks = set()
            for task in tasks:
                cleaned_task = task[0].strip().lower()
                unique_tasks.add(cleaned_task.capitalize())

            # Populate the dropdown menu with task names
            self.task_selector.addItem("All Tasks")
            for task in sorted(unique_tasks):
                self.task_selector.addItem(task)

    def plot_data(self):
        selected_task = self.task_selector.currentText().lower() if self.task_selector.currentText() != "All Tasks" else None
        search_text = self.search_bar.text().lower()

        # Connect to the database and fetch data
        conn = self.db_manager.get_connection()
        if conn:
            cursor = conn.cursor()
            if selected_task:
                cursor.execute("SELECT task, roi, date FROM TaskLog WHERE LOWER(task) = ?", (selected_task,))
            else:
                cursor.execute("SELECT task, roi, date FROM TaskLog;")
            data = cursor.fetchall()
            conn.close()

            # Clear previous cursors
            for cursor in self.cursors:
                cursor.remove()
            self.cursors.clear()

            if selected_task:
                # Plot data for a specific task over time
                x_data = []
                y_data = []
                labels = []
                for row in data:
                    task_name = row[0].strip().lower()
                    roi = row[1]
                    date = row[2]
                    if search_text in task_name:
                        x_data.append(date)
                        y_data.append(roi)
                        labels.append(f"{task_name.capitalize()}: {roi}")

                # Plot each data point as a standalone point
                scatter = self.canvas.axes.scatter(x_data, y_data)

                # Label the axes
                self.canvas.axes.set_xlabel('Date')
                self.canvas.axes.set_ylabel('ROI')
                self.canvas.axes.set_title(f'Task ROI for {selected_task.capitalize()}')

                # Rotate x-axis labels for better readability
                self.canvas.axes.tick_params(axis='x', rotation=45)

                # Add hover functionality for individual points
                cursor = mplcursors.cursor(scatter, hover=True)
                cursor.connect("add", lambda sel: sel.annotation.set_text(labels[sel.index]))
                self.cursors.append(cursor)

            else:
                # Normalize task names to lowercase, strip whitespace, and collect ROI values
                task_data = {}
                for row in data:
                    task_name = row[0].strip().lower()  # Strip whitespace and convert to lowercase
                    roi = row[1]
                    if search_text in task_name:
                        if task_name in task_data:
                            task_data[task_name].append(roi)
                        else:
                            task_data[task_name] = [roi]

                x_data = []
                y_data = []
                labels = []
                avg_x_data = []
                avg_y_data = []
                for task_name, rois in task_data.items():
                    avg_roi = sum(rois) / len(rois)
                    for roi in rois:
                        x_data.append(task_name)
                        y_data.append(roi)
                        labels.append(f"{task_name.capitalize()}: {roi}\nAverage: {avg_roi:.2f}")
                    if len(rois) > 1:
                        avg_x_data.append(task_name)
                        avg_y_data.append(avg_roi)

                # Plot each data point as a standalone point
                scatter = self.canvas.axes.scatter(x_data, y_data)

                # Plot average ROI as a black bar
                self.canvas.axes.scatter(avg_x_data, avg_y_data, color='black', marker='_', s=100)

                # Label the axes
                self.canvas.axes.set_xlabel('Task')
                self.canvas.axes.set_ylabel('ROI')
                self.canvas.axes.set_title('Task ROI')

                # Rotate x-axis labels for better readability
                self.canvas.axes.tick_params(axis='x', rotation=45)

                # Add hover functionality for individual points
                cursor = mplcursors.cursor(scatter, hover=True)
                cursor.connect("add", lambda sel: sel.annotation.set_text(labels[sel.index]))
                self.cursors.append(cursor)

            self.canvas.draw()
    
    def update_plot(self):
        self.canvas.axes.clear()
        self.plot_data()

    def clear_search(self):
        self.search_bar.clear()