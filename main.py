import configparser


if __name__ == "__main__":
   # Initialize config parser
   config = configparser.ConfigParser()
   config.read('config.txt')
   
   print(config['DEFAULT']['LibraryRoot'])