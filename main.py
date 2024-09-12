import sys
from PyQt6.QtWidgets import QApplication, QWidget, QFileDialog
from PyQt6.QtGui import QImage, QPixmap
from ui_main import Ui_dialog
from qt_material import apply_stylesheet
import cv2
from utils import process

class Main_Window(QWidget):
    def __init__(self):
        super().__init__()
        # use the Ui_login_form
        self.ui = Ui_dialog()       
        self.ui.setupUi(self)      
        self.ui.import_btn.clicked.connect(self.upload)
        self.ui.res_btn.clicked.connect(self.get_result)
        self.width_source, self.height_source = self.ui.src_img.width(), self.ui.src_img.height()      
        self.show()
        
    def upload(self):
        self.arr_filename = QFileDialog.getOpenFileName(self,"Select Resumes","","Image Files(*.jpg *png *bmp)")[0]
        if self.arr_filename != '':
            img = cv2.imread(self.arr_filename)
            self.src_img = cv2.resize(img, (self.width_source, self.height_source))
            src_img = cv2.cvtColor(self.src_img, cv2.COLOR_BGR2RGB)
            temp_img = QImage(src_img, self.width_source, self.height_source, src_img.strides[0], QImage.Format.Format_RGB888) 
            self.ui.src_img.setPixmap(QPixmap.fromImage(temp_img))

    def get_result(self):
        img = process(self.src_img)
        src_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        temp_img = QImage(src_img, self.width_source, self.height_source, src_img.strides[0], QImage.Format.Format_RGB888) 
        self.ui.src_img.setPixmap(QPixmap.fromImage(temp_img))
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = Main_Window()
    apply_stylesheet(app, theme='dark_teal.xml')
    sys.exit(app.exec())