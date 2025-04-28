import os
import shutil
import time
import hashlib
import json
from PIL import Image
import logging

# CONFIGURATIONS
IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.webp', '.bmp', '.tiff')
GENERAL_COMPRESSION_QUALITY = 75
TARGET_DIRS_TO_SCAN = ['/Users/chiragdahiya']  # Update accordingly
EXCLUDED_FOLDERS = [
    # System and application folders
    'Library', 'System', 'Applications', 'node_modules',
    
    # Development and coding related folders
    'fullstack-project', 'ic-projects', 'miniforge3', 'tensorflow-proj',
    'StudioProjects', 'Scripts', 'custom_temp', 'CS Notes', 'Postman',
    'Project', 'LocalAppData', 'Google Drive',
    
    # Build and dependency folders that may contain optimized images
    '.git', '.vscode', 'dist', 'build', 'venv', 'env',
    
    # Special folders
    'footage', 'Movies', 'Music', 'Downloads', 'MEGA downloads',
    
    # Already optimized files
    'ImageBackup'
]
GLOBAL_BACKUP_FOLDER = '/Users/chiragdahiya/ImageBackup'
TRACKING_DB_PATH = '/Users/chiragdahiya/ImageBackup/tracking_db.json'

# Setup logging
log_file = '/Users/chiragdahiya/ImageBackup/image_optimizer.log'
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(message)s')

def is_image_file(file_name):
    return file_name.lower().endswith(IMAGE_EXTENSIONS)

def get_file_hash(file_path):
    """Generate a hash of file contents to identify unique files"""
    try:
        with open(file_path, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    except Exception as e:
        logging.error(f"Failed to hash file {file_path}: {e}")
        return None

def load_tracking_db():
    """Load the tracking database of processed files"""
    try:
        if os.path.exists(TRACKING_DB_PATH):
            with open(TRACKING_DB_PATH, 'r') as f:
                return json.load(f)
    except Exception as e:
        logging.error(f"Failed to load tracking DB: {e}")
    return {}

def save_tracking_db(db):
    """Save the tracking database of processed files"""
    try:
        print(">>> Saving tracking DB to:", TRACKING_DB_PATH)
        with open(TRACKING_DB_PATH, 'w') as f:
            json.dump(db, f, indent=2)
    except Exception as e:
        logging.error(f"Failed to save tracking DB: {e}")

def has_been_processed(file_path, tracking_db):
    """Check if file has been processed based on content hash and modification time"""
    file_hash = get_file_hash(file_path)
    if not file_hash:
        return False
        
    file_stat = os.stat(file_path)
    file_size = file_stat.st_size
    mod_time = file_stat.st_mtime
    
    # Check if we've processed this exact file before
    if file_hash in tracking_db:
        # If file size and modification time match what we've processed before, skip it
        if (tracking_db[file_hash]['size'] == file_size and 
            tracking_db[file_hash]['mtime'] == mod_time):
            return True
        # Hash matches but other properties don't - file was modified after processing
        return False
    
    return False

def create_backup(input_path):
    relative_folder = os.path.basename(os.path.dirname(input_path))
    backup_folder_path = os.path.join(GLOBAL_BACKUP_FOLDER, relative_folder)
    os.makedirs(backup_folder_path, exist_ok=True)

    backup_file_path = os.path.join(backup_folder_path, os.path.basename(input_path))

    if not os.path.exists(backup_file_path):
        shutil.copy2(input_path, backup_file_path)
        logging.info(f"Backup created: {backup_file_path}")
    else:
        logging.info(f"Backup already exists: {backup_file_path}")

def compress_image(input_path, output_path, quality=GENERAL_COMPRESSION_QUALITY):
    try:
        img = Image.open(input_path)
        img.save(output_path, optimize=True, quality=quality)
        logging.info(f"Compressed: {input_path}")
    except Exception as e:
        logging.error(f"Failed to compress {input_path}: {e}")

def compress_resume_image(input_path, output_folder):
    base_name = os.path.splitext(os.path.basename(input_path))[0]
    try:
        img = Image.open(input_path)

        # Save original copy
        original_path = os.path.join(output_folder, f"{base_name}_original.jpg")
        img.save(original_path, optimize=True, quality=95)

        # Save under 2MB
        path_2mb = os.path.join(output_folder, f"{base_name}_2mb.jpg")
        img.save(path_2mb, optimize=True, quality=85)

        # Save under 1MB
        path_1mb = os.path.join(output_folder, f"{base_name}_1mb.jpg")
        img.save(path_1mb, optimize=True, quality=70)

        # Save under 0.5MB
        path_05mb = os.path.join(output_folder, f"{base_name}_05mb.jpg")
        img.save(path_05mb, optimize=True, quality=50)

        logging.info(f"Compressed resume versions for {input_path}")
    except Exception as e:
        logging.error(f"Failed resume compress {input_path}: {e}")

def should_skip_folder(folder_path):
    folder_name = os.path.basename(folder_path).lower()
    
    # Skip if the current folder name matches any excluded folder
    if any(excluded.lower() == folder_name for excluded in EXCLUDED_FOLDERS):
        return True
    
    # Skip if the path contains any excluded folder
    if any(f'/{excluded.lower()}/' in folder_path.lower() for excluded in EXCLUDED_FOLDERS):
        return True
        
    return False

def scan_and_compress():
    """Scan and compress images"""
    os.makedirs(GLOBAL_BACKUP_FOLDER, exist_ok=True)
    tracking_db = load_tracking_db()
    processed_files = 0
    
    for base_dir in TARGET_DIRS_TO_SCAN:
        for root, dirs, files in os.walk(base_dir, onerror=lambda e: logging.warning(f"Skipping {e.filename}: {e.strerror}")):
            if should_skip_folder(root):
                continue

            for file in files:
                if is_image_file(file):
                    full_path = os.path.join(root, file)
                    
                    # Check if this file needs processing
                    if has_been_processed(full_path, tracking_db):
                        logging.info(f"Skipping already processed file: {full_path}")
                        continue
                    
                    # Process the file
                    file_hash = get_file_hash(full_path)
                    if not file_hash:
                        continue
                        
                    create_backup(full_path)
                    
                    if os.path.basename(root).lower() == 'resume':
                        compress_resume_image(full_path, root)
                    else:
                        compress_image(full_path, full_path)
                    
                    # Update tracking database with this file's info
                    file_stat = os.stat(full_path)
                    tracking_db[file_hash] = {
                        'path': full_path,
                        'size': file_stat.st_size,
                        'mtime': file_stat.st_mtime,
                        'processed_at': time.time()
                    }
                    processed_files += 1
                    
                    # Periodically save the tracking database if processing many files
                    if processed_files % 100 == 0:
                        save_tracking_db(tracking_db)
    
    # Save the final tracking database
    save_tracking_db(tracking_db)
    logging.info(f"Processed {processed_files} files")

if __name__ == "__main__":
    logging.info("Script started.")
    scan_and_compress()
    logging.info("Script finished.")