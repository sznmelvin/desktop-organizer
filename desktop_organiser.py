from os import scandir, rename
from os.path import exists, join, splitext
from shutil import move
import os

import logging

# Define the source directory and destination directories
source_dir = r"C:\Users\USER\Downloads"
dest_dir_sfx = r"C:\Users\USER\Music\Sound"
dest_dir_music = r"C:\Users\USER\Music\Downloaded Music"
dest_dir_video = r"C:\Users\USER\Videos\Downloaded Videos"
dest_dir_image = r"C:\Users\USER\Pictures\Downloaded Images"
dest_dir_documents = r"C:\Users\USER\Documents\Downloaded Documents"

# Define the file extensions for different file types
image_extensions = [".jpg", ".jpeg", ".png", ".gif", 
                    ".bmp", ".tiff", ".svg", ".webp"]

video_extensions = [".mp4", ".avi", ".mov", ".wmv", 
                    ".flv", ".mkv", ".webm", ".m4v", ".3gp"]

audio_extensions = [".mp3", ".wav", ".ogg", ".aac",
                    ".flac", ".wma", ".m4a", ".opus", ".aiff"]

document_extensions = [".doc", ".docx", ".pdf", ".txt", 
                       ".rtf", ".ppt", ".pptx", ".xls", ".xlsx", ".csv"]

def make_unique(dest, name):
    """
    Create a unique filename by adding a counter to the filename if it already exists.
    """
    filename, extension = splitext(name)
    counter = 1

    while exists(f"{dest}/{name}"):
        name = f"{filename}({str(counter)}){extension}"
        counter += 1

    return name

def move_file(dest, entry, name):
    """
    Move a file to a destination directory, making the filename unique if necessary.
    """
    if exists(f"{dest}/{name}"):
        unique_name = make_unique(dest, name)
        oldName = join(dest, name)
        newName = join(dest, unique_name)
        rename(oldName, newName)
    move(entry, dest)

def on_cleaner(self, event):
    """
    Move files from the source directory to the appropriate destination directory based on their file extension.
    """
    with scandir(source_dir) as entries:
        for entry in entries:
            name = entry.name
            if os.path.is_file(entry.path):
                # Check if the file is an audio file
                if self.check_audio_files(entry, name):
                    continue
                # Check if the file is a video file
                if self.check_video_files(entry, name):
                    continue
                # Check if the file is an image file
                if self.check_image_files(entry, name):
                    continue
                # Check if the file is a document file
                if self.check_document_files(entry, name):
                    continue

def check_audio_files(self, entry, name): # Checks All Audio Files
    """
    Move audio files to the appropriate destination directory.
    """
    for audio_extension in audio_extensions:
        if name.endswith(audio_extension) or name.endswith(audio_extension.upper()):
            dest = dest_dir_sfx if entry.stat().st_size < 10_000_000 or "SFX" in name else dest_dir_music
            move_file(dest, entry, name)
            logging.info(f"Moved audio file: {name}")
            return True
    return False

def check_video_files(self, entry, name): # Checks All Video Files
    """
    Move video files to the appropriate destination directory.
    """
    for video_extension in video_extensions:
        if name.endswith(video_extension) or name.endswith(image_extensions.upper()):
            move_file(dest_dir_video, entry, name)
            logging.info(f"Moved video file: {name}")
            return True
    return False

def check_image_files(self,entry, name): # Checks All Image Files
    """
    Move image files to the appropriate destination directory.
    """
    for image_extension in image_extensions:
        if name.endswith(image_extension) or name.endswith(image_extension.upper()):
            move_file(dest_dir_image, entry, name)
            logging.info(f"Moved image file: {name}")
            return True
    return False

def check_document_files(self, entry, name): # Checks All Document Files
    """
    Move document files to the appropriate destination directory.
    """
    for document_extension in document_extensions:
        if name.endswith(document_extension) or name.endswith(document_extension.upper()):
            move_file(dest_dir_documents, entry, name)
            logging.info(f"Moved document file: {name}")
            return True
    return False
