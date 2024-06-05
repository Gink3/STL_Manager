# STL_Manager

# Key functionality
* Browse and view 3D printing files
* Handle metadata files for searching and file association
* Search Library
* Model preview

# Install & Running #
After cloning repo change the library root directory path in config.txt to a valid absolute path


Then run `python -m pip install -r requirements.txt` to install required packages
To run the program run `python  ./src/main.py`


# Development Tasks #
[ ] File Metadata display
[ ] Initial Config dialog
[ ] Allow for multiple "library" directories
[ ] Add drop down to select between the different library directories

## Key Terms ##
* Model file - file like .stl, .obj
* Metadata -
   * Unique hash
   * Absolute Filepath
   * Sculptor
   * Source
   * Tags
   * Notes
