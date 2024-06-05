
import sqlite3
import hashlib
import os
from pathlib import Path
import logging

class FileDB():
   def __init__(self,dbFile="stl_data.db"):
      '''
      self.con - db Connection
      self.cur - db cursor to execute queries
      '''
      if os.path.exists(dbFile):
         already_generated = True
      self.con = sqlite3.connect(dbFile)
      self.cur = self.con.cursor()
      
      if not already_generated:
         self.cur.execute("""
                        CREATE TABLE file(
                        hash TEXT NOT NULL, 
                        path TEXT NOT NULL, 
                        sculptor TEXT, 
                        source TEXT, 
                        tags TEXT, 
                        notes TEXT
                        PRIMARY KEY(hash, path))
                        """)


   def __del__(self):
      '''
      Destructor for db connection
      '''
      self.con.close()


   def insert_file(self, filepath):
      hash = self._hash_file(filepath)
      sql = ''' INSERT into file(hash, path) VALUES(?,?) '''
      self.cur.execute(sql,(hash, filepath))
      self.con.commit()


   def _hash_file(self, filepath):
      new_hash = hashlib.md5(open(filepath,'rb').read()).hexdigest()
      logging.debug("Hashed: " + filepath + " -> " + new_hash)
      return new_hash


   def print_db(self):
      query = "SELECT * FROM file"
      res = self.cur.execute(query)
      print(res.fetchone())


if __name__ == "__main__":
   print("Running filedb.py")

   example_stl = os.path.join("test","Circle_25mm_A.stl")
   print("Example STL File:", example_stl)

   logFile = os.path.join("logs","filedb.log")
   if (os.path.exists(logFile)):
      os.remove(logFile)
   
   logging.basicConfig(filename=logFile, encoding='utf-8', level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
   logging.info("Logging initialized")

   fdb = FileDB()
   fdb.insert_file(example_stl)
   fdb.print_db()