import json
import shutil
from pathlib import Path
from typing import Union

from loguru import logger

from src.data import DATA_DIR
from src.utils.io import read_json


class OrganizeFiles:
    """
    This class is used to organize files in a directory by
     moving files into directories based on extentions
    """
    def __init__(self):
        ext_dirs = read_json(DATA_DIR / "extensions.json")
        self.extensions_dest = {}
        for dir_name, ext_list in ext_dirs.items():
            for ext in ext_list:
                self.extensions_dest[ext] = dir_name
        #print(self.extensions_dest)

    def __call__(self, directory: Union[str, Path]):
        """
        Organize fils in a directory by moving them
        to subdirectories based on extension.
        """
        directory = Path(directory)
        if not directory.exists():
            raise FileNotFoundError(f"{directory} Does Not Exist!")

        logger.info(f"Organizing files in {directory}...")
        file_extensions = []
        for file_path in directory.iterdir():
            #IGNORE DIRECTORIES
            if file_path.is_dir():
                continue
            #IGNORE HIDDEN FILES
            if file_path.name.startswith('.'):
                continue

            #MOVE FILES
            file_extensions.append(file_path.suffix)
            if file_path.suffix not in self.extensions_dest:
                DEST_DIR = directory / 'Other'
            else:
                DEST_DIR = directory / self.extensions_dest[file_path.suffix]

            DEST_DIR.mkdir(exist_ok = True)
            logger.info("Moving {file_path} to {DEST_DIR}...")
            shutil.move(str(file_path), str(DEST_DIR))


if __name__ == "__main__":
    org_files = OrganizeFiles()
    org_files('/mnt/c/Users/M.Gholinejad/Downloads')
    print("Done!")




