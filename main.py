import sys

# DO NOT REMOVE. vtk IS BEING USED
# WILL BREAK RENDER WIDGET INTERACTION
import vtk

from PyQt5.QtCore import QSize, Qt, QSortFilterProxyModel
from PyQt5.QtGui import QPixmap
from vtkmodules.vtkIOGeometry import vtkSTLReader
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
    QPushButton,
    QFrame
)
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderer
)
import configparser
import sys
from pathlib import Path

import logging
import os

from file_tree import FileTreeParser 

from filedb import FileDB

import signal

# handle Ctrl + C
signal.signal(signal.SIGINT, signal.SIG_DFL)

# class HandleFileTypesProxy(QSortFilterProxyModel):
#    """
#    A proxy model that excludes files from the view
#    that end with the given extension
#    """
#    def __init__(self, excludes, *args, **kwargs):
#       super(HandleFileTypesProxy, self).__init__(*args, **kwargs)
#       self._excludes = excludes[:]

#    def filterAcceptsRow(self, srcRow, srcParent):
#       idx = self.sourceModel().index(srcRow, 0, srcParent)
#       name = idx.data()

#       # Can do whatever kind of tests you want here,
#       # against the name
#       for exc in self._excludes:
#          print(exc)
#          if not name.endswith(exc):
#                return False
      
#       return True

class MainWindow(QMainWindow):
   def __init__(self, parent = None):
      QMainWindow.__init__(self, parent)

      self._init_db()
      self.selected_file = None
      self.colors = vtkNamedColors()

      self._init_config()
      self._init_parser()
      self._init_layouts()

      # TODO Add toolbar menu
      # Could break down the rest of the init functions to go by column
      self._init_search()
      self._init_right_column()
      self._init_current_dir_box()

      # # Map the displayed filenames to the full paths for later manipulation
      self.filemap = self.parser.list_model_files(self.parser.get_root_path())

      self._init_window_settings()
      self._init_file_explorer()
      self._init_back_button()

      self.main_widget = QWidget(objectName='main_widget')
      self.main_widget.setLayout(self.high_box)
      self.setCentralWidget(self.main_widget)


   def handle_back_clicked(self):
      """
      Go back a previous directory with default Back button
      """
      pathName = Path(self.current_dir).parent.absolute()

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
         self.current_dir = self.tree_model.filePath(index)
         self.current_dir_wid.setText(self.current_dir)
         # regenerate filemap
         new_filemap = self.parser.list_model_files(self.current_dir)
         self.filemap = new_filemap
         self.tree_model.setRootPath("")    
         self.tree.reset()
         self.tree.setModel(self.tree_model)        
         self.tree.setRootIndex(self.tree_model.index(self.tree_model.filePath(index)))

         # Check for metadata files for each file entry in the filemap
         for filepath in self.filemap.values():
            self.parser.check_for_mtd_file(Path(filepath))


   def click_file(self, index):
      """
      Action for updating the file parameters and image preview for the selected item       
      """
      logging.debug("File path associated with " + str(self.tree_model.filePath(index)) )
      filePath = Path(self.tree_model.filePath(index))
      
      if os.path.basename(filePath).endswith("stl"):
         self.selected_file = filePath
         self.parameters.setText( os.path.basename((self.selected_file)) )
         metadata_filepath = self.parser.check_for_mtd_file(Path(self.tree_model.filePath(index)))

         self.update_render(filePath)
            

   def update_render(self,stl_filepath):
      # if not empty 
      if not self.renders_layout.isEmpty():
         self.renders_layout.removeWidget(self.frame)

      self.frame = QFrame()
      self.vl = QVBoxLayout()
      self.vtkWidget = QVTKRenderWindowInteractor(self.frame)
      self.vl.addWidget(self.vtkWidget)

      self.ren = vtkRenderer()
      self.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
      self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()

      self.reader = vtkSTLReader()
      self.reader.SetFileName(stl_filepath)
      self.reader.Update()

      # Create a mapper
      self.mapper = vtkPolyDataMapper()
      self.mapper.SetInputConnection(self.reader.GetOutputPort())

      # Create an actor
      self.actor = vtkActor()
      self.actor.GetProperty().SetDiffuseColor(self.colors.GetColor3d('LightSteelBlue'))
      self.actor.SetMapper(self.mapper)

      self.ren.AddActor(self.actor)
      self.ren.SetBackground(self.colors.GetColor3d('DimGray'))

      self.ren.ResetCamera()

      self.frame.setLayout(self.vl)
      self.renders_layout.addWidget(self.frame)
      
      self.show()
      self.iren.Initialize()


   def _init_config(self):
      # Initialize config parser
      self.config = configparser.ConfigParser()
      self.config.read('dev/config.txt')
      self.current_dir = self.config['DEFAULT']['LibraryRoot']
      logging.info("LibraryRoot: " + self.current_dir)


   def _init_parser(self):
      # TODO replace with SQLite handler
      # Initialize file parser
      self.parser = FileTreeParser(self.current_dir)
      #self.parser.scan_for_metadata()


   def _init_layouts(self):
      # Highest level widget
      self.high_box = QHBoxLayout()

      # Add left column layout
      self.left_column_lo = QVBoxLayout()
      self.high_box.addLayout(self.left_column_lo)
      
      # # Add right column layout
      self.right_column_lo = QVBoxLayout()
      self.high_box.addLayout(self.right_column_lo)

      self.top_right_lo = QHBoxLayout()
      self.right_column_lo.addLayout(self.top_right_lo)

      self.top_left_lo = QHBoxLayout()
      self.left_column_lo.addLayout(self.top_left_lo)


   def _init_search(self):
      # Search Text box
      self.search_text = QLineEdit()
      self.search_text.setPlaceholderText("Search Text")
      self.top_right_lo.addWidget(self.search_text)

      # Search button
      self.search_button = QPushButton(text="Search")
      self.top_right_lo.addWidget(self.search_button)


   def _init_right_column(self):
      # File Parameter Label
      self.parameters = QLabel()
      self.parameters.setText("File Parameters")
      self.right_column_lo.addWidget(self.parameters)

      self.renders_layout = QVBoxLayout()
      self.right_column_lo.addLayout(self.renders_layout)


   def _init_current_dir_box(self):
      # Current Directory Box
      # TODO Added functionality to update the list if the text is changed to a valid directory 
      self.current_dir_wid = QLineEdit()
      self.current_dir_wid.setText(self.current_dir)
      self.top_left_lo.addWidget(self.current_dir_wid, 75)


   def _init_window_settings(self):
      self.setWindowTitle("STL Manager")
      self.window_width = self.config.getint('DEFAULT','DefaultWidth')
      self.window_height = self.config.getint('DEFAULT','Defaultheight')
      self.resize(QSize(self.window_width, self.window_height))


   def _init_back_button(self):
      # Back Button
      self.backbutton = QPushButton(text="Back")
      self.top_left_lo.addWidget(self.backbutton, 25)
      self.backbutton.clicked.connect(self.handle_back_clicked)
      self.left_column_lo.addWidget(self.tree)   


   def _init_file_explorer(self):
      # File explorer viewer
      self.tree_model = QFileSystemModel()
      self.idx = self.tree_model.setRootPath(self.current_dir)   

      # Include certain file extension to be displayed via proxy 
      self.tree_model.setNameFilters(['*.stl'])
      self.tree_model.setNameFilterDisables(False)

      self.tree = QTreeView()
      self.tree.setModel(self.tree_model)
      self.tree.setRootIndex(self.tree_model.index(self.current_dir))
      
      self.tree.setAnimated(False)
      self.tree.setIndentation(20)
      self.tree.setSortingEnabled(True)
      
      # Resize name row
      old_length = self.tree.columnWidth(0)
      self.tree.setColumnWidth(0, old_length * 3)

      # self.list_widget.currentItemChanged.connect(self.index_changed)
      # self.list_widget.currentTextChanged.connect(self.text_changed)
      self.tree.doubleClicked.connect(self.double_click_file)
      self.tree.clicked.connect(self.click_file)


   def _init_db(self):
      logging.info("Initializing FileDB")
      self.db = FileDB()


   def update_current_dir(self, text):
      self.current_dir_wid.setText(self.current_dir)


if __name__ == "__main__":
   # Initalize logs
   logFile = os.path.join("logs","stl_manager.log")
   if (os.path.exists(logFile)):
      os.remove(logFile)
   
   logging.basicConfig(filename=logFile, encoding='utf-8', level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
   logging.info("Logging initialized")

   # Basic QT window
   app = QApplication([])
   
   with open("stylesheet.qss") as fh:
      app.setStyleSheet(fh.read())

   window = MainWindow()

   window.show()
   sys.exit(app.exec_())

