import logging
from PySide6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget

class MainWindow(QMainWindow):
    def __init__(self, logger):
        super().__init__()

        self.logger = logger
        self.setWindowTitle("My PySide6 Application")

        # Set the central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create a layout and add widgets
        layout = QVBoxLayout()
        label = QLabel("Hello, PySide6!")
        layout.addWidget(label)

        central_widget.setLayout(layout)