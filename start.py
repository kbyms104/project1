import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
import interpark

form_class = uic.loadUiType("./prototype.ui")[0]


class WindowClass(QMainWindow, form_class):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.interpark_con.clicked.connect(self.start_interpark)
        # 전회차탐색 여부 체크박스
        #self.all_round_search
        # 현장수령 여부 체크박스
        #self.reception
        # 속력 선택 텍스트박스
        #self.speed_txt
        # 취켓팅버튼
        self.cancel_ticket.clicked.connect(self.start_reservation)

        self.inter = interpark.interpark(3)

    def start_interpark(self):
        self.inter.start_interpark()

    def start_reservation(self):
        self.inter.reservation()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()
