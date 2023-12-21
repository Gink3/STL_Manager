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

      # Initialize config parser
      self.config = configparser.ConfigParser()
      self.config.read('config.txt')
      logging.info("LibraryRoot: " + self.config['DEFAULT']['LibraryRoot'])

      # Initialize file parser
      self.parser = FileTreeParser(self.config['DEFAULT']['LibraryRoot'])

      # Map the displayed filenames to the full paths for later manipulation
      self.filemap = self.parser.list_model_files(self.parser.get_root_path())

      self.setWindowTitle("STL Manager")
      list_widget = QListWidget()
      list_widget.addItems(self.filemap.keys())

      list_widget.currentItemChanged.connect(self.index_changed)
      list_widget.currentTextChanged.connect(self.text_changed)

      self.setCentralWidget(list_widget)

   def index_changed(self, i): # Not an index, i is a QListWidgetItem
      print(i.text())

   def text_changed(self, s): # s is a str
      print(s)

if __name__ == "__main__":
   logging.basicConfig(filename='stl_manager.log', encoding='utf-8', level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
   logging.info("Logging initialized")

   # Basic QT window
   app = QApplication(sys.argv)
   window = MainWindow()
   window.show()
   app.exec()