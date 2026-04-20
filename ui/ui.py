import sys
from PyQt5.QtWidgets import QApplication, QMessageBox, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QDateTimeEdit
from PyQt5.QtCore import Qt, QDateTime
from PyQt5.QtGui import QFont, QColor, QIcon
from services.calendar import post_event

class CalendarUI(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Window properties and layout
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
        layout.addStretch() #keeps title at top
        
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
        self.event_prompt.setMinimumHeight(40)  # Height
        layout.addWidget(self.event_prompt)


        # --Hidden Widgets--
        from PyQt5.QtWidgets import QDateTimeEdit
        from PyQt5.QtCore import QDateTime
        
        self.event_name = QLineEdit()
        self.start_time = QDateTimeEdit()
        self.start_time.setDateTime(QDateTime.currentDateTime())
        self.end_time = QDateTimeEdit()
        self.end_time.setDateTime(QDateTime.currentDateTime().addSecs(3600))
        self.description = QLineEdit()
        # --Hidden Widgets--


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
        send_btn.setCursor(Qt.PointingHandCursor)  # Hand cursor on hover
        send_btn.clicked.connect(self.prompt_and_responses)
        layout.addWidget(send_btn)
        
        self.setLayout(layout)

    def prompt_and_responses(self):
        """
        Test function that extracts event details (simulating Claude API)
        """
        text = self.event_prompt.text()
        
        if not text:
            QMessageBox.warning(self, 'Error', 'Please enter event details')
            return
        
        def extract_field(field_name):
            """Simulate extracting a field from the text"""
            # For testing, just return hardcoded values
            test_data = {
                "title": "test",
                "description": "testing",
                "start_datetime": "2026-04-22T09:00:00",
                "end_datetime": "2026-04-22T10:00:00"
            }
            return test_data.get(field_name, "")
        
        # Get each field separately
        title = extract_field("title")
        description = extract_field("description")
        start = extract_field("start_datetime")
        end = extract_field("end_datetime")
        
        # Populate the UI fields
        self.event_name.setText(title)
        self.description.setText(description)
        
        from PyQt5.QtCore import QDateTime
        start_dt = QDateTime.fromString(start, 'yyyy-MM-ddThh:mm:ss')
        end_dt = QDateTime.fromString(end, 'yyyy-MM-ddThh:mm:ss')
        self.start_time.setDateTime(start_dt)
        self.end_time.setDateTime(end_dt)
        
        # Show preview
        self.show_preview()

    def show_preview(self):
        """Show preview dialog before posting"""
        name = self.event_name.text()
        start = self.start_time.dateTime().toString('yyyy-MM-dd HH:mm:ss')
        end = self.end_time.dateTime().toString('yyyy-MM-dd HH:mm:ss')
        description = self.description.text()
        
        if not name:
            QMessageBox.warning(self, 'Error', 'Please enter an event name')
            return
        
        preview_text = f"""
    Event Details:
    ━━━━━━━━━━━━━━
    Name: {name}
    Start: {start}
    End: {end}
    Description: {description if description else '(none)'}

    Confirm to post this event?
        """
        
        reply = QMessageBox.question(
            self, 
            'Preview Event', 
            preview_text,
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.post_event()

    def post_event(self):
        """Actually post the event"""
        start = self.start_time.dateTime().toString('yyyy-MM-ddThh:mm:ss')
        end = self.end_time.dateTime().toString('yyyy-MM-ddThh:mm:ss')
        
        post_event(
            summary=self.event_name.text(),
            start_datetime=start,
            end_datetime=end,
            description=self.description.text()
        )
        
        QMessageBox.information(self, 'Success', 'Event posted to calendar!')
        self.event_name.setText('')
        self.description.setText('')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CalendarUI()
    window.show()
    sys.exit(app.exec_())