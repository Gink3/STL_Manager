#!/usr/bin/python3
import configparser
import sys
from pathlib import Path

# https://docs.python.org/3/howto/logging.html#logging-basic-tutorial
import logging
import os

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
    QFileSystemModel,
    QLabel,
    QLineEdit,
    QListWidget,
    QMainWindow,
    QSlider,
    QSpinBox,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
    QTreeView,
    QPushButton
)


from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

# TODO Setup PEP-8 linter

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
      self.parser.scan_for_metadata()

      # Highest level widget
      self.high_box = QHBoxLayout()

      # Back Button
      self.backbutton = QPushButton("Back")

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

      # File explorer viewer
      self.tree_model = QFileSystemModel()
      self.tree_model.setRootPath("")      
      self.tree = QTreeView()
      self.tree.setModel(self.tree_model)
      self.tree.setRootIndex(self.tree_model.index(self.current_dir))
      
      self.tree.setAnimated(False)
      self.tree.setIndentation(20)
      self.tree.setSortingEnabled(True)
      
      self.tree.resize(640, 480) # Can change
      # TODO Need to make button prettier
      self.initUI() 
      self.left_column_lo.addWidget(self.tree)   
      
      # self.list_widget.currentItemChanged.connect(self.index_changed)
      # self.list_widget.currentTextChanged.connect(self.text_changed)
      self.tree.doubleClicked.connect(self.double_click_file)
      #self.tree_widget.itemClicked.connect(self.click_file)

      self.main_widget = QWidget()
      self.main_widget.setLayout(self.high_box)
      self.setCentralWidget(self.main_widget)

   # def index_changed(self, i): # Not an index, i is a QListWidgetItem
   #    logging.debug("index_changed " + i.text())

   # def text_changed(self, s): # s is a str
   #    logging.debug("text_changed " + s)

   def initUI(self):
      """
      Add Back button to File Explorer widget
      """
      self.left_column_lo.addWidget(self.backbutton)
      self.backbutton.clicked.connect(self.handle_back_clicked)

   def handle_back_clicked(self):
      """
      Go back a previous directory with default Back button
      """
      pathName = Path(self.current_dir).parent.absolute()
      print(pathName)

      self.current_dir = str(pathName)
      self.current_dir_wid.setText(self.current_dir)
      # regenerate filemap
      new_filemap = self.parser.list_model_files(self.current_dir)
      self.filemap = new_filemap
      self.tree_model.setRootPath("")    
      self.tree.reset()
      self.tree.setModel(self.tree_model)        
      self.tree.setRootIndex(self.tree_model.index(str(pathName)))

      #self.list_widget.addItems(self.filemap.keys())

      # Check for metadata files for each file entry in the filemap
      for filepath in self.filemap.values():
         self.parser.check_for_mtd_file(Path(filepath))

   def double_click_file(self, index):
      """
      Action for the list widget to navigate up or down the file tree when double clicking on a directory
      """

      logging.debug("Double clicked on " + self.tree_model.filePath(index))
      # if selected text if a directory
      if os.path.isdir(self.tree_model.filePath(index)):

         # update current directory (Can add this back)
         #self.filemap.add[self.parser.get_root_path()]
         #self.update_current_dir(self.tree_model.filePath(index))

         self.current_dir = self.tree_model.filePath(index)
         self.current_dir_wid.setText(self.current_dir)
         # regenerate filemap
         new_filemap = self.parser.list_model_files(self.current_dir)
         self.filemap = new_filemap
         self.tree_model.setRootPath("")    
         self.tree.reset()
         self.tree.setModel(self.tree_model)        
         self.tree.setRootIndex(self.tree_model.index(self.tree_model.filePath(index)))

         #self.list_widget.addItems(self.filemap.keys())

         # Check for metadata files for each file entry in the filemap
         for filepath in self.filemap.values():
            self.parser.check_for_mtd_file(Path(filepath))


   def click_file(self, s):
      """
      Action for updating the file parameters and image preview for the selected item       
      """
      # TODO
      logging.info("[[STUB click_file STUB]] <-- main.py")
      logging.debug("Clicked on " + s.text() + " in list_widget")
      logging.debug("File path associated with " + s.text() + " is " + str(self.filemap[s.text()]) )
      metadata_filepath = self.parser.check_for_mtd_file(Path(self.filemap[s.text()]))


   def update_current_dir(self, text):
      #print(self.filemap)
      #self.current_dir = self.filemap[text]
      self.current_dir_wid.setText(self.current_dir)


if __name__ == "__main__":
   logging.basicConfig(filename='stl_manager.log', encoding='utf-8', level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
   logging.info("Logging initialized")

   # Basic QT window
   app = QApplication(sys.argv)
   window = MainWindow()
   window.show()
   app.exec()

