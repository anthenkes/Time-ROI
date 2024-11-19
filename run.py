import sys, logging
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap

from frontend.main import MainWindow
from backend.logs.logger_setup import GetLogger

logger_level = logging.INFO
logger = GetLogger(__name__, logger_level)

if __name__ == "__main__":
    app = QApplication(sys.argv)


    window = MainWindow(logger)
    window.show()

    sys.exit(app.exec())