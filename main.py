#!/usr/bin/python3
import configparser
import sys
from pathlib import Path

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
      self.high_box = QHBoxLayout()

      # TODO Add toolbar menu

      # Add left column layout
      self.left_column_lo = QVBoxLayout()
      # set spacing to be 60/40 left to right
      # self.left_column_lo.set
      self.high_box.addLayout(self.left_column_lo)
      
      # Add right column layout
      self.right_column_lo = QVBoxLayout()
      self.high_box.addLayout(self.right_column_lo)

      self.top_right_lo = QHBoxLayout()
      self.right_column_lo.addLayout(self.top_right_lo)

      # Search Text box
      self.search_text = QLineEdit()
      self.search_text.setPlaceholderText("Search Text")
      self.top_right_lo.addWidget(self.search_text)

      # Search button
      self.search_button = QPushButton(text="Search")
      self.top_right_lo.addWidget(self.search_button)

      # File Parameter Label
      self.parameters = QLabel()
      self.parameters.setText("File Parameters")
      self.right_column_lo.addWidget(self.parameters)

      # Image preview widget
      self.preview = QLabel()
      pixmap = QPixmap('stl.png')
      self.preview.setPixmap(pixmap)
      self.right_column_lo.addWidget(self.preview)

      # Current Directory Box
      # TODO Added functionality to update the list if the text is changed to a valid directory 
      self.current_dir_wid = QLineEdit()
      self.current_dir_wid.setText(self.current_dir)
      self.left_column_lo.addWidget(self.current_dir_wid)

      # Map the displayed filenames to the full paths for later manipulation
      self.filemap = self.parser.list_model_files(self.parser.get_root_path())

      self.setWindowTitle("STL Manager")
      self.window_width = self.config.getint('DEFAULT','DefaultWidth')
      self.window_height = self.config.getint('DEFAULT','Defaultheight')
      self.resize(QSize(self.window_width, self.window_height))

      self.list_widget = QListWidget()
      self.left_column_lo.addWidget(self.list_widget)
      self.list_widget.addItems(self.filemap.keys())

      # self.list_widget.currentItemChanged.connect(self.index_changed)
      # self.list_widget.currentTextChanged.connect(self.text_changed)
      self.list_widget.itemDoubleClicked.connect(self.double_click_file)
      self.list_widget.itemClicked.connect(self.click_file)

      self.main_widget = QWidget()
      self.main_widget.setLayout(self.high_box)
      self.setCentralWidget(self.main_widget)

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


   def click_file(self, s):
      """
      Action for updating the file parameters and image preview for the selected item       
      """
      # TODO
      logging.info("[[STUB click_file STUB]] <-- main.py")
      logging.debug("Clicked on " + s.text() + " in list_widget")
      logging.debug("File path associated with " + s.text() + " is " + str(self.filemap[s.text()]) )
      self.check_for_mtd_file(Path(self.filemap[s.text()]))


   def check_for_mtd_file(self, filepath):
      """
      Check if the given file has a metadata file already associated with it
      """
      # TODO Create a filter check function for model object extensions
      if filepath.name.endswith(".stl"):   
         # if file path exists
         if filepath.exists():
            logging.debug("Filepath: " + str(filepath) + " basename: " + filepath.name)
            # get metadata filepath
            metadata_file = self.get_metadata_filepath(filepath)
            # Check if metadata filepath exists
            if metadata_file.exists():
               logging.debug("Found metadata file: " + str(metadata_file))
            else:
               # if not already created, create
               logging.debug("Metadata file not found, creating" + str(metadata_file))
               with metadata_file.open("w", encoding="utf-8") as f:
                  f.write("Created " + str(metadata_file))


   def get_metadata_filepath(self, modelpath):
      """"
      Convert a model file path to metadata file
      """
      logging.debug("Entering get_metadata_filepath")
      return modelpath.parent.joinpath("." + modelpath.name[:-3] + "mtd")

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

