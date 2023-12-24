#!/usr/bin/python3

import os
import logging
from pathlib import Path
import configparser

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


   def list_model_files(self, path):
      """
      Gets a list of all 3d model files from a directory
      """
      logging.debug("Got to list_model_files with " + path)
      # TODO Check if file path is valid
      directory = Path(path)
      model_files = dict()
      model_files[".."] = str(directory.parent)
      logging.debug(model_files[".."])
      # iterate through directory contents
      for i in os.listdir(directory):
         filename = os.path.basename(i)
        
         # TODO change to accept more file formats like .obj, .3fd etc..
         if i.endswith(".stl") or i.endswith(".obj"):
            model_files[filename] = os.path.join(directory,filename)
         
         # Check if item is a directory in current folder
         if os.path.isdir(os.path.join(directory,filename)):
            logging.debug("Found directory: " + os.path.join(directory,filename))
            model_files[filename+"\\"] = os.path.join(directory,filename)

      logging.debug("list_model_files(" + path + ") Returning: " + str(model_files))
      return model_files
   

   def scan_for_metadata(self):
      """
      Checks all .stl files in a library for a corresponding metadata file
      """
      # TODO Benchmark the performance over a larger library
      directory = Path(self.root_path)
      for i in directory.rglob(r"*.stl"):
         self.check_for_mtd_file(i)


   def check_for_mtd_file(self, filepath):
      """
      Check if the given file has a metadata file already associated with it
      """
      # TODO Create a filter check function for model object extensions
      if filepath.name.endswith(".stl"):   
         # if file path exists
         if filepath.exists():
            logging.debug("Filepath: " + str(filepath))
            logging.debug("Basename: " + filepath.name)
            # get metadata filepath
            metadata_file = self.get_metadata_filepath(filepath)
            # Check if metadata filepath exists
            if metadata_file.exists():
               logging.debug("Found metadata file: " + str(metadata_file))
            else:
               # if not already created, create
               logging.debug("Metadata file not found, creating" + str(metadata_file))
               # TODO Create function to generate the default metadata file contents
               with metadata_file.open("w", encoding="utf-8") as f:
                  f.write("Created " + str(metadata_file))


   def get_metadata_filepath(self, modelpath):
      """"
      Convert a model file path to metadata file
      """
      logging.debug("Entering get_metadata_filepath")
      return modelpath.parent.joinpath("." + modelpath.name[:-3] + "mtd")


   def get_root_path(self):
      return self.root_path
   

   def get_metadata_filename(self, model_filename):
      """
      model_file - 3d model file, such as .obj, .3fd, .stl
      get the file name of the metadata file which should be in the format
      .<file name>.mtd
      """
      return "." + model_filename.split(".")[0] + ".mtd"


if __name__ == "__main__":
   logging.basicConfig(filename='file_tree.log', encoding='utf-8', level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
   logging.info("Logging initialized")

   config = configparser.ConfigParser()
   config.read('config.txt')
   current_dir = config['DEFAULT']['LibraryRoot']

   parser = FileTreeParser(current_dir)

   parser.scan_for_metadata()