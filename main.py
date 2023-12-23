#!/usr/bin/python3
import configparser
import sys

# https://docs.python.org/3/howto/logging.html#logging-basic-tutorial
import logging

from file_tree import FileTreeParser 

# https://build-system.fman.io/pyqt5-tutorial
# https://www.pythonguis.com/tutorials/pyqt-basic-widgets/
from PyQt5.QtCore import QSize, Qt
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
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
    QPushButton
)

class MainWindow(QMainWindow):
   def __init__(self):
      super(MainWindow, self).__init__()

      # Initialize config parser
      self.config = configparser.ConfigParser()
      self.config.read('config.txt')
      self.current_dir = self.config['DEFAULT']['LibraryRoot']
      logging.info("LibraryRoot: " + self.current_dir)

      # Initialize file parser
      self.parser = FileTreeParser(self.current_dir)

      # Highest level widget
      high_box = QHBoxLayout()

      # Add left column layout
      left_column_lo = QVBoxLayout()
      high_box.addLayout(left_column_lo)
      
      # Add right column layout
      right_column_lo = QVBoxLayout()
      high_box.addLayout(right_column_lo)

      top_right_lo = QHBoxLayout()
      right_column_lo.addLayout(top_right_lo)

      # Search Text box
      search_text = QLineEdit()
      search_text.setPlaceholderText("Search Text")
      top_right_lo.addWidget(search_text)

      # Search button
      search_button = QPushButton(text="Search")
      top_right_lo.addWidget(search_button)

      # Image preview widget
      preview = QLabel()
      pixmap = QPixmap('stl.png')
      preview.setPixmap(pixmap)
      right_column_lo.addWidget(preview)

      # Current Directory Box
      self.current_dir_wid = QLineEdit()
      self.current_dir_wid.setText(self.current_dir)
      left_column_lo.addWidget(self.current_dir_wid)

      # Map the displayed filenames to the full paths for later manipulation
      self.filemap = self.parser.list_model_files(self.parser.get_root_path())

      self.setWindowTitle("STL Manager")
      self.window_width = self.config.getint('DEFAULT','DefaultWidth')
      self.window_height = self.config.getint('DEFAULT','Defaultheight')
      self.resize(QSize(self.window_width, self.window_height))

      self.list_widget = QListWidget()
      left_column_lo.addWidget(self.list_widget)
      self.list_widget.addItems(self.filemap.keys())

      # self.list_widget.currentItemChanged.connect(self.index_changed)
      # self.list_widget.currentTextChanged.connect(self.text_changed)
      self.list_widget.itemDoubleClicked.connect(self.double_click_file)


      widget = QWidget()
      widget.setLayout(high_box)
      self.setCentralWidget(widget)

   # def index_changed(self, i): # Not an index, i is a QListWidgetItem
   #    logging.debug("index_changed " + i.text())

   # def text_changed(self, s): # s is a str
   #    logging.debug("text_changed " + s)

   def double_click_file(self, s):
      """
      Action for the list widget to navigate up or down the file tree when double clicking on a directory
      """
      logging.debug("Double clicked on " + s.text())
      # if selected text if a directory
      if s.text().endswith("\\") or s.text() == "..":
         # update current directory
         self.update_current_dir(s.text())

         # regenerate filemap
         new_filemap = self.parser.list_model_files(self.current_dir)
         self.filemap = new_filemap

         # clear list widget and add new elements
         self.list_widget.clear()
         self.list_widget.addItems(self.filemap.keys())


   def update_current_dir(self, text):
      self.current_dir = self.filemap[text]
      self.current_dir_wid.setText(self.current_dir)


if __name__ == "__main__":
   logging.basicConfig(filename='stl_manager.log', encoding='utf-8', level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
   logging.info("Logging initialized")

   # Basic QT window
   app = QApplication(sys.argv)
   window = MainWindow()
   window.show()
   app.exec()

