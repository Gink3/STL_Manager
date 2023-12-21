import configparser
from file_tree import FileTreeParser 

if __name__ == "__main__":
   # Initialize config parser
   config = configparser.ConfigParser()
   config.read('config.txt')

   print(config['DEFAULT']['LibraryRoot'])

   parser = FileTreeParser(config['DEFAULT']['LibraryRoot'])