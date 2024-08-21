import os
import shutil

def move_file(source: str, destination: str) -> bool:
    try:
        shutil.move(source, destination)
        print(f"Moved file from {source} to {destination}")
        return True
    except Exception as e:
        print(f"Error moving file: {e}")
        return False

def download_file(url: str, destination: str) -> bool:
    try:
        response = requests.get(url, stream=True)
        with open(destination, 'wb') as file:
            shutil.copyfileobj(response.raw, file)
        print(f"Downloaded file to {destination}")
        return True
    except Exception as e:
        print(f"Error downloading file: {e}")
        return False
