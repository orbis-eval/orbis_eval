from pathlib import Path
import os
import shutil

def main():
    p = Path('.')

    # """
    for folder in list(p.glob('**/__pycache__')):
        print(f"Removing folder: {folder}")
        shutil.rmtree(folder)
    # """

    # """
    for item in list(p.glob('**/*.pyc')):
        print(f"Removing file: {item}")
        os.remove(item)
    # """
