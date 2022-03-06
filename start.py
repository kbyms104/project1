import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication
import coco

if __name__ == '__main__':
    app = QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = coco.Ui_Dialog(Dialog)
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
