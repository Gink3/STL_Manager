import os
from pathlib import Path

class FileTreeParser:
   def __init__(self, root):
      self.file_dict = dict()
      self.num_node_parsed = 0
      self.root_path = root


   def check_duplicates(self):
      """
      Checks library for duplicate files
      """
      directory = Path(self.root_path)
      files = []
      for i in directory.rglob(r"*.stl"):
         filename = os.path.basename(i)
         files.append(filename)
         #print(filename)
      print(len(files))
      for name in files:
         if files.count(name) > 1:
            print("Duplicate Found: " + name + ", " + str(files.count(name)) + " times")



if __name__ == "__main__":
   parser = FileTreeParser("D:\\3D_Printing")
