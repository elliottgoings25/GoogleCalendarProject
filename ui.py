import sys
from PyQt5.QtWidgets import QApplication, QMessageBox, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit
from PyQt5.QtGui import QFont, QColor, QIcon
from PyQt5.QtCore import Qt
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
        send_btn.clicked.connect(self.show_preview)
        layout.addWidget(send_btn)
        
        self.setLayout(layout)

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
        
        post_event(  # 👈 Pass description here
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