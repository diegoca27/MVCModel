# main.py
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from views.login_hospital import Ui_MainWindow
from model.DAO.add_person_DAO import LoginController

if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)

    # Iniciar el controlador del Login
    controller = LoginController(ui)

    MainWindow.show()
    sys.exit(app.exec_())
