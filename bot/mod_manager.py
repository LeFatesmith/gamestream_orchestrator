import os
import shutil
import requests
import zipfile
import subprocess
from typing import List, Dict, Optional

class ModManager:
    def __init__(self, mod_config: Dict):
        self.mod_config = mod_config

    def download_mod(self, url: str, destination: str) -> bool:
        try:
            response = requests.get(url, stream=True)
            with open(destination, 'wb') as file:
                shutil.copyfileobj(response.raw, file)
            print(f"Downloaded mod to {destination}")
            return True
        except Exception as e:
            print(f"Error downloading mod: {e}")
            return False

    def extract_mod(self, archive_path: str, extract_to: str) -> bool:
        try:
            with zipfile.ZipFile(archive_path, 'r') as archive:
                archive.extractall(extract_to)
            print(f"Extracted mod to {extract_to}")
            return True
        except Exception as e:
            print(f"Error extracting mod: {e}")
            return False

    def copy_files(self, source: str, destination: str) -> bool:
        try:
            if not os.path.exists(destination):
                os.makedirs(destination)
            shutil.copytree(source, destination, dirs_exist_ok=True)
            print(f"Copied files from {source} to {destination}")
            return True
        except Exception as e:
            print(f"Error copying files: {e}")
            return False

    def run_install_script(self, commands: List[str]) -> bool:
        try:
            for command in commands:
                subprocess.run(command, shell=True, check=True)
            print(f"Ran installation script: {commands}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error running script: {e}")
            return False
