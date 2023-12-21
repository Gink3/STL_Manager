import configparser
from file_tree import FileTreeParser 

# https://build-system.fman.io/pyqt5-tutorial
from PyQt5.QtWidgets import QApplication, QLabel


if __name__ == "__main__":
   # Initialize config parser
   config = configparser.ConfigParser()
   config.read('config.txt')
   print(config['DEFAULT']['LibraryRoot'])
   parser = FileTreeParser(config['DEFAULT']['LibraryRoot'])

   # Basic QT window
   app = QApplication([])
   label = QLabel('STL Manager')
   label.show()
   app.exec()