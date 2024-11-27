from PySide6.QtWidgets import QVBoxLayout, QWidget
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from backend.data.dbmanager import DatabaseManager

class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super().__init__(fig)

class GraphWidget(QWidget):
    def __init__(self, db_manager: DatabaseManager, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.layout = QVBoxLayout(self)
        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
        self.layout.addWidget(self.canvas)
        self.plot_data()

    def plot_data(self):
        # Connect to the database and fetch data
        conn = self.db_manager.get_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT task, time_investment FROM TaskLog;")
            data = cursor.fetchall()
            conn.close()

            x_data = [row[0] for row in data]
            y_data = [row[1] for row in data]

            self.canvas.axes.plot(x_data, y_data)
            self.canvas.draw()
    
    def update_plot(self):
        self.canvas.axes.clear()
        self.plot_data()