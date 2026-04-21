import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton,
    QLabel, QLineEdit, QMessageBox, QDateTimeEdit
)
from PyQt5.QtCore import Qt, QDateTime
from PyQt5.QtGui import QFont
from services.parser import parse_event
from services.calendar import post_event

#-------------------------
# MAIN UI CODE
#-------------------------
class CalendarUI(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    # Global stylesheet
    def apply_styles(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #303234;
                color: white;
                font-family: 'Times New Roman';
                font-size: 16px;
            }

            QLabel#title {
                color: yellowgreen;
                font-size: 25px;
            }

            QLineEdit {
                padding: 8px;
                border: 2px solid #ccc;
                border-radius: 5px;
                background-color: white;
                color: black;
            }

            QLineEdit:focus {
                border: 2px solid #4CAF50;
            }

            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #45a049;
            }

            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)

    def init_ui(self):
        self.apply_styles()
        self.setWindowTitle('AI Calendar Event Creator')
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        # Title
        title = QLabel('What are you planning?')
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Input
        self.event_prompt = QLineEdit()
        self.event_prompt.setPlaceholderText('Describe your event...')
        layout.addWidget(self.event_prompt)

        # Hidden fields (internal state)
        self.event_name = QLineEdit()
        self.description = QLineEdit()
        self.start_time = QDateTimeEdit()
        self.end_time = QDateTimeEdit()

        # Button
        btn = QPushButton('Create Event')
        btn.setCursor(Qt.PointingHandCursor)
        btn.clicked.connect(self.handle_input)
        layout.addWidget(btn)

        self.setLayout(layout)

    # -------------------------
    # CONTROLLER LOGIC
    # -------------------------
    def handle_input(self):
        text = self.event_prompt.text()

        if not text:
            QMessageBox.warning(self, 'Error', 'Enter event details')
            return

        # 🔥 Call parser (NOT UI responsibility)
        event = parse_event(text)

        # Store values
        self.event_name.setText(event.title)
        self.description.setText(event.description)

        start_dt = QDateTime.fromString(event.start, 'yyyy-MM-ddThh:mm:ss')
        end_dt = QDateTime.fromString(event.end, 'yyyy-MM-ddThh:mm:ss')

        self.start_time.setDateTime(start_dt)
        self.end_time.setDateTime(end_dt)

        self.show_preview(event)

    # -------------------------
    # PREVIEW UI
    # -------------------------
    def show_preview(self, event):
        msg = QMessageBox(self)
        msg.setWindowTitle('Preview Event')

        preview_text = (
            f"Name: {event.title}\n"
            f"Start: {event.start}\n"
            f"End: {event.end}\n"
            f"Description: {event.description or '(none)'}"
        )

        msg.setText(preview_text)

        # Messagebox styling
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #303234;
            }
            QMessageBox QLabel {
                color: #ffffff;
                text-align: center;
            }
        """)

        yes_btn = msg.addButton('Yes', QMessageBox.YesRole)
        no_btn = msg.addButton('No', QMessageBox.NoRole)

        # Button styling
        yes_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 8px 20px;
                border-radius: 5px;
                font-weight: bold;
                min-width: 60px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)
        
        no_btn.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                padding: 8px 20px;
                border-radius: 5px;
                font-weight: bold;
                min-width: 60px;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
            QPushButton:pressed {
                background-color: #ba0000;
            }
        """)

        msg.exec_()

        if msg.clickedButton() == yes_btn:
            self.post_event(event)

    # -------------------------
    # ACTION: send info to backend
    # -------------------------
    def post_event(self, event):
        post_event(
            summary=event.title,
            start_datetime=event.start,
            end_datetime=event.end,
            description=event.description
        )

        QMessageBox.information(self, 'Success', 'Event posted!')
        self.event_prompt.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CalendarUI()
    window.show()
    sys.exit(app.exec_())