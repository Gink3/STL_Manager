import configparser
import sys

# https://docs.python.org/3/howto/logging.html#logging-basic-tutorial
import logging

from file_tree import FileTreeParser 

# https://build-system.fman.io/pyqt5-tutorial
# https://www.pythonguis.com/tutorials/pyqt-basic-widgets/
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDoubleSpinBox,
    QLabel,
    QLineEdit,
    QListWidget,
    QMainWindow,
    QSlider,
    QSpinBox,
)

class MainWindow(QMainWindow):
   def __init__(self):
      super(MainWindow, self).__init__()

      self.config = configparser.ConfigParser()
      self.config.read('config.txt')
      print(self.config['DEFAULT']['LibraryRoot'])
      self.parser = FileTreeParser(self.config['DEFAULT']['LibraryRoot'])

      self.setWindowTitle("STL Manager")
      widget = QListWidget()
      widget.addItems(["One", "Two", "Three"])

      widget.currentItemChanged.connect(self.index_changed)
      widget.currentTextChanged.connect(self.text_changed)

      self.setCentralWidget(widget)

   def index_changed(self, i): # Not an index, i is a QListWidgetItem
      print(i.text())

   def text_changed(self, s): # s is a str
      print(s)

if __name__ == "__main__":

   # Basic QT window
   app = QApplication(sys.argv)
   window = MainWindow()
   window.show()
   app.exec()