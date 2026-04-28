import sys
import json
from PyQt5.QtWidgets import QApplication, QMessageBox, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt
from services.calendar import post_event
from llm import ask_gemini

class CalendarUI(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Ai Calendar Event Creator')
        self.setGeometry(100, 100, 400, 300)
        self.setStyleSheet("background-color: #303234;")
        
        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Title
        title = QLabel('What are you planning?')
        title.setFont(QFont('Papyrus', 20))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: yellowgreen; font-size: 20px;")
        layout.addWidget(title)
        layout.addStretch()
        
        # Event prompt
        self.event_prompt = QLineEdit()
        self.event_prompt.setPlaceholderText('What are you planning?')
        self.event_prompt.setFont(QFont('Comic Sans MS', 12))
        self.event_prompt.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 2px solid #ccc;
                border-radius: 5px;
                background-color: white;
            }
            QLineEdit:focus {
                border: 2px solid #4CAF50;
            }
        """)
        self.event_prompt.setMinimumHeight(40)
        layout.addWidget(self.event_prompt)

        # Send button
        send_btn = QPushButton('Create Event')
        send_btn.setFont(QFont('Bleeding Cowboys', 12, QFont.Bold))
        send_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)
        send_btn.setMinimumHeight(45)
        send_btn.setCursor(Qt.PointingHandCursor)
        send_btn.clicked.connect(self.show_preview)
        layout.addWidget(send_btn)
        
        self.setLayout(layout)

    def show_preview(self):
        user_text = self.event_prompt.text()
        
        if not user_text:
            QMessageBox.warning(self, 'Error', 'Please enter what you are planning')
            return
        
        prompt = f"""
        Extract event details from this text and return ONLY a JSON object with these fields:
        - summary (event name)
        - start (in format YYYY-MM-DDTHH:MM:SS)
        - end (in format YYYY-MM-DDTHH:MM:SS)
        - description
        
        Text: {user_text}
        Today's date is: 2026-04-28
        """
        
        response = ask_gemini(prompt)
        
        try:
            response = response.strip().replace("```json", "").replace("```", "")
            event = json.loads(response)
            
            preview_text = f"""
Event Details:
━━━━━━━━━━━━━━
Name: {event['summary']}
Start: {event['start']}
End: {event['end']}
Description: {event.get('description', '(none)')}

Confirm to post this event?
            """
            
            reply = QMessageBox.question(
                self,
                'Preview Event',
                preview_text,
                QMessageBox.Yes | QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                post_event(
                    summary=event['summary'],
                    start_datetime=event['start'],
                    end_datetime=event['end'],
                    description=event.get('description', '')
                )
                QMessageBox.information(self, 'Success', 'Event posted to calendar!')
                self.event_prompt.setText('')
                
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Could not parse event: {str(e)}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CalendarUI()
    window.show()
    sys.exit(app.exec_())