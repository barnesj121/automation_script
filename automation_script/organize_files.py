import os
import shutil
import logging
import sys

# Set up logging for better tracking and debugging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define file categories with their corresponding extensions
CATEGORIES = {
    'Images': ['.png', '.jpg', '.jpeg', '.gif'],
    'Documents': ['.pdf', '.docx', '.txt', '.xlsx'],
    'Videos': ['.mp4', '.mkv', '.avi'],
    'Music': ['.mp3', '.wav', '.aac'],
}

def create_directories(destination):
    """
    Create category directories in the destination path.
    """
    for folder in CATEGORIES.keys():
        folder_path = os.path.join(destination, folder)
        try:
            os.makedirs(folder_path, exist_ok=True)
            logging.info(f'Created directory: {folder_path}')
        except Exception as e:
            logging.error(f'Error creating directory {folder_path}: {e}')

def move_file(file_path, destination):
    """
    Move a file to the appropriate category folder.
    """
    filename = os.path.basename(file_path)
    for category, extensions in CATEGORIES.items():
        if filename.lower().endswith(tuple(extensions)):
            destination_path = os.path.join(destination, category, filename)
            try:
                shutil.move(file_path, destination_path)
                logging.info(f'Moved: {filename} to {category}')
                return True
            except Exception as e:
                logging.error(f'Error moving file {filename}: {e}')
    return False

def organize_files(source, destination):
    """
    Organize files from the source directory into the destination directory based on file types.
    """
    if not os.path.exists(source):
        logging.error(f'Source directory does not exist: {source}')
        return

    create_directories(destination)

    # Iterate over files in the source directory
    for filename in os.listdir(source):
        file_path = os.path.join(source, filename)
        if os.path.isfile(file_path):
            if not move_file(file_path, destination):
                logging.info(f'No category for: {filename}')

def main(source, destination):
    """
    Main function to organize files.
    """
    organize_files(source, destination)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        logging.error("Usage: python organize_files.py <source_directory> <destination_directory>")
        sys.exit(1)

    source_directory = os.path.abspath(sys.argv[1])
    destination_directory = os.path.abspath(sys.argv[2])
    
    main(source_directory, destination_directory)
