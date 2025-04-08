print("Script started")
import os
import shutil
from pathlib import Path
import schedule
import time
import tempfile


print(tempfile.gettempdir())
os.environ['TMPDIR'] = os.path.expanduser('~/custom_temp')
tempfile.tempdir = os.environ['TMPDIR']

# File types and destination folders
FILE_TYPES = {
    'Images': ['.jpg', '.jpeg', '.png', '.gif'],
    'Documents': ['.pdf', '.docx', '.txt', '.xlsx'],
    'Videos': ['.mp4', '.mov', '.avi'],
    'Audio': ['.mp3', '.wav'],
    'Archives': ['.zip', '.rar', '.tar', '.gz'],
    'Code': ['.py', '.js', '.html', '.css', '.cpp'],
}

# Default download path
FOLDERS_TO_WATCH = [
    str(Path.home() / "Downloads"),
    str(Path.home() / "Desktop"),
    str(Path.home() / "Documents"),
    # Add more folders here
]

# Function to organize files
def organizeFiles(path):
    print(f"Organizing files in: {path}")
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isfile(item_path):
            ext = os.path.splitext(item)[1].lower()
            moved = False
            for folder, extensions in FILE_TYPES.items():
                if ext in extensions:
                    folder_path = os.path.join(path, folder)
                    os.makedirs(folder_path, exist_ok=True)
                    shutil.move(item_path, os.path.join(folder_path, item))
                    moved = True
                    break
            if not moved:
                other_path = os.path.join(path, 'Others')
                os.makedirs(other_path, exist_ok=True)
                shutil.move(item_path, os.path.join(other_path, item))

# Schedule the script to run every 10 minutes
for folder in FOLDERS_TO_WATCH:
    schedule.every(10).minutes.do(organizeFiles, folder)


# Run loop
while True:
    schedule.run_pending()
    time.sleep(1)
