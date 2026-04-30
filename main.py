import os
import sys
import multiprocessing
import traceback
from dotenv import load_dotenv
from PyQt5.QtWidgets import QApplication
from ui.ui import CalendarUI

#--------------------------
# Load env
#--------------------------
def get_env_path():
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, '.env')
    return '.env'

load_dotenv(get_env_path())

#--------------------------
# MAIN ENTRY POINT
#--------------------------
if __name__ == '__main__':
    multiprocessing.freeze_support()

    try:
        app = QApplication(sys.argv)
        window = CalendarUI()
        window.show()
        sys.exit(app.exec_())

    except Exception as e:
        print("CRASH OCCURRED:")
        traceback.print_exc()
        input("Press Enter to exit...")