import os


class FileTreeParser:
   def __init__(self, root):
      self.file_dict = dict()
      self.num_node_parsed = 0
      self.root_path = root


   def check_duplicates(self):
      # define root file path
      root = self.root_path
      print("Parsing for duplicate .stl files from \"" + root + "\"")
      list_dir = os.listdir(root)

      # Iterate through the list of directories
      for node in list_dir:
         self.num_node_parsed += 1
         next_node = os.path.join(root, node)
         
         if node.endswith(".stl"):
            print("Parsing: {}".format(next_node))

         # If a directory add to the list of directories to go through
         if os.path.isdir(next_node):
            # Check if filepath is a duplicate
            # Shouldn't happen, but want to be safe
            if not next_node in list_dir:
               list_dir.append(next_node)
         # # If a file
         # else:
         #    # If file is an stl file, check to add into the dict
         #    if node.endswith(".stl"):
         #       if not self.file_dict.keys().contains(node):
         #          self.file_dict[node] = 1
         #       else: 
         #          self.file_dict[node] += 1
         #    # If not an stl file, ignore
         #    else:
         #       continue
         
      print(self.file_dict)
      print("Number of Nodes Parsed: {}".format(self.num_node_parsed))




if __name__ == "__main__":
   parser = FileTreeParser("D:\\3D_Printing")
   parser.check_duplicates()