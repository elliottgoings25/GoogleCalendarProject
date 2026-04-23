import sys
import os
import subprocess

# Ensure parent directory is in path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Action imports
from services.parser import parse_event
from services.calendar import post_event as calendar_post_event

# UI imports
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QMessageBox, QDateTimeEdit
)
from PyQt5.QtCore import Qt, QDateTime
from PyQt5.QtGui import QFont

#-------------------------
# UI CODE
#-------------------------
class CalendarUI(QWidget):
    def __init__(self):
        super().__init__()

        # -----Check for token.pickle-----
        if not os.path.exists('token.pickle'):
            success = self.ensure_token()
            if not success:
                print("Failed to generate token")
                sys.exit(1)

        self.init_ui()
    
    #-------------------------
    # Global stylesheet
    #-------------------------
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
    #-------------------------
    # UI SETUP
    #-------------------------
    def init_ui(self):

        self.apply_styles()
        self.setWindowTitle('AI Calendar Event Creator')
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        # -----Title-----
        title = QLabel('What are you planning?')
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # -----Input textbox-----
        self.event_prompt = QLineEdit()
        self.event_prompt.setPlaceholderText('What are you getting up to?')
        layout.addWidget(self.event_prompt)

        # -----Create Button-----
        btn = QPushButton('Schedule Event')
        btn.setCursor(Qt.PointingHandCursor)
        btn.clicked.connect(self.handle_input) # Connect button to handler
        layout.addWidget(btn)

        self.setLayout(layout)

    # -------------------------
    # CONTROLLER LOGIC
    # -------------------------
    def handle_input(self):
        text = self.event_prompt.text()

        # -----Ensure input is present-----
        if not text:
            QMessageBox.warning(self, 'Error', 'Enter event details')
            return

        #-------------------------
        # ACTION: Parse event
        #-------------------------
        event = parse_event(text)

        # -----Go to preview-----
        self.show_preview(event)

    # -------------------------
    # PREVIEW OF EVENT BEFORE PUSH
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

        # -----Messagebox styling-----
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
        no_btn = msg.addButton('No', QMessageBox.NoRole) # Closes the preview with no action

        # -----Button styling-----
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

        # -----Links button click to push action-----
        if msg.clickedButton() == yes_btn:
            self.post_event(event)

    # -------------------------
    # ACTION: send event to push code
    # -------------------------
    def post_event(self, event):
        # -----Call calendar service-----
        calendar_post_event(
            summary=event.title,
            start_datetime=event.start,
            end_datetime=event.end,
            description=event.description
        )

        # -----Confirmation message-----
        QMessageBox.information(self, 'Success', 'Event posted!')
        self.event_prompt.clear()

    # -------------------------
    # Ensure token.pickle exists by calling generate_token.py
    # -------------------------
    def ensure_token(self):
        try:
            result = subprocess.run(
                [sys.executable, 'generate_token.py'],
                check=True,
                capture_output=True
            )
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
            return False


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CalendarUI()
    window.show()
    sys.exit(app.exec_())