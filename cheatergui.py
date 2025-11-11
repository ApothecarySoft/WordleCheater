import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QTextEdit, QVBoxLayout


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("WordleBot")

        guessTextEdit = QTextEdit()
        layout = QVBoxLayout()
        layout.addWidget(guessTextEdit)
        self.setCentralWidget(layout)

        
