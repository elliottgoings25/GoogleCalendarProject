import sys
from PyQt5.QtWidgets import QApplication
from ui import CalendarUI

#--------------------------
# MAIN ENTRY POINT
#--------------------------
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CalendarUI()
    window.show()
    sys.exit(app.exec_())